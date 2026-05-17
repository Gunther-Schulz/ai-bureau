"""Tests for Phase C C8 AEGIS integrity protocol (D76 §B; activates D40 §B).

Covers per the tracker test pattern:
  1. happy-path round-trip: 5+ events → save+stamp → load+verify → no failures
  2. tampered event content → ValidationFailure(detail.subcase='hash-mismatch')
  3. tampered signature → ValidationFailure(detail.subcase='signature-invalid')
  4. missing integrity record → ValidationFailure(detail.subcase='missing-record')
  5. boot with configured integrity-protocol + clean chain → boot succeeds
  6. boot with configured integrity-protocol + tampered chain →
     WorkspaceBootError(category='integrity-violation')
  7. boot without configured integrity-protocol → no integrity check, boots
  8. key bootstrap: first event triggers keypair generation + persistence

Per scope-cut C12: tests use pytest tmp_path fixtures for filesystem
isolation; no real KMS/HSM; mockable test scope only.
"""
from __future__ import annotations

import base64
import copy
import json
from pathlib import Path

import pytest

from fresh_plan.runtime import (
    AEGISIntegrityProtocol,
    IntegrityProtocol,
    IntegrityRecord,
    PersistenceLayer,
    Workspace,
    WorkspaceBootError,
    generate_aegis_keypair,
    load_or_create_aegis_keypair,
)
from fresh_plan.runtime.persistence import INTEGRITY_RECORDS_FILE


# Fixture pointers per existing test conventions.
IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
END_TO_END_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-end-to-end"
)


def _load_e2e_manifest_with_integrity(
    tmp_path: Path, integrity_protocol: str | None = None
) -> dict:
    """Load workspace-end-to-end manifest + inject persistence-root +
    optionally integrity-protocol config."""
    manifest = json.loads(
        (END_TO_END_FIXTURE / "workspace.json").read_text()
    )
    manifest = copy.deepcopy(manifest)
    bindings = manifest["composition"]["substrate-bindings"]
    bindings[0].setdefault("configuration", {})
    bindings[0]["configuration"]["persistence-root"] = str(tmp_path)
    if integrity_protocol is not None:
        bindings[0]["configuration"]["integrity-protocol"] = integrity_protocol
    return manifest


# ---------------------------------------------------------------------------
# 1. IntegrityProtocol abstract base — IntegrityProtocol is a subclass shape
# ---------------------------------------------------------------------------


def test_aegis_is_integrity_protocol_subclass() -> None:
    """D40 §B: AEGISIntegrityProtocol extends IntegrityProtocol abstract base.

    Future protocols (Axon / PROV-O / post-quantum) plug in via the same
    abstract; this test pins the inheritance contract.
    """
    priv, _ = generate_aegis_keypair()
    aegis = AEGISIntegrityProtocol(private_key=priv, workspace_id="test-ws")
    assert isinstance(aegis, IntegrityProtocol)
    assert (
        aegis.identifier
        == "aegis-protocol-ext:aegis-event-chain-integrity"
    )


# ---------------------------------------------------------------------------
# 2. Happy-path round-trip
# ---------------------------------------------------------------------------


def test_aegis_happy_path_roundtrip_5_events(tmp_path: Path) -> None:
    """D76 §B closure (g): stamp 5 events → verify → no failures.

    Standalone PersistenceLayer + AEGISIntegrityProtocol exercise — no
    boot.py + no workspace; isolates the protocol surface from runtime
    glue.
    """
    priv, pub = generate_aegis_keypair()
    aegis = AEGISIntegrityProtocol(
        private_key=priv, workspace_id="aegis-happy-ws"
    )

    layer = PersistenceLayer(
        persistence_root=str(tmp_path),
        workspace_id="aegis-happy-ws",
        integrity_protocol=aegis,
    )

    events = [
        {"id": f"evt-{i}", "payload-subtype": "claim", "seq": i}
        for i in range(5)
    ]
    for evt in events:
        layer.save_event(evt)

    # Round-trip read
    loaded_events = list(layer.load_chain())
    record_dicts = list(layer.load_integrity_records())
    records = [IntegrityRecord.from_jsonl(r) for r in record_dicts]

    assert loaded_events == events
    assert len(records) == 5
    # Sequence is 0-indexed contiguous
    assert [r.sequence for r in records] == list(range(5))
    # Each record's event_id matches its event
    for i, r in enumerate(records):
        assert r.event_id == f"evt-{i}"

    # Verify — clean chain → no failures
    failures = aegis.verify(loaded_events, records, pub)
    assert failures == [], (
        f"clean chain should verify; got {len(failures)} failures: "
        f"{[f.reason for f in failures]}"
    )


