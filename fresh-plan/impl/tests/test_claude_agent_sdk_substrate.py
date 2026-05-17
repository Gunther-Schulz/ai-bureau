"""Tests for the Phase C C1 Claude Agent SDK real-wire substrate (D69 §B.1).

Per scope-cut C12 (autopilot constraint): tests use a monkeypatched
_sdk_client_factory to inject a fake SDK client; NO real Anthropic API calls.
The fake client mimics ClaudeSDKClient's async surface (connect /
receive_response / disconnect) under controlled conditions:

  - Happy-path: connect succeeds; receive_response yields synthetic messages
    that translate to action events; disconnect succeeds.
  - sdk-init failure: connect raises; start_session wraps as
    WorkspaceBootError(category='sdk-init') with the SDK exception chained.
  - Subscriber capture: a synthetic message that triggers a subscribing
    specialist's on_event raise is captured per D47 §B.1 aggregation —
    NOT re-wrapped as sdk-init (the SDK-side path succeeded; the failure is
    in framework-level subscriber dispatch).
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from fresh_plan.runtime import (
    ClaudeAgentSDKSubstrate,
    InProcessSubstrate,
    Substrate,
    Workspace,
    WorkspaceBootError,
    load_substrate_from_provision,
)
from fresh_plan.runtime.substrate import SubscriberDispatchError
from fresh_plan.validator.schemas import load_schemas
from fresh_plan.validator.types import FAILURE_CATEGORIES


IMPL_EXTENSIONS_DIR = Path(__file__).resolve().parents[1] / "extensions"
CLAUDE_FIXTURE = (
    Path(__file__).parent / "fixtures" / "workspace-claude-agent-sdk-substrate"
)
SCHEMAS_DIR = Path(__file__).resolve().parents[2] / "schemas"


# ---------------------------------------------------------------------------
# Test doubles
# ---------------------------------------------------------------------------


# Per substrate's _translate_sdk_message_to_event: identification uses
# ``type(message).__name__``. Fake classes are NAMED to match the real SDK
# message class names so translation fires (keeps framework SDK-import-free
# while still exercising the real translation path).
class AssistantMessage:  # noqa: N801 — mimics claude_agent_sdk.types.AssistantMessage
    """Stand-in for claude_agent_sdk.types.AssistantMessage."""


class ResultMessage:  # noqa: N801 — mimics claude_agent_sdk.types.ResultMessage
    """Stand-in for claude_agent_sdk.types.ResultMessage."""


class SystemMessage:  # noqa: N801 — mimics claude_agent_sdk.types.SystemMessage (non-translated)
    """Stand-in for claude_agent_sdk.types.SystemMessage — non-translated."""


class _FakeSDKClient:
    """In-process fake for claude_agent_sdk.ClaudeSDKClient.

    Tracks connect / receive_response / disconnect invocations. Configurable
    per test via class attributes / constructor kwargs.
    """

    # Per-instance trackers populated at construction.
    def __init__(self, options=None) -> None:
        self.options = options
        self.connect_called = False
        self.disconnect_called = False
        self.connect_prompt = None
        # Subclasses override _messages / _connect_raises / _disconnect_raises.
        self._messages: list[object] = []
        self._connect_raises: BaseException | None = None
        self._disconnect_raises: BaseException | None = None

    async def connect(self, prompt=None) -> None:
        self.connect_called = True
        self.connect_prompt = prompt
        if self._connect_raises is not None:
            raise self._connect_raises

    async def receive_response(self):
        for msg in self._messages:
            yield msg

    async def disconnect(self) -> None:
        self.disconnect_called = True
        if self._disconnect_raises is not None:
            raise self._disconnect_raises


def _make_happy_factory(messages: list[object]):
    """Factory that returns _FakeSDKClient instances pre-loaded with messages.
    """

    class _HappyClient(_FakeSDKClient):
        def __init__(self, options=None) -> None:
            super().__init__(options=options)
            self._messages = list(messages)

    return _HappyClient


def _make_connect_failing_factory(exc: BaseException):
    class _FailingClient(_FakeSDKClient):
        def __init__(self, options=None) -> None:
            super().__init__(options=options)
            self._connect_raises = exc

    return _FailingClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def booted_claude_workspace():
    manifest = json.loads((CLAUDE_FIXTURE / "workspace.json").read_text())
    ws = Workspace.boot(manifest, CLAUDE_FIXTURE / "extensions")
    try:
        yield ws
    finally:
        ws.shutdown()


# ---------------------------------------------------------------------------
# 1. FAILURE_CATEGORIES extension (D69 §B.1)
# ---------------------------------------------------------------------------


def test_sdk_init_category_registered():
    """D69 §B.1: FAILURE_CATEGORIES MUST include 'sdk-init' for Phase C
    real-wire SDK init / auth / connection failure."""
    assert "sdk-init" in FAILURE_CATEGORIES


# ---------------------------------------------------------------------------
# 2. Loader dispatch (Step 5 — register in _SUBSTRATE_CLASSES)
# ---------------------------------------------------------------------------


def test_load_substrate_from_provision_returns_claude_agent_sdk_subclass():
    """D69 §C + Step 5: the shipped substrate provision dispatches to the
    ClaudeAgentSDKSubstrate runtime class with the expected capabilities +
    runtime-shape per D17 + D43."""
    schema_store = load_schemas(SCHEMAS_DIR)
    substrate = load_substrate_from_provision(
        "claude-agent-sdk-substrate-ext:claude-agent-sdk-substrate",
        IMPL_EXTENSIONS_DIR,
        workspace_id="probe-ws",
        runtime_shape="claude-agent-sdk-substrate-ext:interactive",
        schema_store=schema_store,
        capabilities=["hooks", "skills", "event-chain"],
    )
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)
    assert isinstance(substrate, Substrate)
    assert not isinstance(substrate, InProcessSubstrate)
    assert substrate.capabilities == ["hooks", "skills", "event-chain"]
    assert substrate.runtime_shape == (
        "claude-agent-sdk-substrate-ext:interactive"
    )


# ---------------------------------------------------------------------------
# 3. Boot lifecycle (Acceptance Criterion 3)
# ---------------------------------------------------------------------------


def test_boot_attaches_claude_substrate_with_full_composition(
    booted_claude_workspace,
):
    """D7 §4 + D46: booting the fixture instantiates ClaudeAgentSDKSubstrate
    (not InProcessSubstrate), seeds manifest-actor, attaches generic-shape,
    instantiates bound adapter + specialist, emits lifecycle-transition:boot.
    """
    ws = booted_claude_workspace
    assert isinstance(ws.substrate, ClaudeAgentSDKSubstrate)
    assert isinstance(ws.substrate, Substrate)
    assert not isinstance(ws.substrate, InProcessSubstrate)
    # Shape + adapter + specialist all attached.
    assert ws.substrate.shape is not None
    assert ws.substrate.shape.id == "generic-shape"
    assert "primary-mcp" in ws.substrate.adapter_instances
    assert "primary-specialist" in ws.substrate.specialist_instances
    # Manifest actor seeded via composition-change:add + boot event emitted.
    assert ws.substrate.state.has_actor("agent-primary")
    # Chain carries: 1 composition-change:add + 1 lifecycle-transition:boot.
    assert len(ws.event_chain) >= 2
    boot_event = ws.event_chain.tail
    assert boot_event.get("payload-subtype") == "lifecycle-transition"
    assert boot_event.get("payload", {}).get("transition-type") == "boot"


# ---------------------------------------------------------------------------
# 4. Start/stop session round-trip — SDK callback fires append_event
#    (Acceptance Criterion 6a)
# ---------------------------------------------------------------------------


def test_start_session_drives_sdk_round_trip_and_emits_events(
    booted_claude_workspace,
):
    """D69 §B.1 + D44 sync-substrate: start_session uses asyncio.run to drive
    the async SDK lifecycle. SDK messages translate to action events via
    append_event (preserving D10 chain integrity). stop_session disconnects
    cleanly."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)

    chain_len_pre = len(ws.event_chain)
    # Inject a happy fake SDK client that yields 2 translatable messages.
    messages = [AssistantMessage(), ResultMessage()]
    substrate._sdk_client_factory = _make_happy_factory(messages)

    seqs = substrate.start_session(prompt="hello, agent")

    # Each translatable message produced one action event.
    assert len(seqs) == 2
    assert len(ws.event_chain) == chain_len_pre + 2
    last_event = ws.event_chain.tail
    assert last_event.get("payload-subtype") == "action"
    assert last_event.get("payload", {}).get("action-name") == (
        "claude-agent-sdk-substrate-ext:sdk-message"
    )
    # Each emitted event attributes to the agent-actor seeded by manifest.
    assert last_event["actors"][0]["id"] == "agent-primary"

    # _sdk_client is set during the session, cleared by stop_session.
    # (After asyncio.run returns, the client object stays on the substrate
    # until stop_session releases it.)
    assert substrate._sdk_client is not None
    substrate.stop_session()
    assert substrate._sdk_client is None
    assert substrate._session_active is False


