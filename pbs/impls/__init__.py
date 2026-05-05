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

Phase 6.2 forthcoming impls (deferred per BACKLOG §242+): MS Agent Framework
substrate; MCP-server adapter impl; audit storage realization (jsonl
file-backed); authority-binding mechanism; sparring sub-mechanism impls;
practitioner-shape quality-gate impl; autonomous-business / personal-OS /
research-lab gate impls.

Foundation-up: imports from `pbs.<surface>` (Pattern A Protocols + manifests)
to satisfy them concretely; impls are downstream of Surfaces.
"""