# ---------------------------------------------------------------------------
# 3. Tampered event content → hash-mismatch
# ---------------------------------------------------------------------------


def test_aegis_tampered_event_content_surfaces_hash_mismatch(
    tmp_path: Path,
) -> None:
    """D76 §B.1 detection: event content modified after stamping →
    AEGISIntegrityProtocol.verify returns ValidationFailure with
    detail.subcase='hash-mismatch'."""
    priv, pub = generate_aegis_keypair()
    aegis = AEGISIntegrityProtocol(
        private_key=priv, workspace_id="tampered-content-ws"
    )

    layer = PersistenceLayer(
        persistence_root=str(tmp_path),
        workspace_id="tampered-content-ws",
        integrity_protocol=aegis,
    )

    for i in range(3):
        layer.save_event(
            {"id": f"evt-{i}", "payload-subtype": "claim", "value": i}
        )

    loaded_events = list(layer.load_chain())
    records = [
        IntegrityRecord.from_jsonl(r) for r in layer.load_integrity_records()
    ]

    # Tamper: modify event content (sub-case: middle event)
    tampered = list(loaded_events)
    tampered[1] = {**loaded_events[1], "value": 99}  # changed from 1 → 99

    failures = aegis.verify(tampered, records, pub)
    assert len(failures) == 1
    assert failures[0].category == "integrity-violation"
    assert "subcase=hash-mismatch" in failures[0].reason
    assert "evt-1" in failures[0].reason


# ---------------------------------------------------------------------------
# 4. Tampered signature → signature-invalid
# ---------------------------------------------------------------------------


def test_aegis_tampered_signature_surfaces_signature_invalid(
    tmp_path: Path,
) -> None:
    """D76 §B.1 detection: integrity record's signature corrupted →
    AEGISIntegrityProtocol.verify returns ValidationFailure with
    detail.subcase='signature-invalid'."""
    priv, pub = generate_aegis_keypair()
    aegis = AEGISIntegrityProtocol(
        private_key=priv, workspace_id="tampered-sig-ws"
    )

    layer = PersistenceLayer(
        persistence_root=str(tmp_path),
        workspace_id="tampered-sig-ws",
        integrity_protocol=aegis,
    )

    for i in range(3):
        layer.save_event({"id": f"evt-{i}", "payload-subtype": "claim"})

    loaded_events = list(layer.load_chain())
    records = [
        IntegrityRecord.from_jsonl(r) for r in layer.load_integrity_records()
    ]

    # Tamper: replace one record's signature with a base64-encoded all-zero
    # signature (right length, wrong contents). Hash stays correct so
    # hash-mismatch doesn't fire first.
    bogus_sig = base64.b64encode(b"\x00" * 64).decode("ascii")
    from dataclasses import replace
    records[2] = replace(records[2], signature=bogus_sig)

    failures = aegis.verify(loaded_events, records, pub)
    assert len(failures) == 1
    assert failures[0].category == "integrity-violation"
    assert "subcase=signature-invalid" in failures[0].reason
    assert "evt-2" in failures[0].reason


# ---------------------------------------------------------------------------
# 5. Missing integrity record → missing-record
# ---------------------------------------------------------------------------


