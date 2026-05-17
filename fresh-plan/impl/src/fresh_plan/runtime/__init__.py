"""fresh-plan runtime — Phase B workstream B2 per D36.

Public API:
    Workspace, ActorHandle, WorkUnitHandle — user-facing handles.
    boot_workspace — explicit boot procedure (also reachable via
        Workspace.boot).
    WorkspaceBootError — raised on B1 validation failure during boot.
    EventRejected — raised when per-event D30 §4 runtime checks reject.
    MalformedEventError — raised on schema / chain-integrity failure.
    InProcessSubstrate — the B2 substrate runtime (for advanced use /
        introspection).

The B2 substrate is the *in-process* substrate (the substrate extension
`inprocess-substrate-ext` honestly names this). Real Claude Agent SDK
integration is a follow-on workstream — B2 mocks the LLM and validates
the framework's runtime structure.
"""
from __future__ import annotations

from fresh_plan.runtime.boot import WorkspaceBootError, boot_workspace
from fresh_plan.runtime.event_chain import (
    AppendOnlyEventChain,
    MalformedEventError,
)
from fresh_plan.runtime.hooks import HookRegistry
from fresh_plan.runtime.per_event_checks import (
    EventRejected,
    check_event_references,
)
from fresh_plan.runtime.skills import SkillRegistry, UnknownSkillError
from fresh_plan.runtime.substrate import (
    ClaudeAgentSDKSubstrate,
    InProcessSubstrate,
    MSAgentFrameworkSubstrate,
    Substrate,
    load_substrate_from_provision,
)
from fresh_plan.runtime.workspace import ActorHandle, Workspace, WorkUnitHandle
from fresh_plan.runtime.workspace_state import (
    DuplicateActorError,
    InvalidWorkUnitTransitionError,
    UnknownActorError,
    UnknownWorkUnitError,
    WORK_UNIT_STATUSES,
    WorkspaceState,
)


__all__ = [
    "ActorHandle",
    "AppendOnlyEventChain",
    "ClaudeAgentSDKSubstrate",
    "DuplicateActorError",
    "EventRejected",
    "HookRegistry",
    "InProcessSubstrate",
    "InvalidWorkUnitTransitionError",
    "MSAgentFrameworkSubstrate",
    "MalformedEventError",
    "SkillRegistry",
    "Substrate",
    "UnknownActorError",
    "UnknownSkillError",
    "UnknownWorkUnitError",
    "WORK_UNIT_STATUSES",
    "Workspace",
    "WorkspaceBootError",
    "WorkspaceState",
    "WorkUnitHandle",
    "boot_workspace",
    "check_event_references",
    "load_substrate_from_provision",
]
