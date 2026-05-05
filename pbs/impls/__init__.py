"""Mode 2 reference Implementations — Phase 6.1 thin-slice.

Per `ARCHITECTURE.md` §6 Logic placement modes Mode 2 + `MAINTENANCE.md`
TOP-LEVEL MILESTONE STRUCTURE Phase 6.1 in-scope: reference impls satisfying
the Pattern A protocol Surfaces (`pbs.substrate` / `pbs.adapter` /
`pbs.quality_gate`) + mechanism-class Surfaces (`pbs.audit` / `pbs.sparring`)
locked at Phase 3.4-3.6.

Phase 6.1 thin-slice scope (per `BACKLOG.md` §222-§224):

- `claude_agent_sdk_substrate` — Claude Agent SDK substrate Implementation
  per `arch/substrate.md` §4; MS Agent Framework + hand-rolled deferred per
  `docs/decisions/substrate-hand-rolled-drop.md` thin-slice scope-narrowing
  (hand-rolled dropped) + Phase 6.2 (MS AF added)
- `claude_agent_sdk_audit` — Claude Agent SDK audit storage realization
  (jsonl file-backed; SHA-256 hash-chain) satisfying `pbs.audit.AuditProtocol`
  per `arch/audit.md` §4 default substrate-impl storage realization +
  `ARCHITECTURE.md` §6 composite boot subsection audit-phase 1-3 ordering;
  practitioner-shape default policy (fail-closed) per `BACKLOG.md` §224
  thin-slice scope; autonomous-business / personal-OS shapes wire policies
  via config injection (Phase 6.2 alert + retry mechanics)
- `mcp_server_adapter` — generic MCP-Server adapter Implementation satisfying
  `pbs.adapter.McpServerAdapterProtocol` (which extends `AdapterProtocol`
  META-Surface) per `arch/adapter.md` §3 + §4 per-implementation aspect;
  reference impl spans in_process / subprocess / HTTP transports per
  `pbs.substrate.TransportMode`; MCP-Server class only at Phase 6.1 per
  `BACKLOG.md` §223 (Email / Accounting / A2A-Peer / File-Sync per-class
  Surface Protocols + impls deferred to Phase 6.2)
- `practitioner_shape_gate` — practitioner-shape quality-gate Implementation
  satisfying `pbs.quality_gate.QualityGateProtocol` per `arch/quality-gate.md`
  §4 per-implementation aspect; full engagement procedure (friction + nudge +
  block + practitioner attestation + re-engagement); fail-closed
  (defensibility-critical); stateful (cumulative engagement signals via
  audit-trail-as-state-store reframe per §2.F); axis-3 PRIMARY (rubber-
  stamping detection mandatory per §14 row 2) per `BACKLOG.md` §224 thin-
  slice scope; autonomous-business / personal-OS / research-lab gate impls
  deferred to Phase 6.2 per W1
- `practitioner_shape_authority_binding` — practitioner-shape authority-binding
  mechanism reference satisfying `pbs.authority_binding.AuthorityBindingProtocol`
  per `glossary/authority-binding.md` + `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE
  concept-by-concept table; PRACTITIONER_JUDGMENT trust model; HUMAN actor
  required for accountability-bearing legal-bind moments (signature_applied /
  send_authorized / claim_attested / work_unit_archived /
  workflow_phase_transition); composes with audit class via `AuthorityChecker`
  injection (per `arch/audit.md` §11 `AuditTrustError`); composes with
  substrate Surface §C permission flow via `bind_decision()` (Phase 6.2 wiring
  point). Per `BACKLOG.md` §224 thin-slice; autonomous-business-shape
  (BUDGET_POLICY) + personal-OS-shape (INDIVIDUAL) deferred to Phase 6.2
- `practitioner_shape_sparring` — practitioner-shape sparring mechanism-class
  reference satisfying `pbs.sparring.SparringProtocol` per `arch/sparring.md`
  §6 mechanism-class structural reconciliation; aggregates 8 sub-mechanism
  impl classes (4 architecturally-encoded: counter-argument / confidence-
  calibration / visible-reasoning / selective-friction + 4 behaviorally-
  enforced: anti-sycophancy / asymmetric-knowledge-respect / commit-to-
  recommendations / whats-missing-checkpoint); fail-closed (defensibility-
  critical); all 8 sub-mechanisms active per §14 practitioner-shape profile;
  ≥1 sparring-event per claim mandatory; AI_RUNTIME actor binding for axis-2
  production-phase engagement events. Per `BACKLOG.md` §224 thin-slice;
  autonomous-business-shape (subset 4-6 / fail-open with alert) + personal-
  OS-shape (subset 1-3 / fail-open) sparring impls deferred to Phase 6.2 per
  W3 second-shape productization
- `stub_mcp_server_backend` — minimum-viable filesystem-backed MCP server
  backend per `BACKLOG.md` §226 thin-slice exercising the §224 mechanism
  set end-to-end; exposes 3 MCP tools (`read_entity` / `write_entity` /
  `record_audit_event`) registerable via `arch/substrate.md` §2.B (in-
  process transport at Phase 6.1; subprocess + HTTP transports deferred
  to Phase 6.2); `record_audit_event` realizes the skill-side MCP audit
  gate path per `arch/audit.md` §8 dual-emission (forwards reconstructed
  `AuditEventBase` to injected audit Implementation's `emit()`); single-
  workspace scoping per `arch/scope-model.md` W3 deferred multi-workspace
  schema; production backend (LanceDB + fastembed + bge-m3 + LaTeX
  compile wrapper) deferred to Phase 6.2 per `BACKLOG.md` §248

Phase 6.2 forthcoming impls (deferred per BACKLOG §242+): MS Agent Framework
substrate; Email / Accounting / A2A-Peer / File-Sync per-class adapter impls;
autonomous-business / personal-OS / research-lab gate impls; autonomous-
business-shape + personal-OS-shape authority-binding impls; autonomous-
business-shape + personal-OS-shape sparring impls; LanceDB + fastembed +
bge-m3 + LaTeX compile wrapper production MCP-server backend (replaces
Phase 6.1 stub backend per `BACKLOG.md` §248).

Foundation-up: imports from `pbs.<surface>` (Pattern A Protocols + manifests)
to satisfy them concretely; impls are downstream of Surfaces.
"""