def test_stop_session_is_idempotent_when_no_session_active(
    booted_claude_workspace,
):
    """D69 §B.1 recovery: stop_session is a no-op when _sdk_client is None
    (safe to call without an active session OR after a prior stop_session)."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)
    assert substrate._sdk_client is None
    # First call: no-op.
    substrate.stop_session()
    # Second call: still no-op.
    substrate.stop_session()
    assert substrate._sdk_client is None


def test_start_session_with_no_prompt_connects_and_returns_empty(
    booted_claude_workspace,
):
    """D69 §B.1: start_session with prompt=None opens the SDK connection
    but does not drain receive_response (no messages flow until the caller
    drives interaction). Per the Phase C C1 scope cut — one round-trip per
    start_session — this proves the connect-only happy path."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)
    substrate._sdk_client_factory = _make_happy_factory([])
    seqs = substrate.start_session(prompt=None)
    assert seqs == []
    substrate.stop_session()


# ---------------------------------------------------------------------------
# 5. sdk-init failure surface (Acceptance Criterion 6b)
# ---------------------------------------------------------------------------


def test_start_session_connect_failure_surfaces_as_sdk_init(
    booted_claude_workspace,
):
    """D69 §B.1 Detection + Surface: SDK ``connect`` raise is caught by
    start_session and wrapped as WorkspaceBootError(category='sdk-init')
    with the original SDK exception chained via __cause__. Substrate is
    left in clean state (recovery contract)."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)

    sdk_exc = RuntimeError("connection refused — auth token rejected")
    substrate._sdk_client_factory = _make_connect_failing_factory(sdk_exc)

    with pytest.raises(WorkspaceBootError) as excinfo:
        substrate.start_session(prompt="hello")

    # Structured failure carries the sdk-init category.
    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].category == "sdk-init"
    assert failures[0].path == "substrate.session.start"
    assert "connection refused" in failures[0].reason
    # Original SDK exception chained via Python's `from`.
    assert excinfo.value.__cause__ is sdk_exc

    # D69 §B.1 Recovery: substrate left in a clean state.
    assert substrate._sdk_client is None
    assert substrate._session_active is False


def test_start_session_double_invocation_surfaces_as_sdk_init(
    booted_claude_workspace,
):
    """D69 §B.1 Detection: calling start_session while a session is already
    active raises WorkspaceBootError(category='sdk-init'). Prevents the
    accidental double-connect failure mode."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)

    # Force _session_active=True without going through start_session.
    substrate._session_active = True
    substrate._sdk_client_factory = _make_happy_factory([])

    with pytest.raises(WorkspaceBootError) as excinfo:
        substrate.start_session(prompt=None)
    failures = excinfo.value.failures
    assert len(failures) == 1
    assert failures[0].category == "sdk-init"
    assert "already active" in failures[0].reason


