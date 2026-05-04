**STATUS: DRAFT — not locked, not final, Round 1 sharpening surface preserved as v1.x amendment candidate context**

# PydanticAI substrate evaluation — Round 1 sharpening surface

## Origin context

Surfaced 2026-05-04 during Phase 3.7 ARCH amendments work (post-Phase-3.6 close; Pattern A 12+7 FORMAL STABILITY 3 of 3 achieved). Round 1 sharpening fired on the question "Where does PydanticAI fit in the locked substrate Pattern A shape?" using `decision-design-sharpening` v0.10.0. Reached STABLE — lock at this round verdict; user redirected mid-session toward thin-slice v1.0-runtime milestone approach. Round 1 surface parked as v1.x amendment candidate context per `BACKLOG.md` Phase 3.7 entry + `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE → v1.x amendment cadence.

This draft preserves the Round 1 reasoning chain so when the v1.x amendment fires per evidence trigger (PydanticAI maturity reaches ≥5 of 7 Surface categories OR concrete deployment-instance evidence surfaces typed-agent substrate need distinct from Claude Agent SDK / MS AF), Round 2 picks up from preserved context rather than re-deriving.

## Question

Where does PydanticAI fit in the locked substrate Pattern A shape (`arch/substrate.md` §2 seven Surface capability categories + §4 Implementation set)?

## Adoption options considered

- **A**. 4th substrate Implementation — peer of Claude Agent SDK / MS AF / Hand-rolled in `arch/substrate.md` §4 current instance set (NOTE: hand-rolled was concurrently dropped per separate amendment; if A had been chosen, set would have been Claude Agent SDK / MS AF / PydanticAI)
- **B**. NOT a substrate — typed-agent library that lives INSIDE a substrate Implementation (Phase 6 territory); register the eval verdict in §17 provenance + §16 watch-list for re-evaluation signal
- **C**. Cancel/no-action — PydanticAI is implementation detail; ARCH stays silent; eval just produces a "non-event" verdict

## Position committed (Round 1)

**B — NOT a substrate; watch-list entry W5 added.**

## Reasoning

1. **Surface scope mismatch**. Substrate Surface = 7 capability categories (agent loop + MCP server registration with multi-transport / permission flow / structured output / hooks + event-bus / session+context / specialist registration). PydanticAI's positioning is narrower: typed agent calls + Pydantic-validated tool wrapping + structured output. It primarily covers §A (agent loop) + §D (structured output validation). It does NOT natively cover §B (MCP server registration with multi-transport peer model — in-process / subprocess / HTTP as first-class peers), §C (permission flow with `request_permission` 7 decision-kinds per archived `permission-abstraction.md`), §E (hooks + event-bus dispatch), §F (session/context cross-substrate persistence), §G (specialist registration with substrate-native materialization). Satisfies ~2 of 7.

2. **Boundary criteria fail** (`arch/substrate.md` §3). Per the Surface-vs-extension decision rule: "capabilities supported natively with comparable shape across all substrates → Surface; only one substrate supports natively → per-impl extension". PydanticAI satisfying only 2 of 7 Surface categories means it would have to hand-roll the rest. That's not a peer of Claude Agent SDK (which natively covers all 7) or MS AF (which covers all 7 via middleware translation) — it's a typed-agent layer that some substrate impl could USE.

3. **Hand-rolled was the natural home** (per Round 1 framing; concurrent hand-rolled drop amendment 2026-05-04 changes this — see "Composition with concurrent hand-rolled drop" below). Per `arch/substrate.md` line 103 (pre-amendment): "Hand-rolled (Python + MCP + Pydantic) — Tier 1 fallback; minimal direct implementation; baseline for substrate-pluggability validation". PydanticAI fit cleanly inside this — replace some of Hand-rolled's typed-agent + Pydantic-validation guts with PydanticAI primitives. With hand-rolled dropped, PydanticAI's natural home becomes any future substrate impl that wants typed-agent layer (e.g., as Claude Agent SDK substrate impl internal Phase 6 implementation choice).

4. **Pattern-vs-instance discipline**: substrate is the PATTERN (mechanism Surface contract); concrete frameworks are INSTANCES. PydanticAI as a separate Pattern A Implementation would over-elevate a typed-agent library to peer status with full agent-runtime frameworks — instance-leakage at the substrate-level (treating "uses Pydantic" as a substrate-defining property when Pydantic is already a per-impl detail).

## 5 refinements stress-tested upfront

- **R1: Watch-list signal explicit**. Add §16 watch-list entry W5 specifically for PydanticAI (separate from W2 "new substrate candidate emergence"; W5 captures PydanticAI is a known existing candidate already evaluated, not emergent). W5 awaited signal: "PydanticAI matures to satisfy ≥5 of 7 Surface categories natively OR concrete deployment surfaces typed-agent substrate need distinct from Hand-rolled-replacement."
- **R2: §17 provenance entry**. Add archived `substrate-agentic-framework.md` + this evaluation's verdict to §17 decision-design provenance — preserves rationale that PydanticAI was evaluated and rejected-as-substrate (counters future "did we consider PydanticAI?" cycle).
- **R3: NO change to §4 current instance set**. Hand-rolled substrate stays "Python + MCP + Pydantic" — PydanticAI could be a Phase 6 Hand-rolled implementation choice but isn't a separate Implementation requiring §4 enumeration. (NOTE: hand-rolled now dropped per concurrent amendment; R3 reframes to "PydanticAI not added to §4 current instance set; usable as Phase 6 implementation choice inside any substrate impl that wants typed-agent layer.")
- **R4: NO change to §3 boundary criteria**. Boundary criteria already correctly classify PydanticAI as not-substrate; criteria don't need amendment.
- **R5: BACKLOG cross-link**. Phase 6 implementation entry could note "evaluate PydanticAI for typed-agent layer" as implementation choice. Not blocking; Phase 6 territory.

## 4 counter-arguments engaged

- **CA-1**: "PydanticAI may have its own MCP integration as of 2026" — verified via knowledge cutoff: PydanticAI does have MCP support (via `pydantic_ai.mcp.MCPServerStdio` etc.) but this is single-transport; doesn't match the substrate Surface §B multi-transport peer model (in-process / subprocess / HTTP as first-class peers). Doesn't change boundary verdict.
- **CA-2**: "If PydanticAI grows to satisfy more Surface categories, position should reverse" — agreed; that's exactly what W5 watch-list captures. Concrete signal: ≥5 of 7 Surface categories satisfied natively.
- **CA-3**: "Even if not substrate-grade, PydanticAI's typed-agent abstraction may inform Phase 6 spec contract for substrate Surface §A" — possible but Phase 6 territory, not Phase 3 ARCH amendment. Surface contract is articulated at conceptual level; Phase 6 lands Pydantic Protocol typing. Not a Phase 3 concern.
- **CA-4**: "Position B feels like 'no real architectural change' — is this evaluation worth Phase 3.7 effort?" — partial concession; the eval verdict is "no amendment to §4". But the value is RECORDED-RATIONALE: §17 provenance entry preserves the eval, §16 W5 adds explicit re-eval signal. Without this, BACKLOG line 131 stays unresolved and future sessions could re-litigate. Eval verdict + watch-list IS the architectural deliverable.

## Composition with existing architecture

- **`arch/substrate.md`**: minor amendments to §16 (W5 add) + §17 (provenance entry); NO change to §1–§15.
- **GLOSSARY**: no changes (PydanticAI doesn't surface a new vocabulary distinction).
- **BACKLOG.md**: Phase 3.7 entry resolved with cross-link to amendment commit when v1.x amendment fires; potential Phase 6 cross-link in substrate impl entry (informational, not load-bearing).
- **Other ARCH topics**: no cascade.

## Composition with concurrent hand-rolled drop (2026-05-04)

Hand-rolled substrate Implementation was dropped concurrent with this Round 1 sharpening per separate amendment. Round 1 Position B reasoning (item 3) cited Hand-rolled as the natural home for PydanticAI. With hand-rolled dropped, the natural home becomes any future substrate impl that adopts typed-agent layer (e.g., Claude Agent SDK substrate impl internal Phase 6 implementation choice; potential future substrate impl emerging per W2).

This DOES NOT reverse Position B. PydanticAI is still NOT a substrate (still satisfies ~2 of 7 Surface categories); the natural home shifts from "Hand-rolled internal" to "any substrate impl's internal typed-agent layer choice." W5 watch-list signal (≥5 of 7 Surface categories) remains the canonical revisit trigger.

## Round 1 termination self-check (per skill v0.6.0)

- **REVISION/EXPANSION classification**: 0 REVISIONS surfaced; 5 refinements all EXPANSIONS (W5 add, §17 add, no §4 change, no §3 change, BACKLOG cross-link). No EXPANSION feels REVISION-flavored on second look.
- **Empirical density**: 5 refinements + 4 counter-arguments engaged in Round 1 (typical for narrow-surface decisions per skill empirical observation 5-15 refinements).
- **Surface-type**: ARCHITECTURAL-DECISION; expected decay 6→5→3→0-1 per skill.

**Self-check verdict**: STABLE — lock at this round candidate. Termination signals: narrow architectural surface (single sub-decision; amendment-shape); 0 REVISIONS; all refinements EXPANSIONS; verdict resolves the question; W5 captures revisit mechanism. Per skill 2-round sweet spot: this fits the narrow-decision pattern; Round 2 would likely surface manufactured criticism rather than substantive refinements.

User did NOT trigger Round 2 — pivoted to thin-slice v1.0-runtime milestone approach mid-conversation; Round 1 surface parked.

## Round 1 termination checklist (per skill)

- [x] SKILL.md Read at this invocation
- [~] Profile files Read for this validation — read `profiles/INDEX.md`; full L1 / L4a / L8 cluster profiles are skeletons; principle-level multi-axis check applied (substrate amendment is narrow surface; profile-anchored deeper validation candidate for Round 2 if/when v1.x amendment fires)
- [x] Archived sources greenfield-evaluated — re-read `substrate-agentic-framework.md` (10-candidate eval; PydanticAI absent from screen) + `permission-abstraction.md` (R3c Substrate.request_permission Surface); archived ROADMAP context confirmed PydanticAI was demoted from BLOCKING and never produced its own DR
- [x] Pattern-vs-instance stress-test — applied per CA-1 / CA-3 / CA-4: PydanticAI as substrate would be instance-leakage (over-elevating typed-agent library to substrate-pattern peer); position B preserves pattern integrity
- [x] G Gate — substrate Implementation set is L1-L3 producer territory; G Gate fires here. Verdict: position B preserves multi-mode consumption (any substrate impl stays substrate-portable; PydanticAI as internal impl choice doesn't break composability gate). Pass.
- [x] D Gate — am I deferring? W5 watch-list is NOT a defer — explicit external signal named (≥5 Surface categories satisfied natively OR deployment-driven typed-agent substrate need). Mental modeling RESOLVES the question now (verdict B locked); watch-list captures REVISIT mechanism, not deferral. Pass.

## Knowledge-cutoff caveats

- PydanticAI MCP integration assessment (CA-1) reasoned from training data + general PydanticAI ecosystem knowledge. If v1.x amendment fires per evidence trigger, web-fetch current PydanticAI docs to confirm: (a) multi-transport MCP support status; (b) permission flow primitives status; (c) hook + event-bus surface status; (d) session/context cross-substrate persistence status; (e) specialist registration analog status.
- "≥5 of 7 Surface categories" threshold for W5 trigger is heuristic — Round 2 sharpening (when fired) should refine the precise threshold + per-category coverage criteria.

## Maturity test

What would graduate this draft to a locked v1.x amendment?

- **Evidence trigger fires** per W5 watch-list signal: PydanticAI maturity reaches ≥5 of 7 Surface categories natively OR concrete deployment-instance evidence (Track 1 viability test or Phase 6.1 work) surfaces typed-agent substrate need distinct from Claude Agent SDK / MS AF
- **Round 2 sharpening** fires on this draft + current PydanticAI docs verification + profile-anchored deeper validation
- **DR drafted** at `docs/decisions/pydanticai-substrate-evaluation.md` if verdict reverses to Position A (4th Implementation) OR amendment to `arch/substrate.md` §16 W5 + §17 provenance lands if verdict stays Position B but warrants formal architectural amendment
- **Draft removed** at graduation per `drafts/README.md` discipline (provenance lives in commit + DR; no retention)

## Cross-references

- `BACKLOG.md` Phase 3.7 v1.x ARCH amendment candidates entry (PydanticAI substrate evaluation — non-sequential; fires per W5 evidence trigger)
- `arch/substrate.md` §2 (Surface 7 capability categories) + §3 (boundary criteria) + §4 (current instance set; post-hand-rolled-drop = 2 Implementations) + §16 (watch-list; W5 candidate) + §17 (decision-design provenance)
- `archive/docs/decisions/substrate-agentic-framework.md` (#18 — original 10-candidate eval; PydanticAI absent from screen; demoted from BLOCKING per ROADMAP #20 framing)
- `archive/docs/decisions/permission-abstraction.md` (R3c — Substrate.request_permission Surface; permission flow surface PydanticAI doesn't natively cover)
- `MAINTENANCE.md` TOP-LEVEL MILESTONE STRUCTURE → v1.x amendment cadence (governs when this draft graduates)
- `MAINTENANCE.md` TOP-LEVEL DESIGN PRINCIPLES §2 (pattern-vs-instance discipline; per-instance leakage prevention)
- `plugin/skills/decision-design-sharpening/SKILL.md` v0.10.0 (Round 1 surface produced via this skill)
