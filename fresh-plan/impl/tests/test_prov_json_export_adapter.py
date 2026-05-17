"""Tests for the Phase C C9 PROV-JSON export adapter (D77 §B).

Per D77 §A NON-BREAKING contract + D24 standards-compat tracker: the
adapter is EXPORT-ONLY (no inbound; no outbound real-wire) — it converts
the workspace event chain to W3C PROV-JSON (https://www.w3.org/TR/prov-json/)
either returning the dict in-memory or persisting it to a filesystem
path. The fresh-plan event envelope is UNCHANGED.

Test coverage per D77 §B:

  - Structural verification:
    - ProvJsonExportAdapter registered under
      ``prov-json-export-ext:prov-json-export`` in the module
      ``_ADAPTER_CLASSES`` registry.
    - Subclasses Adapter with ``_outcome_prefix = "prov-json-export"``.
  - Happy-path conversion:
    - call() with output-path absent returns dict; structure carries
      prov-json keys + activity-count reflects chain length.
    - call() with output-path set writes file to disk + returns dict;
      file content round-trips as valid JSON.
  - Pre-export action event (D71 pre-wire convention):
    - call() emits one ``action`` event BEFORE conversion; the
      emitted event is NOT included in the exported PROV document
      (export-side-effect is recorded in the chain but excluded from
      the export payload to avoid self-reference pollution).
  - Failure paths (D77 §B.2 triad):
    - File IO failure on readonly directory → AdapterCallError
      (category='transport').
    - Malformed event in chain (synthetic injection) →
      AdapterCallError(category='protocol-error').
"""
from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

import pytest

from fresh_plan.runtime import Workspace
from fresh_plan.runtime.adapter import (
    Adapter,
    AdapterCallError,
    ProvJsonExportAdapter,
    _ADAPTER_CLASSES,
)


FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-prov-json-export-adapter"
)


PROV_EXPORT_ADAPTER_SPEC = {
    "id": "prov-json-export-adapter",
    "version": "0.1.0",
    "protocol-or-transport": "prov-json-export-ext:prov-json-export",
    "required-substrate-capabilities": [],
    "declared-event-emissions": [{"payload-subtype": "action"}],
    "declared-event-consumptions": [],
}


# ---------------------------------------------------------------------------
# Structural verification
# ---------------------------------------------------------------------------


def test_prov_json_export_adapter_registered_under_protocol_identifier():
    """D77 §B + D29 namespacing: ProvJsonExportAdapter registered under
    `prov-json-export-ext:prov-json-export` in module `_ADAPTER_CLASSES`."""
    assert (
        _ADAPTER_CLASSES["prov-json-export-ext:prov-json-export"]
        is ProvJsonExportAdapter
    )


def test_prov_json_export_adapter_subclasses_adapter_with_outcome_prefix():
    adapter = ProvJsonExportAdapter(spec=dict(PROV_EXPORT_ADAPTER_SPEC))
    assert isinstance(adapter, Adapter)
    assert adapter._outcome_prefix == "prov-json-export"
    assert (
        adapter.protocol_or_transport
        == "prov-json-export-ext:prov-json-export"
    )


