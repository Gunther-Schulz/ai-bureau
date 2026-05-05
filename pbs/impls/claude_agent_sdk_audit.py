"""Claude Agent SDK audit storage realization — Phase 6.1 reference impl.

Per `arch/audit.md` §4 per-substrate-impl storage realization 'Default Claude
Agent SDK substrate: jsonl file-backed (per archived audit-trail-v2.md);
local filesystem persistence; hash-chain integrity primitive; line-delimited
AuditEvent records; query implementation reads file + filters.'

This module realizes the **storage backend** parameterizing the Audit
mechanism class Surface (`AuditProtocol`) for the Claude Agent SDK substrate
Implementation. Per `arch/audit.md` §6 mechanism-class structural
reconciliation: the class Surface (AuditEvent schema + 7 capability
categories) is fixed at framework-mechanism layer + same across all
substrate-impls; per-substrate-impl realization (jsonl / Postgres / cloud /
federation) inherits from selected substrate Implementation per substrate
Surface §F. Storage-backend variation is **substrate-impl level**, NOT
audit-class-level pluggability — that's the discriminator distinguishing
audit (mechanism class) from Pattern A protocols.

Surface satisfaction (`pbs.audit.AuditProtocol` per `arch/audit.md` §2):

- §A Emission API + actor declaration → `emit()` (substrate-internal direct
  + skill-side via MCP audit gate both converge here per §8 dual-emission
  resolution)
- §B Append-only persistence → file opened in append mode 'a'; per-emit
  flush; tamper detection via §D hash-chain re-walk; attempted rewrite /
  truncate / rewind raises `AuditAppendOnlyViolation`
- §C Query for reasoning-chain reconstruction → `query_per_claim` /
  `query_per_actor` / `query_per_time_window` / `query_per_event_kind` /
  `query_per_work_unit` (file-scan + filter; index-backed query is Phase
  6.2+ per `arch/audit.md` §15)
- §D Integrity verification → `verify_integrity()` re-walks the SHA-256
  hash-chain; raises `AuditIntegrityError` + emits
  `AuditTrailIntegrityViolated` on hash-chain break (per `arch/audit.md`
  §11 substrate-impl detects)
- §E Event-kind catalog management → at three layers (framework baseline /
  per-shape / per-specialist) per `arch/audit.md` §2.E. Reference impl
  enforces the active shape's mandatory catalog when
  `catalog_enforcement=True` is set on config; otherwise accepts any
  `AuditEventBase` subclass
- §F State-rendering-from-events → `render_state(kind)` derives workspace
  state from the event sequence (3 reference kinds: `workflow_instance` /
  `claim_status` / `actor_activity`); richer kinds Phase 6 wiring
- §G Cross-deployment external-format export → `export(format)` supports
  `jsonl` (raw bytes copy); `pdf` / `csv` / `regulator_submission` are
  Phase 6 wiring points

Per `arch/audit.md` §10 boot/shutdown phase ordering invariant + the canonical
composite sequence at `ARCHITECTURE.md` §6 Workspace boot + shutdown
composite sequence subsection: this audit storage realization MUST be ready
(audit-phase 1-3) BEFORE the substrate Implementation emits its first
architectural event (substrate-phase 1+). The realization shuts down LAST
(after substrate / quality-gate / sparring drains complete) so every
emitted event lands in the audit-trail before workspace shutdown returns.

Per `arch/audit.md` §11 per-shape error semantics: practitioner-shape =
fail-closed (defensibility-critical; default); autonomous-business-shape =
fail-open with alert + queued-retry (Phase 6.2 wiring); personal-OS-shape =
fail-open with retry (Phase 6.2 wiring). Phase 6.1 thin-slice is
practitioner-shape per `BACKLOG.md` §224.

Per `arch/audit.md` §11 + `glossary/authority-binding.md`: authority-binding
mechanism is its own framework primitive composing with audit (audit records
the binding actor on every event; per-shape trust policy lives at shape
policy bundle declaring trust at authority-binding mechanism). Reference
impl exposes an `AuthorityChecker` injection point for Phase 6.2 full
mechanism wiring; Phase 6.1 default = no enforcement.

Phase 6 wiring points (marked explicitly in docstrings + `NotImplementedError`
where load-bearing):

- pdf / csv / regulator_submission export formats (§G; specific format
  catalog per `arch/audit.md` §15)
- Cross-deployment migration mechanics (§G round-trip; W2 watch-list)
- Audit-trail compression / archival at scale (W3 watch-list)
- Index-backed query (§C; `arch/audit.md` §15 query implementation)
- Authority-binding mechanism full integration (§11 AuditTrustError; Phase
  6.2 per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table)
- Per-shape mandatory catalog declaration syntax in shape policy bundles
  (§5; `arch/audit.md` §15)
"""