def test_aegis_missing_record_surfaces_missing_record(tmp_path: Path) -> None:
    """D76 §B.1 detection: chain has N events but only N-1 integrity
    records → ValidationFailure with detail.subcase='missing-record'."""
    priv, pub = generate_aegis_keypair()
    aegis = AEGISIntegrityProtocol(
        private_key=priv, workspace_id="missing-rec-ws"
    )

    layer = PersistenceLayer(
        persistence_root=str(tmp_path),
        workspace_id="missing-rec-ws",
        integrity_protocol=aegis,
    )

    for i in range(3):
        layer.save_event({"id": f"evt-{i}", "payload-subtype": "claim"})

    loaded_events = list(layer.load_chain())
    records = [
        IntegrityRecord.from_jsonl(r) for r in layer.load_integrity_records()
    ]

    # Drop the last record (simulates truncated integrity file).
    truncated = records[:-1]

    failures = aegis.verify(loaded_events, truncated, pub)
    assert len(failures) == 1
    assert failures[0].category == "integrity-violation"
    assert "subcase=missing-record" in failures[0].reason
    assert "evt-2" in failures[0].reason


# ---------------------------------------------------------------------------
# 6. Boot with configured integrity-protocol + clean chain succeeds
# ---------------------------------------------------------------------------


def test_boot_with_integrity_protocol_clean_chain_succeeds(
    tmp_path: Path,
) -> None:
    """D76 §B + D70 §B + boot.py step 4.5+: when integrity-protocol is
    configured AND the persisted chain + records are self-consistent,
    boot proceeds normally."""
    manifest = _load_e2e_manifest_with_integrity(
        tmp_path,
        integrity_protocol="aegis-protocol-ext:aegis-event-chain-integrity",
    )

    # First boot — emit some events; integrity records get stamped.
    ws1 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        agent = ws1.actors["agent-primary"]
        agent.emit_claim("c1", role="author", confidence="high")
        agent.emit_action("act-1")
    finally:
        ws1.shutdown()  # Emits lifecycle-transition:shutdown event

    # Verify the integrity records file exists + is well-formed
    workspace_dir = tmp_path / manifest["id"]
    integrity_path = workspace_dir / INTEGRITY_RECORDS_FILE
    assert integrity_path.exists()
    events_path = workspace_dir / "events.jsonl"
    with open(events_path, "r", encoding="utf-8") as fh:
        event_lines = [line for line in fh if line.strip()]
    with open(integrity_path, "r", encoding="utf-8") as fh:
        record_lines = [line for line in fh if line.strip()]
    assert len(record_lines) == len(event_lines), (
        f"integrity records should match persisted events line-for-line; "
        f"events={len(event_lines)}, records={len(record_lines)}"
    )
    assert len(record_lines) >= 4  # 2 actor seeds + boot + claim + action + shutdown

    # Second boot — replays chain + verifies integrity; should succeed.
    ws2 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        # Boot succeeded → workspace handle constructed
        assert ws2.substrate.persistence is not None
        assert ws2.substrate.persistence.integrity_protocol is not None
        # State preserved across boot via integrity-checked replay
        assert "agent-primary" in ws2.substrate.state.actors
    finally:
        ws2.shutdown()


# ---------------------------------------------------------------------------
# 7. Boot with integrity-protocol + tampered chain → boot error
# ---------------------------------------------------------------------------


def test_boot_with_integrity_protocol_tampered_chain_raises_boot_error(
    tmp_path: Path,
) -> None:
    """D76 §B + D45 triad: tampered events.jsonl → boot replays the
    tampered chain → integrity verify fails → WorkspaceBootError(
    category='integrity-violation')."""
    manifest = _load_e2e_manifest_with_integrity(
        tmp_path,
        integrity_protocol="aegis-protocol-ext:aegis-event-chain-integrity",
    )

    # First boot — populate the chain + integrity records.
    ws1 = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        agent = ws1.actors["agent-primary"]
        agent.emit_claim("c1", role="author", confidence="high")
    finally:
        ws1.shutdown()

    # Tamper: rewrite events.jsonl with the claim event's content modified.
    # The integrity records still encode the ORIGINAL hash, so verify will
    # surface hash-mismatch on the tampered line.
    workspace_dir = tmp_path / manifest["id"]
    events_path = workspace_dir / "events.jsonl"
    lines = events_path.read_text().splitlines()
    # Locate the claim line + mutate its payload.assertion content.
    new_lines = []
    mutated = False
    for line in lines:
        if not line.strip():
            continue
        obj = json.loads(line)
        if (
            obj.get("payload-subtype") == "claim"
            and (obj.get("payload") or {}).get("assertion") == "c1"
            and not mutated
        ):
            obj["payload"]["assertion"] = "tampered-content"
            mutated = True
        new_lines.append(
            json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        )
    assert mutated, "test setup failure: no claim event found to tamper"
    events_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")

    # Second boot — should detect tampered chain.
    with pytest.raises(WorkspaceBootError) as excinfo:
        Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    assert any(
        f.category == "integrity-violation"
        for f in excinfo.value.failures
    ), (
        f"expected integrity-violation; got categories: "
        f"{[f.category for f in excinfo.value.failures]}"
    )


