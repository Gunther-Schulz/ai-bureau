# fresh-plan

Append-only decision ledger for a fresh framework dev plan, started 2026-05-08 on branch `fresh-plan`.

## Session-start procedure (Claude: follow when invoked)

**When the user has directed you to this README** (e.g., "read fresh-plan/README.md"), follow these steps in order before responding to substantive prompts:

1. **Read this README in full** — context + conventions + status + working preferences.
2. **Read `fresh-plan/decisions.md` in full** — the append-only ledger. Each entry is locked; supersedes-relationships are explicit. Key closure entries: **D5** (layer 1 identity), **D25** (layer 2; 8 kinds), **D35** (Phase A — layer 3 formal schemas + composition rules + versioning). **D26** + **D36** name the post-Phase-A roadmap. The latest entries reflect current state; check the bottom of the file.
3. **Confirm context tightly** — in 2–3 sentences, tell the user where work stands (last decision number; current phase per D26; any explicit open threads — including Phase B impl status at `fresh-plan/impl/` if relevant). Do not summarize the entire ledger; cite by entry number.
4. **Wait for user direction** — do not jump into work. The user may have specific next steps that don't follow the obvious path.

Throughout the session, follow the **procedural conventions** + **working preferences** below.

## Operating disciplines (load-bearing during session)

- **Append-only ledger.** Entries in `decisions.md` are locked once added. Override = new entry that explicitly supersedes the prior. Never edit a locked entry's substance; clarifications go in follow-up entries.
- **One question at a time.** Discussion proceeds question by question. Each question is answered (or deliberately deferred) before the next is opened. Don't batch unrelated questions.
- **Concrete examples before locking.** Substantive decisions are grounded with worked examples that exercise the contract before the entry is written. Don't write a decision entry from pure abstract reasoning when a concrete scenario is available.
- **Multiple passes for substantive findings.** When a finding has cascading effects (e.g., the strict protocol-neutrality finding in D16), do honest passes — solidify or refute — before locking. Single-pass on big findings is unsafe.
- **Rolling refinement (option C).** Clear-now findings get supersedes / clarification entries when surfaced (rather than accumulating until a closure pass). The named refinement pass per D14 catches cross-cutting and late-emerging findings at end-of-layer.
- **Commit and push regularly.** Each substantive lock ≈ one commit, pushed to `origin/fresh-plan` (canonical branch per D36). Some hosted-session environments push to a session-specific branch (e.g., `claude/identify-repo-S5zfO`) — those are session-quirks; reconcile to `fresh-plan` at the session boundary (see "Branch state" below). The session-stop hook complains about uncommitted / untracked files and will block stop until clean.

## Working preferences (observed during prior session)