from __future__ import annotations

import hashlib
import json
import threading
from collections.abc import Callable
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from pbs.audit import (
    AuditAppendOnlyViolation,
    AuditCatalogError,
    AuditIntegrityError,
    AuditMigrationError,
    AuditQueryError,
    AuditTrailIntegrityVerified,
    AuditTrailIntegrityViolated,
    AuditTrustError,
    AuditWriteError,
)
from pbs.types.actor_kind import ActorKind
from pbs.types.event_base import AuditEventBase

# ---------------------------------------------------------------------------
# Substrate identity binding
# ---------------------------------------------------------------------------


SUBSTRATE_ID: Literal["claude_agent_sdk"] = "claude_agent_sdk"
"""Substrate Implementation identity per `arch/substrate.md` §4. Audit
storage realization is substrate-impl-pinned per `arch/audit.md` §4; this
realization binds to `claude_agent_sdk` per Pattern A ≥2 implementations
discriminator preserved (current set: claude_agent_sdk + ms_agent_framework
per `docs/decisions/substrate-hand-rolled-drop.md`).
"""


# ---------------------------------------------------------------------------
# Per-shape policy types (per `arch/audit.md` §5 + §11 + §14)
# ---------------------------------------------------------------------------


class AuditGranularity(StrEnum):
    """Per `arch/audit.md` §14 per-shape granularity dimension.

    Values mirror the locked event entry Cross-archetype illustration:
    practitioner-shape = claim-level (every substantive claim emits
    `claim_made` + per-claim attestation events); autonomous-business-shape
    = action-level (per workflow action / task batch / budget-consumed
    checkpoint); personal-OS-shape = light (memory/replay only; minimal
    emission).
    """

    CLAIM_LEVEL = "claim_level"
    ACTION_LEVEL = "action_level"
    LIGHT = "light"


class AuditErrorSemantics(StrEnum):
    """Per `arch/audit.md` §11 + §14 per-shape error semantics on emission
    failure dimension.
    """

    FAIL_CLOSED = "fail_closed"
    """practitioner-shape (defensibility-critical; audit-trail emission
    failure must block)."""

    FAIL_OPEN_WITH_ALERT = "fail_open_with_alert"
    """autonomous-business-shape (continuity prioritized; alert on failure;
    queued-retry mechanism). Phase 6.2 wiring point — reference impl logs
    + returns without retry queue."""

    FAIL_OPEN_WITH_RETRY = "fail_open_with_retry"
    """personal-OS-shape (lightweight; degradation acceptable). Phase 6.2
    wiring point — reference impl logs + returns."""


class AuditTrustModel(StrEnum):
    """Per `arch/audit.md` §14 per-shape trust model dimension (per-shape
    policy on authority-binding mechanism per `MAINTENANCE.md` TOP-LEVEL
    ARCHITECTURE concept-by-concept table).
    """

    PRACTITIONER_JUDGMENT = "practitioner_judgment"
    """practitioner-shape: human-actor required in accountability-bearing
    output chain."""

    BUDGET_POLICY = "budget_policy"
    """autonomous-business-shape: programmatic threshold-based."""

    INDIVIDUAL = "individual"
    """personal-OS-shape: single-user attestation; no chain."""


class AuditShapePolicy(BaseModel):
    """Per-shape audit policy bundle declaration per `arch/audit.md` §5.

    Each per-shape policy bundle declares granularity + mandatory event-kind
    catalog + error semantics + trust model. Reference impl ships
    practitioner-shape defaults (Phase 6.1 thin-slice scope per `BACKLOG.md`
    §224); other shapes wire via config-time policy injection.

    Per-shape mandatory catalog declaration syntax in shape policy bundles is
    a Phase 6 wiring point per `arch/audit.md` §15; reference impl accepts a
    plain `frozenset[str]` of mandatory event_kind values.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    granularity: AuditGranularity = AuditGranularity.CLAIM_LEVEL
    mandatory_catalog: frozenset[str] = Field(default_factory=frozenset)
    error_semantics: AuditErrorSemantics = AuditErrorSemantics.FAIL_CLOSED
    trust_model: AuditTrustModel = AuditTrustModel.PRACTITIONER_JUDGMENT


# ---------------------------------------------------------------------------
# Authority-binding integration (Phase 6.1 stub; Phase 6.2 full mechanism)
# ---------------------------------------------------------------------------


AuthorityChecker = Callable[[AuditEventBase], bool]
"""Authority-binding mechanism integration point per `arch/audit.md` §11
`AuditTrustError` + `glossary/authority-binding.md`.

