"""Append-only event chain (per D10 + D23).

Per D10, the workspace has a single ordered event chain. Events form
the workspace's attribution-bearing record; integrity is checkable
(mechanism unspecified at framework-core — D10 is explicit it leaves
the mechanism open). Per B2 design lock (see B2 brief §"Design choices
already locked"): the in-process substrate uses an append-only Python
list with sequential integer sequence numbers + `prev-event` chain
validation. Schema validation per `event.schema.json` is applied at
append time so structurally-invalid events are rejected before they
enter the chain.

This module owns only the chain mechanism. Per-event referential
integrity (D30 §4 runtime portion) lives in `per_event_checks.py`;
both are invoked by the substrate's `append` orchestration.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator, Optional

from fresh_plan.validator.schemas import SchemaStore
from fresh_plan.validator.types import ValidationFailure


class MalformedEventError(Exception):
    """Raised when an event fails schema validation or chain-integrity checks.

    Carries the structured failure list so callers can report them the same
    way the B1 validator does. The substrate translates these into
    `EventRejected` exceptions on the public surface.
    """

    def __init__(self, failures: list[ValidationFailure]) -> None:
        self.failures = failures
        msg = "; ".join(f"[{f.category}] {f.path}: {f.reason}" for f in failures)
        super().__init__(msg or "malformed event")


@dataclass
class _ChainEntry:
    """One entry in the chain: the event dict plus its assigned sequence number."""

    sequence: int
    event: dict


@dataclass
class AppendOnlyEventChain:
    """Append-only chain backing the workspace's single event timeline.

    Per D10:
      - one ordered chain per workspace,
      - `prev-event` references the prior event id (`null` only for the
        first event ever),
      - integrity-checkable (B2: append-only list + sequence numbers).

    Per B2 design lock: state is in-memory; persistence is deferred.
    """

    _entries: list[_ChainEntry] = field(default_factory=list)

    # -----------------------------------------------------------------
    # Append
    # -----------------------------------------------------------------

    def append(self, event: dict, schema_store: SchemaStore) -> int:
        """Validate + append the event. Returns the assigned sequence number.

        Schema validation is run first (per D10 the framework validates
        the five core payload subtypes). Chain integrity is then checked:
        `prev-event` must be `null` on the first event and match the
        previous event's id thereafter. Failures raise MalformedEventError;
        the event is NOT appended.
        """
        failures = self._schema_validate(event, schema_store)
        if not failures:
            failures += self._integrity_check(event)
        if failures:
            raise MalformedEventError(failures)

        seq = len(self._entries)
        self._entries.append(_ChainEntry(sequence=seq, event=event))
        return seq

    def _schema_validate(
        self, event: dict, schema_store: SchemaStore
    ) -> list[ValidationFailure]:
        """Run event.schema.json validation; wrap errors as ValidationFailures."""
        validator = schema_store.validator_for("event.schema.json")
        failures: list[ValidationFailure] = []
        for err in validator.iter_errors(event):
            path_parts = list(err.absolute_path)
            path_str = ".".join(
                f"[{p}]" if isinstance(p, int) else str(p) for p in path_parts
            ) or "<root>"
            failures.append(
                ValidationFailure(
                    category="schema",
                    path=f"event.{path_str}",
                    value=err.instance if not isinstance(err.instance, (dict, list)) else None,
                    reason=err.message,
                )
            )
        return failures

    def _integrity_check(self, event: dict) -> list[ValidationFailure]:
        """Validate chain integrity (`prev-event` rules)."""
        failures: list[ValidationFailure] = []
        prev = event.get("prev-event")
        if not self._entries:
            if prev is not None:
                failures.append(
                    ValidationFailure(
                        category="identity",
                        path="event.prev-event",
                        value=prev,
                        reason=(
                            "first event in chain must have prev-event=null; "
                            f"got {prev!r}"
                        ),
                    )
                )
        else:
            tail_id = self._entries[-1].event.get("id")
            if prev != tail_id:
                failures.append(
                    ValidationFailure(
                        category="identity",
                        path="event.prev-event",
                        value=prev,
                        reason=(
                            f"prev-event {prev!r} does not match tail event id "
                            f"{tail_id!r}"
                        ),
                    )
                )
        # event id must be unique within chain
        eid = event.get("id")
        if eid is not None:
            for entry in self._entries:
                if entry.event.get("id") == eid:
                    failures.append(
                        ValidationFailure(
                            category="identity",
                            path="event.id",
                            value=eid,
                            reason=f"duplicate event id {eid!r} in chain",
                        )
                    )
                    break
        return failures

    # -----------------------------------------------------------------
    # Query API (derived views per D10: filter, don't store)
    # -----------------------------------------------------------------

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[dict]:
        for entry in self._entries:
            yield entry.event

    @property
    def tail(self) -> Optional[dict]:
        """The most recently appended event, or None if the chain is empty."""
        return self._entries[-1].event if self._entries else None

    def all_events(self) -> list[dict]:
        """All events in append order (a fresh copy)."""
        return [e.event for e in self._entries]

    def by_id(self, event_id: str) -> Optional[dict]:
        for entry in self._entries:
            if entry.event.get("id") == event_id:
                return entry.event
        return None

    def by_actor(self, actor_id: str) -> list[dict]:
        return [
            e.event
            for e in self._entries
            if any(a.get("id") == actor_id for a in e.event.get("actors", []))
        ]

    def by_work_unit(self, work_unit_id: str) -> list[dict]:
        return [
            e.event
            for e in self._entries
            if e.event.get("work-unit-id") == work_unit_id
        ]

    def by_payload_subtype(self, subtype: str) -> list[dict]:
        return [
            e.event for e in self._entries if e.event.get("payload-subtype") == subtype
        ]

    def sequence_of(self, event_id: str) -> Optional[int]:
        for entry in self._entries:
            if entry.event.get("id") == event_id:
                return entry.sequence
        return None