# ---------------------------------------------------------------------------
# Fixture: booted workspace + bound adapter
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_export_workspace():
    """Boot a workspace with prov-json-export adapter bound + one user
    event in the chain (for non-empty export tests)."""
    manifest = json.loads((FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, FIXTURE / "extensions")
    # Emit a couple of user events so the export has substantive content.
    actor_id = next(iter(ws._substrate.state.actors))
    ws._emit_event(
        actor_id=actor_id,
        payload_subtype="claim",
        payload={"assertion": "first claim"},
        role="author",
    )
    ws._emit_event(
        actor_id=actor_id,
        payload_subtype="claim",
        payload={"assertion": "second claim"},
        role="author",
    )
    try:
        yield ws
    finally:
        ws.shutdown()


# ---------------------------------------------------------------------------
# Happy-path: in-memory export (no output-path)
# ---------------------------------------------------------------------------


def test_call_without_output_path_returns_prov_json_dict(
    booted_export_workspace,
):
    """D77 §B: call('export', {}) with no output-path returns the
    PROV-JSON dict in the result. activity-count reflects chain length
    excluding the pre-export action event itself."""
    ws = booted_export_workspace
    adapter = ws.adapter("primary-prov-export")
    chain_len_before = len(list(ws.event_chain.all_events()))

    result = adapter.call("export", {})

    assert result["ok"] is True
    assert result["output-path"] is None
    # activity-count is the chain length at call-time (the export action
    # event is emitted BEFORE conversion, then excluded from the export
    # payload — so activity-count == chain_len_before).
    assert result["activity-count"] == chain_len_before
    assert result["agent-count"] >= 1  # at least the workspace agent
    prov = result["prov-json"]
    assert "prefix" in prov
    assert "activity" in prov
    assert "agent" in prov
    assert "wasAttributedTo" in prov


def test_call_with_output_path_writes_file_and_returns_dict(
    booted_export_workspace, tmp_path: Path
):
    """D77 §B: call('export', {output-path: ...}) writes JSON to disk
    AND returns dict. Reread the file to verify round-trip integrity."""
    ws = booted_export_workspace
    adapter = ws.adapter("primary-prov-export")
    output = tmp_path / "workspace-prov.json"

    result = adapter.call("export", {"output-path": str(output)})

    assert result["ok"] is True
    assert result["output-path"] == str(output)
    assert output.exists()

    persisted = json.loads(output.read_text())
    assert persisted == result["prov-json"]
    # Workspace anchor agent present.
    assert "fresh-plan:workspace:prov-json-export-ws" in persisted["agent"]


# ---------------------------------------------------------------------------
# Pre-export action event (D71 pre-wire convention)
# ---------------------------------------------------------------------------


def test_call_emits_one_action_event_before_conversion(
    booted_export_workspace,
):
    """D71 pre-wire convention applied to export adapter: an `action`
    event is emitted into the chain BEFORE the conversion call so the
    export is itself attribution-recorded. The exported PROV-JSON
    document, however, EXCLUDES this just-emitted action event (so the
    export does not self-reference)."""
    ws = booted_export_workspace
    adapter = ws.adapter("primary-prov-export")
    before_actions = len(ws.event_chain.by_payload_subtype("action"))
    chain_len_before = len(list(ws.event_chain.all_events()))

    result = adapter.call("export", {})

    actions = ws.event_chain.by_payload_subtype("action")
    assert len(actions) == before_actions + 1
    emitted = actions[-1]
    assert emitted["payload"]["action-name"] == "export"
    assert (
        emitted["payload"]["outcome-reference"]
        == result["outcome-reference"]
    )
    # Activity-count reflects chain BEFORE the pre-export action event
    # (export-side-effect is in the chain but not in the export payload).
    assert result["activity-count"] == chain_len_before
    # The export action event id should NOT appear in the exported
    # activity map.
    export_event_id = emitted["id"]
    assert (
        f"fresh-plan:event:{export_event_id}"
        not in result["prov-json"]["activity"]
    )


# ---------------------------------------------------------------------------
# Failure paths (D77 §B.2 triad)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="POSIX file-mode semantics; readonly-dir test only applies on POSIX.",
)
def test_call_file_write_failure_raises_transport_adapter_call_error(
    booted_export_workspace, tmp_path: Path
):
    """D77 §B.2: file IO failure (write to a readonly directory) →
    AdapterCallError(category='transport') per D48 §D D-3 starter
    category vocabulary REUSE."""
    ws = booted_export_workspace
    adapter = ws.adapter("primary-prov-export")

    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    # Strip write permission for owner/group/other.
    os.chmod(readonly_dir, stat.S_IRUSR | stat.S_IXUSR)
    target = readonly_dir / "prov.json"
    try:
        with pytest.raises(AdapterCallError) as exc_info:
            adapter.call("export", {"output-path": str(target)})
        err = exc_info.value
        assert err.category == "transport"
        assert err.adapter_id == "prov-json-export-adapter"
        assert err.call_target == "export"
        assert "output-path" in err.detail
    finally:
        # Restore write permission so tmp_path cleanup succeeds.
        os.chmod(
            readonly_dir,
            stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR,
        )


def test_call_malformed_event_raises_protocol_error_adapter_call_error():
    """D77 §B.2: malformed event in the chain (synthetic injection) →
    AdapterCallError(category='protocol-error'). Stages a unit-shape
    test against ProvJsonExportAdapter directly: build adapter, attach
    to a stub workspace whose event_chain returns a malformed event."""

    class _StubChain:
        def all_events(self):
            return [{"id": "evt-bad"}]  # missing required fields

        def by_payload_subtype(self, _):  # for adapter._emit_action path
            return []

    class _StubSubstrate:
        def __init__(self):
            self.state = type(
                "S", (), {"actors": {"actor-x": object()}}
            )()
            self.event_chain = _StubChain()

    class _StubWorkspace:
        def __init__(self):
            self._substrate = _StubSubstrate()
            self.workspace_id = "stub-ws"

        def _emit_event(self, **kwargs):
            # Pretend the action event was appended; return a stub event.
            return {"id": "evt-action"}

    adapter = ProvJsonExportAdapter(spec=dict(PROV_EXPORT_ADAPTER_SPEC))
    adapter.attach_workspace(_StubWorkspace())

    with pytest.raises(AdapterCallError) as exc_info:
        adapter.call("export", {})
    err = exc_info.value
    assert err.category == "protocol-error"
    assert err.adapter_id == "prov-json-export-adapter"
    assert "malformed event envelope" in err.detail["reason"]
