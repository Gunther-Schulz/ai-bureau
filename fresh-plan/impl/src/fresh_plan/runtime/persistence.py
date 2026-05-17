"""Per-workspace JSONL persistence layer (Phase C C2 — D70 §B).

Per D68 §B.2 (Phase C persistence-layer setup decision): each workspace's
event chain persists as one append-only JSONL file (``events.jsonl``);
one JSON-encoded event per UTF-8 line; chain replay reconstructs full
state per D39 + D40 §A. Boot loads the file, replays events through the
substrate's ``append_event`` integrity gate, then activates D54 §B.2
``classify_shape_change`` (resolves D54 §D D-1 boot-integration) + D58
§B.1 lifecycle-derivation reconciliation (resolves D58 §C wiring).

Per-workspace layout under ``<persistence-root>/<workspace-id>/``:

  - ``events.jsonl`` — append-only event log (one JSON object per line).
  - ``last-boot-manifest.json`` — atomic-overwrite snapshot of the
    most-recent successful boot's manifest. Provides the prior shape spec
    for ``classify_shape_change`` (per D61 the composition-change
    ``binding-kind`` enum excludes ``shape``, so prior shape cannot be
    recovered from the event chain alone — separate snapshot required).

Persistence-root default ``./.fresh-plan-state/`` (cwd-relative) per
Python convention; override via
``workspace.composition.substrate-bindings[0].configuration.persistence-root``
per D57 §B.1 opaque pass-through.

Failure mode (D70 §B per D45 standing triad):

  - **Detection** — IO error / JSON parse error / partial-line in
    ``events.jsonl`` → ``PersistenceCorruptionError``.
  - **Surface** — boot.py wraps as ``WorkspaceBootError(category=
    'persistence-corruption')`` with the original exception chained via
    Python's ``from`` clause (full traceback visibility).
  - **Recovery** — caller catches ``WorkspaceBootError``, inspects
    failure category, decides whether to fix the file state OR delete
    the persistence directory for a fresh-start boot. Substrate is not
    constructed when corruption surfaces.

Scope cuts (per D70 §D):

  - **Snapshot caching** deferred per D58 §D D-5 — Phase C uses full
    chain replay on every boot (deterministic; replay-cost framing
    acceptable for Phase C reference-impl scale).
  - **Cross-platform durability** — Phase C scope is POSIX append
    atomicity (Linux + macOS). Windows + fsync-per-append deferred to
    Phase D or later if pioneer-instance needs them.
  - **Schema evolution across sessions** — Phase-C-bounded assumption
    that event.schema.json doesn't evolve mid-Phase-C; if persisted
    events fail schema on replay, the corruption category catches it.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator, Optional


# Default persistence-root: cwd-relative dotted directory per Python convention.
# Override via composition.substrate-bindings[0].configuration.persistence-root
# per D57 §B.1 opaque pass-through.
DEFAULT_PERSISTENCE_ROOT = "./.fresh-plan-state"

# File name conventions; load-bearing at module boundary.
EVENTS_FILE = "events.jsonl"
MANIFEST_SNAPSHOT_FILE = "last-boot-manifest.json"
# Per D76 §C: AEGIS integrity-records persist parallel to events.jsonl,
# one record per event line. File name re-exported from runtime.integrity
# for boot.py + tests; defined here as the canonical persistence-layer
# constant to keep file-layout knowledge in one module.
INTEGRITY_RECORDS_FILE = "events.integrity.jsonl"


class PersistenceCorruptionError(Exception):
    """File IO or JSON-parse failure during persistence read/write.

    Per D70 §B.1 detection-surface-recovery triad:

      - **Detection** — IO error (permission denied, file vanished mid-read)
        OR JSON parse error (malformed line; partial-line from a torn
        append) during ``load_chain`` / ``load_manifest_snapshot``.
      - **Surface** — raised with structured fields (``path`` + ``reason``
        + optional ``line_number`` for events.jsonl parse errors).
        ``boot.py`` catches and wraps as ``WorkspaceBootError(category=
        'persistence-corruption')`` per D45 + D46 pattern.
      - **Recovery** — caller resolves underlying file state OR deletes
        the persistence directory for a fresh-start boot. Substrate not
        constructed when corruption surfaces.
    """

    def __init__(
        self,
        *,
        path: str,
        reason: str,
        line_number: Optional[int] = None,
    ) -> None:
        self.path = path
        self.reason = reason
        self.line_number = line_number
        loc = f" (line {line_number})" if line_number is not None else ""
        super().__init__(f"persistence corruption at {path!r}{loc}: {reason}")


@dataclass
class PersistenceLayer:
    """Stateless service over per-workspace JSONL file I/O (D70 §B).

    Owns nothing in-memory beyond its configuration (root + workspace_id).
    Each method is a separate file operation; failures raise
    ``PersistenceCorruptionError`` which boot.py wraps per D70 §B.1.

    Per D68 §B.2 + D10 append-only chain discipline:

      - ``save_event`` appends one JSON line to events.jsonl (POSIX append).
      - ``load_chain`` reads events.jsonl line-by-line, yielding event dicts.
      - ``save_manifest_snapshot`` writes last-boot-manifest.json via
        atomic-rename (write-temp + os.replace) so a partial write never
        leaves the canonical file corrupted.
      - ``load_manifest_snapshot`` reads last-boot-manifest.json or
        returns None when absent (cold start).
    """

    persistence_root: str
    workspace_id: str

    # Cached resolved paths; computed once at __post_init__.
    workspace_dir: Path = field(init=False)
    events_path: Path = field(init=False)
    manifest_snapshot_path: Path = field(init=False)
    integrity_records_path: Path = field(init=False)

    # Per D76 §B Phase C C8: optional AEGIS-style integrity protocol. When
    # set, save_event also stamps + persists an IntegrityRecord to
    # events.integrity.jsonl (parallel-line discipline). None for tests
    # that don't exercise integrity-stamping.
    # Field is dataclass-Optional[object] not Optional[IntegrityProtocol]
    # to avoid an import cycle between persistence.py + integrity.py.
    integrity_protocol: Optional[object] = None
    # Tracks the most recent stamped hash bytes for chain continuity at
    # save_event time. Loaded from prior integrity records on first call
    # when chain is non-empty.
    _last_integrity_hash: Optional[bytes] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        # Resolve workspace_dir but do NOT create it yet — directory
        # creation is on-write (save_event / save_manifest_snapshot).
        self.workspace_dir = Path(self.persistence_root) / self.workspace_id
        self.events_path = self.workspace_dir / EVENTS_FILE
        self.manifest_snapshot_path = self.workspace_dir / MANIFEST_SNAPSHOT_FILE
        self.integrity_records_path = self.workspace_dir / INTEGRITY_RECORDS_FILE

    # -----------------------------------------------------------------
    # Cold-start detection
    # -----------------------------------------------------------------

    def has_events(self) -> bool:
        """True when events.jsonl exists (non-empty OR empty file)."""
        return self.events_path.exists()

    def has_manifest_snapshot(self) -> bool:
        """True when last-boot-manifest.json exists."""
        return self.manifest_snapshot_path.exists()

    # -----------------------------------------------------------------
    # Event chain — append-only writes + line-by-line replay reads
    # -----------------------------------------------------------------

    def save_event(self, event: dict) -> None:
        """Append one JSON-encoded event to events.jsonl (D70 §B).

        Uses POSIX append (``open(path, 'a')``) — atomic up to PIPE_BUF
        (4KB on Linux) for Phase C event sizes (well under). flush+close
        per append; fsync deferred per D70 §D.

        Creates workspace_dir on first write. JSON-encoding failure
        (non-serializable event content) propagates as ``TypeError``
        from json.dumps — caller's bug, not a persistence bug.
        """
        try:
            self.workspace_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.workspace_dir),
                reason=f"failed to create workspace persistence directory: {exc}",
            ) from exc

        try:
            line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        except TypeError as exc:
            # Non-serializable event content — propagate as IO-level corruption
            # (caller emitted an event the chain accepted but JSON refused).
            raise PersistenceCorruptionError(
                path=str(self.events_path),
                reason=f"event not JSON-serializable: {exc}",
            ) from exc

        try:
            with open(self.events_path, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
                fh.flush()
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.events_path),
                reason=f"failed to append event to JSONL: {exc}",
            ) from exc

        # Per D76 §B Phase C C8: when an integrity protocol is attached,
        # stamp the event + persist the IntegrityRecord to
        # events.integrity.jsonl. Failure to stamp surfaces as
        # PersistenceCorruptionError (the events.jsonl write already
        # committed; the integrity-records file is now inconsistent
        # with the chain — caller must surface to operator).
        if self.integrity_protocol is not None:
            try:
                record = self.integrity_protocol.stamp(  # type: ignore[attr-defined]
                    event, self._last_integrity_hash
                )
            except Exception as exc:
                raise PersistenceCorruptionError(
                    path=str(self.integrity_records_path),
                    reason=(
                        f"integrity protocol failed to stamp event: {exc}"
                    ),
                ) from exc

            # Sequence position = current line count of the integrity file.
            # On first stamp the file does not yet exist → sequence 0.
            try:
                if self.integrity_records_path.exists():
                    with open(
                        self.integrity_records_path, "r", encoding="utf-8"
                    ) as fh:
                        existing_count = sum(1 for line in fh if line.strip())
                else:
                    existing_count = 0
            except OSError as exc:
                raise PersistenceCorruptionError(
                    path=str(self.integrity_records_path),
                    reason=(
                        f"failed to read integrity records for sequence "
                        f"derivation: {exc}"
                    ),
                ) from exc

            # Re-assemble with the correct sequence (stamp returns -1).
            from dataclasses import replace

            record = replace(record, sequence=existing_count)

            # Update cached prior hash for the next event in the chain.
            self._last_integrity_hash = bytes.fromhex(record.hash)

            try:
                payload = json.dumps(
                    record.to_jsonl(),
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            except TypeError as exc:
                raise PersistenceCorruptionError(
                    path=str(self.integrity_records_path),
                    reason=(
                        f"integrity record not JSON-serializable: {exc}"
                    ),
                ) from exc

            try:
                with open(
                    self.integrity_records_path, "a", encoding="utf-8"
                ) as fh:
                    fh.write(payload + "\n")
                    fh.flush()
            except OSError as exc:
                raise PersistenceCorruptionError(
                    path=str(self.integrity_records_path),
                    reason=(
                        f"failed to append integrity record to JSONL: {exc}"
                    ),
                ) from exc

    def has_integrity_records(self) -> bool:
        """True when events.integrity.jsonl exists (per D76 §B Phase C C8)."""
        return self.integrity_records_path.exists()

    def prime_integrity_state(self) -> None:
        """Initialize _last_integrity_hash from the latest persisted record.

        Per D76 §B Phase C C8: when boot replays a prior chain that was
        integrity-stamped, subsequent events appended on this boot must
        chain off the last persisted record's hash (not the bootstrap
        hash). Caller (boot.py) invokes once after attaching the integrity
        protocol + before any new events are appended.

        No-op when events.integrity.jsonl is absent (cold start).
        """
        if not self.integrity_records_path.exists():
            return
        last_hash: Optional[str] = None
        try:
            with open(
                self.integrity_records_path, "r", encoding="utf-8"
            ) as fh:
                for line in fh:
                    stripped = line.strip()
                    if not stripped:
                        continue
                    try:
                        obj = json.loads(stripped)
                    except json.JSONDecodeError as exc:
                        raise PersistenceCorruptionError(
                            path=str(self.integrity_records_path),
                            reason=(
                                f"malformed JSON priming integrity state: {exc}"
                            ),
                        ) from exc
                    if isinstance(obj, dict) and "hash" in obj:
                        last_hash = obj["hash"]
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.integrity_records_path),
                reason=(
                    f"failed to prime integrity state from records file: {exc}"
                ),
            ) from exc
        if last_hash is not None:
            try:
                self._last_integrity_hash = bytes.fromhex(last_hash)
            except ValueError as exc:
                raise PersistenceCorruptionError(
                    path=str(self.integrity_records_path),
                    reason=(
                        f"latest integrity record has non-hex hash field: {exc}"
                    ),
                ) from exc

    def load_integrity_records(self) -> Iterator[dict]:
        """Yield integrity records from events.integrity.jsonl in append order.

        Each record is a raw dict (caller wraps via
        ``IntegrityRecord.from_jsonl`` if a typed object is needed). Empty
        iterator when the file is absent (cold start or no integrity
        protocol was ever attached).

        Parse failures (malformed JSON / non-object line) raise
        ``PersistenceCorruptionError`` symmetrically with load_chain.
        """
        if not self.integrity_records_path.exists():
            return iter([])

        try:
            handle = open(
                self.integrity_records_path, "r", encoding="utf-8"
            )
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.integrity_records_path),
                reason=(
                    f"failed to open integrity records for read: {exc}"
                ),
            ) from exc

        def _iter_records() -> Iterator[dict]:
            try:
                for line_number, raw in enumerate(handle, start=1):
                    stripped = raw.rstrip("\n").rstrip("\r")
                    if not stripped:
                        continue
                    try:
                        record = json.loads(stripped)
                    except json.JSONDecodeError as exc:
                        raise PersistenceCorruptionError(
                            path=str(self.integrity_records_path),
                            reason=(
                                f"malformed JSON in integrity records: {exc}"
                            ),
                            line_number=line_number,
                        ) from exc
                    if not isinstance(record, dict):
                        raise PersistenceCorruptionError(
                            path=str(self.integrity_records_path),
                            reason=(
                                f"integrity record line is JSON but not an "
                                f"object (got {type(record).__name__})"
                            ),
                            line_number=line_number,
                        )
                    yield record
            finally:
                handle.close()

        return _iter_records()

    def load_chain(self) -> Iterator[dict]:
        """Yield events from events.jsonl in append order (D70 §B replay).

        Returns iterator (not list) so callers can stream replay without
        loading entire chain into memory. Each line is JSON-parsed; parse
        failure on any line raises ``PersistenceCorruptionError`` with the
        offending line_number (1-indexed). Partial-line at EOF (torn
        append) surfaces as JSON parse error on the final line.

        Returns empty iterator when events.jsonl is absent (cold start).
        """
        if not self.events_path.exists():
            return iter([])

        try:
            handle = open(self.events_path, "r", encoding="utf-8")
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.events_path),
                reason=f"failed to open events.jsonl for read: {exc}",
            ) from exc

        def _iter_events() -> Iterator[dict]:
            try:
                for line_number, raw in enumerate(handle, start=1):
                    stripped = raw.rstrip("\n").rstrip("\r")
                    if not stripped:
                        # Skip blank lines defensively (POSIX append-only
                        # discipline should never produce them, but a
                        # mid-append crash could leave one at EOF).
                        continue
                    try:
                        event = json.loads(stripped)
                    except json.JSONDecodeError as exc:
                        raise PersistenceCorruptionError(
                            path=str(self.events_path),
                            reason=f"malformed JSON in events.jsonl: {exc}",
                            line_number=line_number,
                        ) from exc
                    if not isinstance(event, dict):
                        raise PersistenceCorruptionError(
                            path=str(self.events_path),
                            reason=(
                                f"events.jsonl line is JSON but not an object "
                                f"(got {type(event).__name__})"
                            ),
                            line_number=line_number,
                        )
                    yield event
            finally:
                handle.close()

        return _iter_events()

    # -----------------------------------------------------------------
    # Manifest snapshot — atomic-rename overwrites (D54 §B.2 boot input)
    # -----------------------------------------------------------------

    def save_manifest_snapshot(self, manifest: dict) -> None:
        """Atomically overwrite last-boot-manifest.json (D70 §B + D54 §B.2).

        Write-temp + os.replace pattern guarantees the canonical file is
        either the prior version OR the new version, never a partial
        write. Used by boot.py after successful boot completes — captures
        the manifest whose shape spec backed this chain's events.

        Per D61 the composition-change ``binding-kind`` enum deliberately
        excludes ``shape``; prior shape cannot be recovered from the event
        chain alone. This snapshot supplies the prior shape spec to
        D54's ``classify_shape_change`` on subsequent boots.
        """
        try:
            self.workspace_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.workspace_dir),
                reason=f"failed to create workspace persistence directory: {exc}",
            ) from exc

        try:
            payload = json.dumps(
                manifest, ensure_ascii=False, indent=2, sort_keys=True
            )
        except TypeError as exc:
            raise PersistenceCorruptionError(
                path=str(self.manifest_snapshot_path),
                reason=f"manifest not JSON-serializable: {exc}",
            ) from exc

        tmp_path = self.manifest_snapshot_path.with_suffix(".json.tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as fh:
                fh.write(payload)
                fh.flush()
            os.replace(tmp_path, self.manifest_snapshot_path)
        except OSError as exc:
            # Best-effort cleanup of tmp file; ignore secondary failures.
            try:
                tmp_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise PersistenceCorruptionError(
                path=str(self.manifest_snapshot_path),
                reason=f"failed to write manifest snapshot: {exc}",
            ) from exc

    def load_manifest_snapshot(self) -> Optional[dict]:
        """Read last-boot-manifest.json, or None when absent (cold start).

        Parse failure raises ``PersistenceCorruptionError`` (the file
        exists but is unreadable — caller cannot safely proceed with
        ``classify_shape_change`` against an unknown prior).
        """
        if not self.manifest_snapshot_path.exists():
            return None
        try:
            with open(self.manifest_snapshot_path, "r", encoding="utf-8") as fh:
                content = fh.read()
        except OSError as exc:
            raise PersistenceCorruptionError(
                path=str(self.manifest_snapshot_path),
                reason=f"failed to read manifest snapshot: {exc}",
            ) from exc
        try:
            manifest = json.loads(content)
        except json.JSONDecodeError as exc:
            raise PersistenceCorruptionError(
                path=str(self.manifest_snapshot_path),
                reason=f"malformed JSON in manifest snapshot: {exc}",
            ) from exc
        if not isinstance(manifest, dict):
            raise PersistenceCorruptionError(
                path=str(self.manifest_snapshot_path),
                reason=(
                    f"manifest snapshot is JSON but not an object "
                    f"(got {type(manifest).__name__})"
                ),
            )
        return manifest