# ---------------------------------------------------------------------------
# 6. SDK callback exception → captured per D47 §B.1 (Acceptance Criterion 6c)
# ---------------------------------------------------------------------------


def test_sdk_message_translated_to_event_triggers_specialist_on_event(
    booted_claude_workspace,
):
    """D69 §B.1 + D47 §B.1 + D44: an event emitted from SDK message
    translation passes through the substrate's full append_event integrity
    gate. A subscribing specialist's on_event raise during the resulting
    subscriber dispatch is captured into _subscriber_failures and surfaces
    as SubscriberDispatchError after the outer drain — NOT re-wrapped as
    sdk-init (the SDK-side path completed; the failure is framework-level)."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)

    # Inject a synthetic subscription on the specialist's spec dict so the
    # subscriber-dispatch loop attempts to fire on_event on SDK-driven action
    # events. ``declared_event_subscriptions`` is a property that returns a
    # copy of the underlying spec list, so we must mutate ``spec`` directly.
    specialist = ws.specialist("primary-specialist")
    original_subscriptions = list(
        specialist.spec.get("declared-event-subscriptions", []) or []
    )
    specialist.spec["declared-event-subscriptions"] = [
        *original_subscriptions,
        {"payload-subtype": "action"},
    ]

    original_on_event = specialist.on_event
    captured_events: list[dict] = []

    def _raising_on_event(event: dict) -> None:
        captured_events.append(event)
        raise RuntimeError(
            "synthetic specialist failure during SDK-driven event"
        )

    specialist.on_event = _raising_on_event  # type: ignore[method-assign]
    try:
        substrate._sdk_client_factory = _make_happy_factory(
            [AssistantMessage()]
        )
        with pytest.raises(SubscriberDispatchError) as excinfo:
            substrate.start_session(prompt="hello")
        # Subscriber failure was captured — NOT an sdk-init failure.
        assert len(captured_events) == 1
        assert captured_events[0]["payload-subtype"] == "action"
        # Aggregated SubscriberDispatchError carries (specialist_id, event_id, exc).
        assert len(excinfo.value.failures) == 1
        spec_id, evt_id, exc = excinfo.value.failures[0]
        assert spec_id == "generic-specialist"
        assert evt_id is not None
        assert isinstance(exc, RuntimeError)
        assert "synthetic specialist failure" in str(exc)
    finally:
        # Restore for fixture teardown's shutdown call.
        specialist.on_event = original_on_event  # type: ignore[method-assign]
        specialist.spec["declared-event-subscriptions"] = original_subscriptions


# ---------------------------------------------------------------------------
# 7. Non-translatable message types are silently skipped
# ---------------------------------------------------------------------------


def test_non_translatable_sdk_messages_are_skipped(
    booted_claude_workspace,
):
    """D69 §B.1 + the message-taxonomy mapping: SystemMessage / other
    non-translated SDK message types do NOT produce events. Per C1 scope —
    finer-grained mapping deferred to Phase C+."""
    ws = booted_claude_workspace
    substrate = ws.substrate
    assert isinstance(substrate, ClaudeAgentSDKSubstrate)

    chain_len_pre = len(ws.event_chain)
    substrate._sdk_client_factory = _make_happy_factory(
        [SystemMessage(), AssistantMessage(), SystemMessage()]
    )
    seqs = substrate.start_session(prompt="hello")
    # Only the AssistantMessage translated.
    assert len(seqs) == 1
    assert len(ws.event_chain) == chain_len_pre + 1
    substrate.stop_session()


# ---------------------------------------------------------------------------
# 8. InProcess loader regression guard
# ---------------------------------------------------------------------------


def test_inprocess_loader_dispatch_still_resolves_inprocess_class():
    """Regression guard: registering claude-agent-sdk-substrate in
    _SUBSTRATE_CLASSES must not perturb existing dispatch."""
    schema_store = load_schemas(SCHEMAS_DIR)
    substrate = load_substrate_from_provision(
        "inprocess-substrate-ext:inprocess-substrate",
        IMPL_EXTENSIONS_DIR,
        workspace_id="probe-ws",
        runtime_shape="interactive",
        schema_store=schema_store,
        capabilities=["hooks", "skills", "event-chain"],
    )
    assert isinstance(substrate, InProcessSubstrate)
    assert isinstance(substrate, Substrate)
    assert not isinstance(substrate, ClaudeAgentSDKSubstrate)