# ---------------------------------------------------------------------------
# 8. Boot WITHOUT integrity-protocol → no integrity check, boots normally
# ---------------------------------------------------------------------------


def test_boot_without_integrity_protocol_does_not_check(
    tmp_path: Path,
) -> None:
    """D76 §B: integrity protocol is OPT-IN per substrate-binding
    configuration. When omitted, boot proceeds with persistence only;
    no integrity stamping; no integrity-records file written."""
    manifest = _load_e2e_manifest_with_integrity(
        tmp_path, integrity_protocol=None
    )
    ws = Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    try:
        # Persistence attached
        assert ws.substrate.persistence is not None
        # Integrity protocol NOT attached
        assert ws.substrate.persistence.integrity_protocol is None
        # No integrity-records file should exist
        workspace_dir = tmp_path / manifest["id"]
        integrity_path = workspace_dir / INTEGRITY_RECORDS_FILE
        assert not integrity_path.exists()
    finally:
        ws.shutdown()


# ---------------------------------------------------------------------------
# 9. Key bootstrap: first save_event generates + persists Ed25519 keypair
# ---------------------------------------------------------------------------


def test_aegis_keypair_bootstrap_persists_pem_files(tmp_path: Path) -> None:
    """D76 §C + scope-cut C12: load_or_create_aegis_keypair generates a
    fresh keypair on first call + persists both PEM files. Subsequent
    calls reload from disk (same key bytes)."""
    workspace_dir = tmp_path / "bootstrap-ws"

    priv1, pub1 = load_or_create_aegis_keypair(workspace_dir)
    assert (workspace_dir / "integrity-private-key.pem").exists()
    assert (workspace_dir / "integrity-public-key.pem").exists()

    # Reload — should return the SAME key bytes (compare via signature
    # round-trip; Ed25519PrivateKey doesn't expose direct bytes equality).
    priv2, pub2 = load_or_create_aegis_keypair(workspace_dir)
    test_data = b"round-trip-test"
    sig = priv1.sign(test_data)
    # pub2 (reloaded from disk) verifies signature from priv1 (original).
    pub2.verify(sig, test_data)
    # priv2 + pub1 round-trip
    sig2 = priv2.sign(test_data)
    pub1.verify(sig2, test_data)


# ---------------------------------------------------------------------------
# 10. Unknown integrity-protocol id → resolution failure (D40 §B coverage)
# ---------------------------------------------------------------------------


def test_boot_with_unknown_integrity_protocol_id_raises_resolution(
    tmp_path: Path,
) -> None:
    """D40 §B + D29 namespacing: integrity-protocol id not registered →
    WorkspaceBootError(category='resolution') (parallel to provision
    resolution failures). Phase C bundles AEGIS only; other protocols
    (Axon / PROV-O / post-quantum) are Phase D+."""
    manifest = _load_e2e_manifest_with_integrity(
        tmp_path,
        integrity_protocol="axon-protocol-ext:axon-chain-integrity",
    )
    with pytest.raises(WorkspaceBootError) as excinfo:
        Workspace.boot(manifest, END_TO_END_FIXTURE / "extensions")
    assert any(
        f.category == "resolution"
        and "axon-protocol-ext" in str(f.value)
        for f in excinfo.value.failures
    )