- **Be honest, not sycophantic.** Push back when the user's claim is wrong; don't agree just to agree. (This is also load-bearing in the framework — D24's standards-compatibility check + the anti-sycophancy theme that emerged from input research during the early session.)
- **Surface tensions explicitly.** Name when something feels off; don't paper over.
- **Tight responses.** Concise communication; tables / bullets where they help; no padding.
- **Cite decisions by number** (D1, D7, D16, etc.) rather than summarizing them inline. The ledger is the canonical reference.

## Working patterns (accumulated across sessions)

Working-process disciplines that emerged through development, parallel to the operating-disciplines + working-preferences above. NOT architectural decisions (those live in `decisions.md`) — these are *how the work proceeds*.

- **Sketch-then-lock for substantive decisions.** For tier-3 substantive items (real architectural choices with branching): sketch the shape first → user signs off on framing → deliver a committed draft → one-round review → lock. Don't jump straight to a draft when the framing isn't agreed. Avoid menu-style "here are 5 options"; commit to a recommendation with tradeoffs surfaced. Pattern observed across D29 / D30 / D32 / D33 / D40 lock cycles.
- **Sub-agent dispatch when / how.** Dispatch a sub-agent for *substantive design + large-artifact production* (multi-module impls per workstream B1 / B2; big sweeps like the D34 refinement pass; fresh-eyes review where Writer-Reviewer separation per process-kit invariant 4 is genuinely valuable). Main-session for *mechanical encoding + small commits + routine wording*. Brief shape: focused scope + required-reading list + concrete deliverables + tensions-to-surface + what-NOT-to-do + return-report format.
- **Honest naming.** Name artifacts for what they ARE today, not what they aspire to become. Example: `inprocess-substrate-ext` (mocked LLM) rather than `claude-agent-sdk-ext` (which would imply real Claude SDK integration). Real names land when real things land. Avoids forward-looking misrepresentation in the codebase.
- **Follow-on tracking** (`<workstream>-followon-N`). When scope is deliberately cut, track as e.g., `B2-followon-1`, `B2-followon-2`. Surfaced in commit messages + relevant ledger entries; addressed before phase closure. Distinguishes "deferred-with-evidence" from "forgotten."
- **Side-quest persistence rule.** Research, positioning, landscape analysis, competitive notes, vision-framing analysis → `market-context.md` (or similar research file). New ledger entries (D-N) *only* for architectural decisions. Positioning is deliberately deferred per discipline; keeping research separate from the ledger separates "thinking we do" from "decisions we lock."
- **Generic vs pioneer-instance discipline.** When building "generic" exemplars per D26 (e.g., B3's generic-shape impl), keep them deliberately neutral. Don't accidentally bake in pioneer-specific opinions. D26 explicitly says B3 is NOT practitioner-shape; the bias-avoidance is load-bearing for Phase E shape-neutrality validation.
- **Fixture vs canonical artifact placement.** Test fixtures (`impl/tests/fixtures/`) are *disposable test inputs*, not canonical artifacts. Canonical artifacts (substrate impls, shape impls, adapter impls) live at `impl/extensions/`. Don't promote a fixture to canonical without intent; don't duplicate work between the two. Example: `min-shape-ext` under B2 fixtures is a test-only minimal shape; the B3 generic-shape impl is a separate canonical artifact under `impl/extensions/`.
- **Steelman-then-resolve.** When a competing alternative surfaces (Kore.ai's orchestrator-vs-worker per D37; Sana's knowledge-as-core per D38; AEGIS-at-core per D40; the `extends` slot per D31; etc.), steelman it honestly + name it explicitly in the rejection rationale. The defense is part of the lock; future readers don't re-open the question. Pattern shape: D8 / D17 / D31 / D37 / D38 / D40.

## Ledger conventions

Structural conventions for `decisions.md` entries, distilled from D7 / D10 / D13 / D16 / D19 / D20 / D29 / D30 / D32 / D33 / D40. **Revisable when a substantive entry's content makes the structure awkward** — structural reason, not aesthetic preference. Revision = update this section + any supersedes entries (NOT rewrites; append-only ledger discipline stands per the operating discipline above).

- **Section shape.** Open with `## D<N> — <YYYY-MM-DD> — <one-line title>`. Then a bold `**Decision**:` paragraph stating the lock crisply. Then numbered sections (`### A.` / `### B.` / etc. — or named subsections when the entry isn't multi-axis). For substantive entries: a `### What is NOT in this decision` section enumerating explicit deferrals + out-of-scope items. Close with `**Rationale**:` paragraph + `**Cross-references**:` line listing related D-N's.
- **Worked-example inclusion.** Substantive entries (esp. those defining new contracts) include a worked example exercising the contract — either inline (`### Worked example`) or in a cited fixture / schema file. Distinct from the operating discipline "Concrete examples before locking" (which is about *grounding the thinking*) — this is about *including the example in the entry's own text* so future readers see what conformance looks like. Pattern across D29 / D30 / D32 / D33 / D40.

---

## What this is (background)

A clean restart of framework architectural decisions. The existing `pbs-bureau` corpus (`VISION.md`, `ARCHITECTURE.md`, `MAINTENANCE.md`, `GLOSSARY.md`, `arch/*`, `profiles/*`, `plugin/*`, `pbs/*`, 1-5 numbered docs at repo root) is treated as **input, not as anchor**. Each prior artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

The fresh-plan reverses the prior `5-PIVOT-DECISION.md` (which had paused the framework and made PBS-Schulz primary). Per D1: **reusable framework is primary; PBS-Schulz is the first deployment / proving ground; generality wins on conflict.**

## Layered structure (per D3)

| Layer | Content | Status |
|---|---|---|
| **Layer 1 — identity** | I1 composition system / I2 machine-checkable contracts / I3 accountability-bearing AI-human work. No substantive identity at core; substantive identity carried by shapes per D4. | Closed at D5. |
| **Layer 2 — kinds** | 8 kinds (workspace D7, actor D9, event D10, substrate D12, shape D13, adapter D16, specialist D19, work-unit D20). | Closed at D25. |
| **Layer 3 — extension protocol + formal schemas** | Per-kind formal schemas (workstream 3 artifacts in `schemas/`). Extension declaration mechanism (D29). Composition + boot-time resolution (D30, D31, D32). Promotion / demotion + versioning policy (D33). End-of-Phase-A refinement (D34). | Closed at D35 (Phase A). |
| **Implementation (below layer 3)** | Format / serialization choices; storage / wire / protocol mechanisms; specific extension impls (substrate impls, shape impls, adapter impls, specialist impls). | Out of scope for framework-core work. Begins at D26 Phase B. |

## The 8 kinds at a glance

| Kind | Decision | One-line |
|---|---|---|
| workspace | D7 | Bounded coordination context where one composition runs (manifest + state). |
| actor | D9 (refined by D22) | Attribution-bearing participant; subtypes `human-actor` / `agent-actor`. |
| event | D10 (refined by D23) | Single ordered chain per workspace; payload-subtypes (claim, action, state-change, composition-change, lifecycle-transition + extension-registered). |
| substrate | D12 (cap section by D17) | Hosts the agent loop; declares capabilities (core abstract: `hooks`, `skills`, `event-streaming`) + extension-registered protocol-named capabilities. |
| shape | D13 | Substantive identity carrier (per D4); policy bundle. |
| adapter | D16 | Interface to external surfaces; `protocol-or-transport` open vocabulary (no specific protocols at core per strict D2). |
| specialist | D19 | Internal capability bundle; declares skills + supported work-unit-kinds + adapter dependencies + event subscriptions. |
| work-unit | D20 | Instance of organized work; kind-discriminated (extension-registered); fixed core lifecycle enum (created / in-progress / paused / completed / abandoned). |

## Roadmap (indicative; per D26)

Phases beyond layer-2 closure, named at high level — order indicative not rigid; phase boundaries trigger-based not scheduled. See **D26** in `decisions.md` for full content.

| Phase | Work | Status |
|---|---|---|
| **A — Layer 3** | Formal schemas per kind; extension declaration mechanism; composition / promotion rules; JSON Schema toolchain | **Closed at D35.** Refined by D34 (refinement pass) + D37-D40 (side-quest sharpening). |
| **B — Reference impl of core** | Generic substrate / shape / adapters / specialist; minimal RAG-via-MCP | **In progress.** Workstreams per D36: B1 conformance validator ✅, B2 substrate runtime ✅ (+ B2-followon-1 D39 record emission ✅ + B2-followon-2 D40 §A `state_at(n)` ✅), B3 generic shape ✅, B4 MCP-server adapter (next), B5 direct-api adapter, B6 specialist, B7 RAG-via-MCP, B8 end-to-end. |
| **C — Standards-compat impl** | A2A peer adapter; MCP server adapter (validates D21) | Not started. Phase B prerequisite. |
| **D — Pioneer-instance (PBS-Schulz)** | Practitioner-shape; domain specialists; bauleitplanung corpus; PBS-Schulz workspace manifest; cutover from 0.1.0 plugin | Not started. Phase B + C prerequisite. |
| **E — Multi-deployment validation** | Second shape impl; second workspace; federation begins | Not started. |
| **F+** | Refinement / optimization / ecosystem | Indefinite. |

## Open questions / deferred items (with phase placement)

Per D26, deferred items have implicit phase homes:

- **D1 open tension** (PBS-Schulz daily during rebuild) → resolved in Phase D.
- **Optional `parent-actor` slot on actor** → revisit in Phase A or B if sub-agent patterns surface concrete need.
- **Workflow as containment hierarchy on work-unit** → Phase D (pioneer) or E (multi-deployment) if forced.
- ~~Branch / commit strategy~~ → **resolved in D36** (`fresh-plan` is canonical).
- **D21 verification targets** (A2A peer + MCP server) → Phase C.
- **Standards-compat per-kind mapping** (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act) → split across Phase A (layer-3-affecting), B/C (impl-level), D (deployment-specific).
- ~~B2 follow-on tasks~~ → **completed**: B2-followon-1 (composition-change `record` per D39) + B2-followon-2 (`state_at(sequence_n)` per D40 §A) landed.
- **D39 out-of-band-state tensions surfaced for end-of-Phase-B refinement** (per D39 "(ii) surfaced as a tension to address"): (a) manifest-declared actors loaded into state at boot bypass the event chain — `state_at(n)` pure-replay does not reflect them; (b) work-units' full records are not carried in state-change events (only `id` and status) — replay reconstructs status but not the full record. Both need either synthetic-event emission at boot (closing the loop) or explicit ledger entries before Phase B closure.
- **Phase B end-of-phase refinement** (per D14 / D34 pattern) before Phase B closure entry (analog of D25 / D35).
- **AEGIS / Axon integrity-protocol extensions** → Phase C (per D40 §B as canonical first examples).
- **Positioning** (open-source / craft-practice / accountability-bearing / methodology-layer) → deliberately deferred per `market-context.md`; revisit Phase D or later.

## Status of the existing pbs-bureau corpus

Treated as **preservation / input only**. Specific findings so far:

- `VISION.md` three axes (intertwining / sparring / authorship-preservation / defensibility / engaged-authorship): **moved from framework identity to shape policy** per D4. Practitioner-shape carries them.
- `arch/adapter.md` 5 Surfaces (Email / Accounting / MCP-Server / A2A-Peer / File-Sync): **superseded** — no specific protocols at framework-core per D2 + D17. Protocol identifiers are extension-registered.
- `arch/*` discipline mechanisms (audit / sparring / gate / authority-binding): **decomposed** per D8 — audit is state property; sparring/authority-binding are shape policy; gate is specialist+shape concern. No `discipline` kind at framework-core.
- `1-NEXT.md` F1-F4 plan: **paused** per 5-PIVOT-DECISION; further reversed by D1 (reusable framework now primary, PBS-Schulz secondary).
- Existing `arch/practitioner.md`, `arch/workflow-work-unit.md`, etc. — not yet processed against fresh-plan; treat as input when relevant.

## Branch state

- **Canonical development branch**: `fresh-plan` (locked at D36).
- **Branched from**: `step-back-evaluation` at commit `4ed5bee`.
- **Session-quirk branches**: `claude/identify-repo-S5zfO` — used by hosted-session environments that cannot push directly to `fresh-plan`. Commits land here; reconcile to `fresh-plan` at the session boundary.
- **Other branches**: `step-back-evaluation`, `lock-and-park`, `main` — earlier points; not active.

### Reconciling after a hosted session

If a prior session pushed to `claude/identify-repo-S5zfO` rather than `fresh-plan`, fast-forward `fresh-plan` locally before continuing:

```bash
git fetch origin
git checkout fresh-plan
git merge --ff-only origin/claude/identify-repo-S5zfO
git push origin fresh-plan
```

Then resume work on `fresh-plan` as canonical. If `--ff-only` fails (branches diverged), investigate before forcing — there should be no divergence under the current session policy.

## Repository layout in this branch

```
fresh-plan/
  README.md          <- this file
  decisions.md       <- the append-only ledger (D1 through current)
  market-context.md  <- adjacent products + positioning research notes (not committed positioning)
  schemas/           <- Phase A layer-3 formal schemas (D28 + workstream 3 + D34 + D39 + D40)
    README.md        <- multi-schema loading convention + identifier conventions
    _common.schema.json
    extension-manifest.schema.json
    workspace.schema.json
    actor.schema.json
    event.schema.json
    substrate.schema.json
    shape.schema.json
    adapter.schema.json
    specialist.schema.json
    work-unit.schema.json
    payload-claim.schema.json
    payload-action.schema.json
    payload-state-change.schema.json
    payload-composition-change.schema.json
    payload-lifecycle-transition.schema.json
    examples/        <- worked-example instances (validate against schemas)
  impl/              <- Phase B reference impl (per D36)
    README.md        <- install + CLI + library usage
    pyproject.toml   <- Python 3.11+; deps: jsonschema, referencing, pyyaml, click, node-semver
    src/fresh_plan/
      validator/     <- B1: conformance validator (D29 + D30 + D32 + D33)
      runtime/       <- B2: in-process substrate runtime (D7 + D10 + D13 + D19 + D20)
      cli.py         <- fresh-plan-validate + fresh-plan-run
    tests/           <- pytest; 101 tests pass (44 B1 + 57 B2)
    extensions/      <- B2 substrate extension (inprocess-substrate-ext/0.1.0)
```

## Current state (snapshot for handoff / session pickup)

- **Last ledger entry**: **D40** (extends D10 with projection / query contract + integrity-mechanism extension point; cites AEGIS as canonical first example).
- **Phase A**: closed at D35; refined by D34 + sharpened by side-quest batch D37-D40.
- **Phase B**: **in progress.** B1 + B2 + B2-followon-1 (D39 `record`) + B2-followon-2 (D40 §A `state_at(n)`) + B3 (generic minimal shape impl per D13) committed; 121 tests pass. D39 out-of-band-state tensions documented for end-of-Phase-B refinement (manifest-declared actors at boot; work-unit records carried only by id). B4 (MCP-server adapter) is next per D36 workstream order; B3/B4/B5 can also run in parallel.
- **Side-quest research**: `market-context.md` captures adjacent products + landscape map (Kore.ai, Sana AI, AEGIS, Axon, big-consultancy / vertical-startup / thought-leader / muddle-through buckets). Not committed positioning; revisit Phase D or later.
- **Open threads at handoff**: B4 (MCP-server adapter; next per D36); B5 / B6 / B7 / B8; D39 out-of-band-state tensions (manifest-declared actors at boot; work-unit record carry); end-of-Phase-B refinement (per D14 / D34); Phase B closure entry (analog of D25 / D35).

## Cleanup notes

- A YouTube transcript was used as input early in the session (commenter feedback on agent UX provided independent confirmation of axis-2-as-architecture). It has been removed; the relevant findings are captured in this README's "Working preferences" note about anti-sycophancy.