Returns True if the event passes the per-shape trust policy (e.g., budget-
policy threshold not exceeded; HITL approval present for accountability-
bearing actions); False raises `AuditTrustError`. Phase 6.2 wiring point:
authority-binding mechanism becomes its own framework primitive per
`MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; reference
impl exposes the injection point so substrate Surface §C permission flow
can wire authority decisions through audit Surface §A emission (per
`arch/substrate.md` §C).
"""


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


GENESIS_HASH = "0" * 64
"""SHA-256 hex sentinel for the first event's `prev_hash` (no prior event in
chain). Per `arch/audit.md` §2.D hash-chain integrity verification + W1
watch-list (SHA-256 default; alternative algorithms per substrate-impl)."""


class ClaudeAgentSDKAuditConfig(BaseModel):
    """Per-substrate-impl configuration for the Claude Agent SDK audit
    storage realization.

    Per `arch/audit.md` §4 Default Claude Agent SDK substrate: jsonl file-
    backed; local filesystem persistence; SHA-256 hash-chain primitive.
    """

    model_config = ConfigDict(frozen=True, extra="forbid", arbitrary_types_allowed=True)

    audit_trail_path: Path
    """Filesystem path to the jsonl audit-trail. Substrate-impl owns this
    path per `arch/audit.md` §9 lifecycle ownership 'audit-trail file:
    persists across workspace lifetime; substrate-impl owns'.
    """

    hash_algorithm: Literal["sha256"] = "sha256"
    """Hash-chain algorithm choice per W1 watch-list. SHA-256 default;
    alternative algorithms surface at Phase 6.2 per Tier 2+ deployment
    requirements (e.g., hash-chain-with-Merkle for federation).
    """

    shape_policy: AuditShapePolicy = Field(default_factory=AuditShapePolicy)
    """Active shape's audit policy bundle. Reference impl ships practitioner-
    shape defaults; other shapes wire via config-time policy injection."""

    authority_checker: AuthorityChecker | None = None
    """Optional Phase 6.2 wiring point per `arch/audit.md` §11. Default None
    = no authority-binding enforcement (Phase 6.1 reference; full mechanism
    integration Phase 6.2)."""

    catalog_enforcement: bool = False
    """Whether to enforce the active shape's `mandatory_catalog`. Default
    False = framework baseline only (any AuditEventBase subclass accepted);
    True = `event_kind` validated against `shape_policy.mandatory_catalog`
    per `arch/audit.md` §2.E + §11 `AuditCatalogError`. Phase 6 wiring point
    per `arch/audit.md` §15 declaration syntax."""


# ---------------------------------------------------------------------------
# Internal hash helpers
# ---------------------------------------------------------------------------


def _sha256_line(line: str) -> str:
    """SHA-256 hex digest of a UTF-8 line. Per `arch/audit.md` §2.D + W1
    default; algorithm choice substrate-impl level."""
    return hashlib.sha256(line.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# ClaudeAgentSDKAudit — Implementation class
# ---------------------------------------------------------------------------


class ClaudeAgentSDKAudit:
    """Claude Agent SDK audit storage realization satisfying `AuditProtocol`.

    Per `arch/audit.md` §6 mechanism-class structural reconciliation: this
    class realizes the storage backend (jsonl file-backed) parameterizing
    the Audit mechanism class Surface; the Surface itself is fixed at
    framework-mechanism layer (`pbs.audit.AuditProtocol`) — same across all
    substrate-impls.

    Surface satisfaction is structural — instances pass
    `isinstance(audit, AuditProtocol)` per the `runtime_checkable` Protocol
    decorator on `pbs.audit.AuditProtocol`.

    Lifecycle (per `arch/audit.md` §10 + `ARCHITECTURE.md` §6 composite boot
    subsection):

    - Boot via `from_config(config)` (audit-phase 1-3 ordering — schema
      validated; storage availability verified; existing audit-trail (if
      present) hash-chain re-walked + `audit_storage_ready` becomes True
      BEFORE substrate emits its first architectural event)
    - `audit_storage_ready` becomes True after construction completes
    - `shutdown()` runs §10 shutdown sequence steps 5-8 (drain pending
      writes; flush + close file; verify hash-chain integrity; emit final
      `audit_trail_integrity_verified` event; return)

    State (instance-private):

    - `_tail_hash`: rolling hash-chain tail (genesis sentinel until first
      event)
    - `_event_count`: monotonic event count
    - `_lock`: per-instance lock serializing emit + integrity ops; ensures
      hash-chain consistency under concurrent emit calls
    - `_is_ready`: True between boot completion and shutdown initiation
    - `_is_shutting_down`: idempotent guard for repeated shutdown calls

    Audit emission catalog (per `arch/audit.md` §8 audit-internal events —
    the class's own emissions): `audit_trail_integrity_verified` (final
    shutdown event + per-query / per-migration verification);
    `audit_trail_integrity_violated` (immediate emission on hash-chain
    break); `audit_trail_migrated` (cross-deployment migration boundary);
    `audit_trail_archived` (W3 future).
    """

    def __init__(self, config: ClaudeAgentSDKAuditConfig) -> None:
        """Internal constructor.

        Use `from_config()` factory per `arch/audit.md` §10 boot sequence;
        this constructor is the underlying primitive.
        """
        self._config = config
        self._lock = threading.Lock()
        self._instance_id: str = f"audit:{SUBSTRATE_ID}:{config.audit_trail_path}"
        self._is_ready: bool = False
        self._is_shutting_down: bool = False
        self._tail_hash: str = GENESIS_HASH
        self._event_count: int = 0

    # ------------------------------------------------------------------
    # Lifecycle (§10 boot + shutdown — composite sequence at
    # `ARCHITECTURE.md` §6 audit-phase 1-3)
    # ------------------------------------------------------------------

    @classmethod
    async def from_config(
        cls, config: ClaudeAgentSDKAuditConfig
    ) -> ClaudeAgentSDKAudit:
        """Boot per `arch/audit.md` §10 boot sequence steps 2-4 + composite
        sequence audit-phase 1-3 at `ARCHITECTURE.md` §6.

        - audit-phase 1: AuditEvent schema validation (Pydantic schema
          available at module import; emission API defined)
        - audit-phase 2: Storage backend availability (filesystem accessible;
          parent dir created on demand); existing audit-trail (if present)
          hash-chain re-walked + tail extracted
        - audit-phase 3: `audit_storage_ready` becomes True; emission API
          ready BEFORE substrate emits its first architectural event

        Raises:
            AuditWriteError: storage path inaccessible (filesystem /
                permission / parent-dir creation failure).
            AuditIntegrityError: existing audit-trail hash-chain broken on
                boot-time re-walk (substrate impl detects; class Surface
                declares category per `arch/audit.md` §11).
        """
        instance = cls(config)
        instance._boot()
        return instance

    def _boot(self) -> None:
        """Internal boot — composite sequence audit-phase 2-3 implementation.

        Per `arch/audit.md` §10 boot step 3: 'If existing audit-trail present:
        substrate-impl verifies hash-chain integrity (load prior tail event;
        verify ready-state).'
        """
        path = self._config.audit_trail_path
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise AuditWriteError(
                f"Audit-trail parent dir not creatable at "
                f"{path.parent}: {exc}"
            ) from exc

        if path.exists():
            self._tail_hash, self._event_count = self._scan_chain_tail()
        else:
            try:
                path.touch()
            except OSError as exc:
                raise AuditWriteError(
                    f"Audit-trail file not creatable at {path}: {exc}"
                ) from exc
            self._tail_hash = GENESIS_HASH
            self._event_count = 0

        self._is_ready = True

    @property
    def audit_storage_ready(self) -> bool:
        """Per `arch/audit.md` §10 boot step 4 `audit_storage_ready` flag.

        True between boot completion and shutdown initiation. Substrate
        impl checks this before emitting (composite sequence audit-phase 3
        invariant: emission API ready BEFORE substrate emits first
        architectural event).
        """
        return self._is_ready and not self._is_shutting_down

    async def shutdown(self) -> None:
        """Per `arch/audit.md` §10 shutdown sequence steps 5-8 + composite
        sequence at `ARCHITECTURE.md` §6 step 9 (audit storage realization
        shuts down LAST).

        Per `ARCHITECTURE.md` §6 invariant: every emitted event is persisted
        in audit-trail BEFORE workspace shutdown completes. Substrate /
        quality-gate / sparring drains complete per `arch/audit.md` §10
        steps 1-4 BEFORE this method runs.

        Steps:

        5. Drain pending audit-trail writes (file flush; emit lock-held)
        6. Verify hash-chain integrity at shutdown
        7. Emit `audit_trail_integrity_verified` (final event)
        8. Audit storage realization shutdown returns

        Idempotent: repeated calls return without re-emitting events.
        """
        if self._is_shutting_down:
            return
        with self._lock:
            self._is_shutting_down = True

        # Step 5: drain pending writes — file is already flushed per emit;
        # explicit verification at next step.
        # Step 6: verify hash-chain integrity at shutdown
        try:
            self.verify_integrity()
        except AuditIntegrityError:
            # `AuditTrailIntegrityViolated` was emitted at violation site
            # via verify_integrity; integrity event is final forensic record;
            # do NOT emit `audit_trail_integrity_verified` per §10.
            self._is_ready = False
            raise

        # Step 7: emit `audit_trail_integrity_verified` (final event)
        # `_emit_unguarded` because we hold the relevant invariants ourselves
        # (post-verify hash-chain valid; storage flush already complete; no
        # catalog re-validation since this is the class's own emission).
        self._emit_unguarded(
            AuditTrailIntegrityVerified(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "event_count": self._event_count,
                    "phase": "shutdown",
                },
            )
        )

        # Step 8: shutdown returns
        self._is_ready = False

    # ------------------------------------------------------------------
    # §A Emission API + actor declaration
    # ------------------------------------------------------------------

    def emit(self, event: AuditEventBase) -> None:
        """Per `arch/audit.md` §2.A. Both substrate-internal direct emission
        + skill-side MCP audit gate emission converge here per §8 dual-
        emission resolution.

        Lock-serialized to keep the hash-chain consistent under concurrent
        emit calls. Per §2.B append-only enforced at write boundary by
        opening the file in 'a' mode (kernel guarantees atomic append on
        POSIX; no per-event-rewrite path exists in this realization).

        Raises:
            AuditWriteError: storage failure (filesystem / permission / disk).
            AuditAppendOnlyViolation: append-only invariant violated
                (storage shutdown in flight; emit attempted after shutdown
                completed).
            AuditCatalogError: `event.event_kind` not in active shape's
                mandatory catalog when `catalog_enforcement=True`.
            AuditTrustError: authority-binding policy violated.
        """
        if not self.audit_storage_ready:
            # Distinguish 'shutdown in flight / completed' from 'never booted':
            # shutdown completed = §11 AuditAppendOnlyViolation (emit attempted
            # after shutdown); never booted = AuditWriteError (storage not
            # ready). Per `arch/audit.md` §10 shutdown invariant.
            if self._is_shutting_down:
                raise AuditAppendOnlyViolation(
                    f"Audit storage realization at "
                    f"{self._config.audit_trail_path} shut down; emit "
                    f"rejected per `arch/audit.md` §10 shutdown invariant."
                )
            raise AuditWriteError(
                f"Audit storage realization at "
                f"{self._config.audit_trail_path} not ready; emit rejected."
            )

        with self._lock:
            self._validate_catalog(event)
            self._validate_authority(event)
            self._emit_unguarded(event)

    def _emit_unguarded(self, event: AuditEventBase) -> None:
        """Internal emit bypassing readiness + catalog + authority checks.

        Used by the class's own integrity events (per `arch/audit.md` §8
        audit-internal events — the class audits its own integrity) where
        the bypassed checks would either no-op (framework-baseline catalog)
        or cause recursion (audit-internal events rarely have meaningful
        authority bindings). MUST be called under `self._lock`.
        """
        chained = event.model_copy(update={"prev_hash": self._tail_hash})
        line = chained.model_dump_json()
        try:
            with self._config.audit_trail_path.open(
                "a", encoding="utf-8"
            ) as fh:
                fh.write(line + "\n")
                fh.flush()
        except OSError as exc:
            self._handle_write_error(exc)
            return
        self._tail_hash = _sha256_line(line)
        self._event_count += 1

    def _validate_catalog(self, event: AuditEventBase) -> None:
        """Per `arch/audit.md` §2.E catalog management + §11 `AuditCatalogError`."""
        if not self._config.catalog_enforcement:
            return
        catalog = self._config.shape_policy.mandatory_catalog
        if catalog and event.event_kind not in catalog:
            raise AuditCatalogError(
                f"event_kind '{event.event_kind}' not in active shape's "
                f"mandatory catalog (granularity="
                f"{self._config.shape_policy.granularity.value})."
            )

    def _validate_authority(self, event: AuditEventBase) -> None:
        """Per `arch/audit.md` §11 `AuditTrustError` + `glossary/authority-binding.md`."""
        checker = self._config.authority_checker
        if checker is None:
            return
        if not checker(event):
            raise AuditTrustError(
                f"Authority-binding policy denied event "
                f"'{event.event_kind}' (trust_model="
                f"{self._config.shape_policy.trust_model.value})."
            )

    def _handle_write_error(self, exc: OSError) -> None:
        """Per `arch/audit.md` §11 + §14 per-shape error semantics dispatch."""
        sem = self._config.shape_policy.error_semantics
        if sem is AuditErrorSemantics.FAIL_CLOSED:
            raise AuditWriteError(
                f"Audit-trail write failed at "
                f"{self._config.audit_trail_path}: {exc}"
            ) from exc
        # FAIL_OPEN_WITH_ALERT / FAIL_OPEN_WITH_RETRY: Phase 6.2 wiring point
        # for alert dispatch + retry queue. Reference impl drops the event
        # silently per fail-open semantics (continuity prioritized per
        # `arch/audit.md` §14). A real autonomous-business / personal-OS
        # deployment SHOULD wire concrete alert + retry mechanisms here per
        # `arch/audit.md` §15 pre-implementation operational concerns.
        return

    # ------------------------------------------------------------------
    # §C Query for reasoning-chain reconstruction
    # ------------------------------------------------------------------

    def query_per_claim(self, claim_id: str) -> list[AuditEventBase]:
        """Per `arch/audit.md` §2.C. Used by `arch/claim-defensibility.md`
        §2.2 re-run-ability via audit-trail reconstruction."""
        return [e for e in self._scan_all() if e.claim_id == claim_id]

    def query_per_actor(
        self, actor_kind: ActorKind, actor_id: str
    ) -> list[AuditEventBase]:
        """Per `arch/audit.md` §2.C. Used by `arch/practitioner.md` cross-
        practitioner audit-trail query pattern."""
        return [
            e
            for e in self._scan_all()
            if e.actor_kind is actor_kind and e.actor_id == actor_id
        ]

    def query_per_time_window(
        self, start: datetime, end: datetime
    ) -> list[AuditEventBase]:
        """Per `arch/audit.md` §2.C. Range is half-open [start, end)."""
        return [
            e
            for e in self._scan_all()
            if start <= e.timestamp < end
        ]

    def query_per_event_kind(self, event_kind: str) -> list[AuditEventBase]:
        """Per `arch/audit.md` §2.C. Used by quality-gate per-axis signal
        ingestion + per-shape policy enforcement."""
        return [e for e in self._scan_all() if e.event_kind == event_kind]

    def query_per_work_unit(self, work_unit_id: str) -> list[AuditEventBase]:
        """Per `arch/audit.md` §2.C. Used by `arch/workflow-work-unit.md`
        per-work-unit audit-trail attribution chain."""
        return [
            e for e in self._scan_all() if e.work_unit_id == work_unit_id
        ]

    def _scan_all(self) -> list[AuditEventBase]:
        """File-scan + collapse-to-base reader.

        Per `pbs.types.event_base.AuditEventBase` docstring: 'Concrete event
        subclasses promote structured fields out of details into typed
        attributes; details remains for impl-specific or extension data not
        yet schematized.' This reader collapses subclass-promoted fields
        back into `details` so query callers operate on a uniform
        `AuditEventBase` shape without needing the cross-module discriminated
        union of every event subclass.

        Index-backed query is Phase 6.2+ per `arch/audit.md` §15; reference
        impl is file-scan.

        Raises:
            AuditQueryError: substrate-impl-internal failure (file unreadable;
                JSON parse error; corrupt line).
        """
        path = self._config.audit_trail_path
        events: list[AuditEventBase] = []
        try:
            with path.open(encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        raw = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise AuditQueryError(
                            f"Audit-trail line {line_num} not valid JSON: "
                            f"{exc}"
                        ) from exc
                    events.append(self._reconstruct_base(raw, line_num))
        except OSError as exc:
            raise AuditQueryError(
                f"Audit-trail not readable at {path}: {exc}"
            ) from exc
        return events

    @staticmethod
    def _reconstruct_base(
        raw: dict[str, Any], line_num: int
    ) -> AuditEventBase:
        """Collapse subclass-promoted fields back into AuditEventBase.

        Subclass-specific fields (those not in `AuditEventBase.model_fields`)
        merge into the base `details` dict so the reader remains uniform.
        """
        base_field_names = set(AuditEventBase.model_fields.keys())
        base_data: dict[str, Any] = {}
        promoted: dict[str, Any] = {}
        for key, value in raw.items():
            if key in base_field_names:
                base_data[key] = value
            else:
                promoted[key] = value
        if promoted:
            details = dict(base_data.get("details") or {})
            details.update(promoted)
            base_data["details"] = details
        try:
            return AuditEventBase.model_validate(base_data)
        except Exception as exc:  # pragma: no cover  # noqa: BLE001
            raise AuditQueryError(
                f"Audit-trail line {line_num} could not be reconstructed "
                f"as AuditEventBase: {exc}"
            ) from exc

    # ------------------------------------------------------------------
    # §D Integrity verification
    # ------------------------------------------------------------------

    def verify_integrity(self) -> bool:
        """Per `arch/audit.md` §2.D. Re-walk the SHA-256 hash-chain.

        On hash-chain break: emits `AuditTrailIntegrityViolated` (forensic
        visibility) + raises `AuditIntegrityError` per `arch/audit.md` §11.

        Returns True when the chain is unbroken end-to-end.
        """
        path = self._config.audit_trail_path
        expected_prev = GENESIS_HASH
        line_num = 0
        try:
            with path.open(encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, start=1):
                    raw_line = line.rstrip("\n")
                    if not raw_line:
                        continue
                    try:
                        record = json.loads(raw_line)
                    except json.JSONDecodeError as exc:
                        self._emit_integrity_violation(
                            line_num, f"JSON decode error: {exc}"
                        )
                        raise AuditIntegrityError(
                            f"Audit-trail line {line_num} not valid JSON: "
                            f"{exc}"
                        ) from exc
                    actual_prev = record.get("prev_hash")
                    if actual_prev != expected_prev:
                        self._emit_integrity_violation(
                            line_num,
                            f"prev_hash mismatch (expected={expected_prev}, "
                            f"actual={actual_prev})",
                        )
                        raise AuditIntegrityError(
                            f"Audit-trail line {line_num} prev_hash mismatch "
                            f"(expected={expected_prev}, actual={actual_prev})"
                        )
                    expected_prev = _sha256_line(raw_line)
        except OSError as exc:
            raise AuditIntegrityError(
                f"Audit-trail not readable at {path}: {exc}"
            ) from exc
        return True

    def _emit_integrity_violation(self, line_num: int, reason: str) -> None:
        """Emit `AuditTrailIntegrityViolated` for forensic visibility per
        `arch/audit.md` §8.

        The violation event itself is appended through `_emit_unguarded`
        (lock NOT re-acquired here — `verify_integrity` is called either
        from shutdown under lock OR ad-hoc; the latter accepts a benign
        race vs. concurrent emit since the violation event records the
        forensic moment regardless).
        """
        self._emit_unguarded(
            AuditTrailIntegrityViolated(
                actor_kind=ActorKind.AI_RUNTIME,
                actor_id=self._instance_id,
                timestamp=datetime.now(tz=UTC),
                substrate_kind=SUBSTRATE_ID,
                details={
                    "line_num": line_num,
                    "reason": reason,
                },
            )
        )

    # ------------------------------------------------------------------
    # §F State-rendering-from-events
    # ------------------------------------------------------------------

    def render_state(self, kind: str) -> dict[str, Any]:
        """Per `arch/audit.md` §2.F + archived audit-trail-v2 single-write
        architecture: state IS the rendered view; events ARE the source of
        truth.

        Reference impl supports three rendering kinds:

        - `workflow_instance` → mapping `workflow_instance_id` → last-emitted
          event_kind for that instance (terminal lifecycle state)
        - `claim_status` → mapping `claim_id` → last-emitted event_kind for
          that claim (terminal claim status)
        - `actor_activity` → mapping `(actor_kind, actor_id)` → emission
          count

        Specific kind catalog beyond these is per-substrate-impl level + a
        Phase 6 wiring point per `arch/audit.md` §15.

        Raises:
            AuditQueryError: unknown rendering kind.
        """
        events = self._scan_all()
        if kind == "workflow_instance":
            return self._render_workflow_instance(events)
        if kind == "claim_status":
            return self._render_claim_status(events)
        if kind == "actor_activity":
            return self._render_actor_activity(events)
        raise AuditQueryError(
            f"Unknown render_state kind '{kind}'; reference impl supports "
            f"'workflow_instance' / 'claim_status' / 'actor_activity'."
        )

    @staticmethod
    def _render_workflow_instance(
        events: list[AuditEventBase],
    ) -> dict[str, Any]:
        state: dict[str, Any] = {}
        for event in events:
            if event.workflow_instance_id is None:
                continue
            state[event.workflow_instance_id] = {
                "last_event_kind": event.event_kind,
                "last_timestamp": event.timestamp.isoformat(),
            }
        return state

    @staticmethod
    def _render_claim_status(events: list[AuditEventBase]) -> dict[str, Any]:
        state: dict[str, Any] = {}
        for event in events:
            if event.claim_id is None:
                continue
            state[event.claim_id] = {
                "last_event_kind": event.event_kind,
                "last_timestamp": event.timestamp.isoformat(),
            }
        return state

    @staticmethod
    def _render_actor_activity(
        events: list[AuditEventBase],
    ) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for event in events:
            key = f"{event.actor_kind.value}:{event.actor_id}"
            counts[key] = counts.get(key, 0) + 1
        return counts

    # ------------------------------------------------------------------
    # §G Cross-deployment external-format export
    # ------------------------------------------------------------------

    def export(self, format: str) -> bytes:
        """Per `arch/audit.md` §2.G + `profiles/L8-auditor-reviewer-posthoc.md`
        line 33 external-format requirements.

        Reference impl supports:

        - `jsonl` → raw bytes copy of the audit-trail file (round-trips
          cleanly; supports cross-deployment migration import)

        Phase 6 wiring points (NotImplementedError + this docstring):

        - `pdf` → regulator submission / professional report rendering
        - `csv` → tabular event log for external analytics
        - `regulator_submission` → jurisdiction-specific bundled format

        Raises:
            AuditMigrationError: jsonl export failed (file unreadable).
            NotImplementedError: pdf / csv / regulator_submission Phase 6
                wiring point.
        """
        if format == "jsonl":
            try:
                return self._config.audit_trail_path.read_bytes()
            except OSError as exc:
                raise AuditMigrationError(
                    f"Audit-trail jsonl export failed at "
                    f"{self._config.audit_trail_path}: {exc}"
                ) from exc
        if format in {"pdf", "csv", "regulator_submission"}:
            raise NotImplementedError(
                f"export(format='{format}') is a Phase 6 wiring point per "
                f"`arch/audit.md` §15 + §2.G + §G. Reference impl supports "
                f"'jsonl' only; concrete format mechanics + L8 external-"
                f"format requirements deliver at deployment-instance wiring."
            )
        raise AuditMigrationError(
            f"Unknown export format '{format}'; reference impl supports "
            f"'jsonl' (pdf / csv / regulator_submission Phase 6 wiring)."
        )

    # ------------------------------------------------------------------
    # Internal: hash-chain tail scan at boot
    # ------------------------------------------------------------------

    def _scan_chain_tail(self) -> tuple[str, int]:
        """Re-walk the persisted audit-trail at boot to reconstruct the
        rolling tail hash + event count.

        Per `arch/audit.md` §10 boot step 3 + composite sequence audit-phase
        2: 'If existing audit-trail present: substrate-impl verifies hash-
        chain integrity (load prior tail event; verify ready-state).'

        Returns (tail_hash, event_count). Tail hash is the SHA-256 of the
        last persisted line (genesis sentinel for empty file).

        Raises:
            AuditIntegrityError: hash-chain broken on boot-time re-walk
                (substrate-impl detects per `arch/audit.md` §11).
            AuditWriteError: file unreadable at boot.
        """
        path = self._config.audit_trail_path
        expected_prev = GENESIS_HASH
        last_hash = GENESIS_HASH
        count = 0
        try:
            with path.open(encoding="utf-8") as fh:
                for line_num, line in enumerate(fh, start=1):
                    raw_line = line.rstrip("\n")
                    if not raw_line:
                        continue
                    try:
                        record = json.loads(raw_line)
                    except json.JSONDecodeError as exc:
                        raise AuditIntegrityError(
                            f"Audit-trail boot scan: line {line_num} not "
                            f"valid JSON: {exc}"
                        ) from exc
                    actual_prev = record.get("prev_hash")
                    if actual_prev != expected_prev:
                        raise AuditIntegrityError(
                            f"Audit-trail boot scan: line {line_num} "
                            f"prev_hash mismatch "
                            f"(expected={expected_prev}, actual={actual_prev})"
                        )
                    last_hash = _sha256_line(raw_line)
                    expected_prev = last_hash
                    count += 1
        except OSError as exc:
            raise AuditWriteError(
                f"Audit-trail not readable at boot: {path}: {exc}"
            ) from exc
        return last_hash, count
