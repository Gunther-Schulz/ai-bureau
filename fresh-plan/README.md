# fresh-plan

Append-only decision ledger for a fresh framework dev plan, started 2026-05-08 on branch `fresh-plan`.

## Session-start procedure (Claude: follow when invoked)

**When the user has directed you to this README** (e.g., "read fresh-plan/README.md"), follow these steps in order before responding to substantive prompts:

1. **Read this README in full** — context + conventions + status + working preferences.
2. **Read `fresh-plan/decisions.md` in full** — the append-only ledger D1 through current. Each entry is locked; supersedes-relationships are explicit; the closure entry (D25) names the layer-2 final kind set; D26 names the post-layer-2 roadmap.
3. **Confirm context tightly** — in 2–3 sentences, tell the user where the work stands (last decision number; current layer / phase per D26; any explicit open threads). Do not summarize the entire ledger; cite by entry number.
4. **Wait for user direction** — do not jump into work. The user may have specific next steps that don't follow the obvious path.

Throughout the session, follow the **procedural conventions** + **working preferences** below.

## Operating disciplines (load-bearing during session)

- **Append-only ledger.** Entries in `decisions.md` are locked once added. Override = new entry that explicitly supersedes the prior. Never edit a locked entry's substance; clarifications go in follow-up entries.
- **One question at a time.** Discussion proceeds question by question. Each question is answered (or deliberately deferred) before the next is opened. Don't batch unrelated questions.
- **Concrete examples before locking.** Substantive decisions are grounded with worked examples that exercise the contract before the entry is written. Don't write a decision entry from pure abstract reasoning when a concrete scenario is available.
- **Multiple passes for substantive findings.** When a finding has cascading effects (e.g., the strict protocol-neutrality finding in D16), do honest passes — solidify or refute — before locking. Single-pass on big findings is unsafe.
- **Rolling refinement (option C).** Clear-now findings get supersedes / clarification entries when surfaced (rather than accumulating until a closure pass). The named refinement pass per D14 catches cross-cutting and late-emerging findings at end-of-layer.
- **Commit and push regularly.** Each substantive lock ≈ one commit, pushed to `origin/fresh-plan`. The session-stop hook complains about uncommitted/untracked files and will block stop until clean.

## Working preferences (observed during prior session)

- **Be honest, not sycophantic.** Push back when the user's claim is wrong; don't agree just to agree. (This is also load-bearing in the framework — D24's standards-compatibility check + the anti-sycophancy theme that emerged from input research during the early session.)
- **Surface tensions explicitly.** Name when something feels off; don't paper over.
- **Tight responses.** Concise communication; tables / bullets where they help; no padding.
- **Cite decisions by number** (D1, D7, D16, etc.) rather than summarizing them inline. The ledger is the canonical reference.

---

## What this is (background)

A clean restart of framework architectural decisions. The existing `pbs-bureau` corpus (`VISION.md`, `ARCHITECTURE.md`, `MAINTENANCE.md`, `GLOSSARY.md`, `arch/*`, `profiles/*`, `plugin/*`, `pbs/*`, 1-5 numbered docs at repo root) is treated as **input, not as anchor**. Each prior artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

The fresh-plan reverses the prior `5-PIVOT-DECISION.md` (which had paused the framework and made PBS-Schulz primary). Per D1: **reusable framework is primary; PBS-Schulz is the first deployment / proving ground; generality wins on conflict.**

## Layered structure (per D3)

| Layer | Content | Status |
|---|---|---|
| **Layer 1 — identity** | I1 composition system / I2 machine-checkable contracts / I3 accountability-bearing AI-human work. No substantive identity at core; substantive identity carried by shapes per D4. | Closed at D5. |
| **Layer 2 — kinds** | 8 kinds (workspace D7, actor D9, event D10, substrate D12, shape D13, adapter D16, specialist D19, work-unit D20). | Closed at D25. |
| **Layer 3 — extension protocol + formal schemas** | Per-kind formal schemas (concrete enough to validate, format-neutral). Extension declaration mechanism. Composition / promotion / demotion rules. | **Not started.** Non-optional for impl work. |
| **Implementation (below layer 3)** | Format / serialization choices; storage / wire / protocol mechanisms; specific extension impls (substrate impls, shape impls, adapter impls, specialist impls). | Out of scope for framework-core work. |

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

| Phase | Work | Closes when |
|---|---|---|
| **A — Layer 3** | Formal schemas per kind; extension declaration mechanism; composition / promotion rules; JSON Schema toolchain | Layer-3 closure analogous to D25 |
| **B — Reference impl of core** | Generic substrate / shape / adapters / specialist; minimal RAG-via-MCP | Reference impl boots end-to-end |
| **C — Standards-compat impl** | A2A peer adapter; MCP server adapter (validates D21) | Peer + MCP-server demonstrably work |
| **D — Pioneer-instance (PBS-Schulz)** | Practitioner-shape; domain specialists; bauleitplanung corpus; PBS-Schulz workspace manifest; cutover from 0.1.0 plugin | PBS-Schulz running on framework end-to-end |
| **E — Multi-deployment validation** | Second shape impl; second workspace; federation begins | Two distinct deployments coexist |
| **F+** | Refinement / optimization / ecosystem | Indefinite |

## Open questions / deferred items (with phase placement)

Per D26, deferred items have implicit phase homes:

- **D1 open tension** (PBS-Schulz daily during rebuild) → resolved in Phase D.
- **Optional `parent-actor` slot on actor** → revisit in Phase A or B if sub-agent patterns surface concrete need.
- **Workflow as containment hierarchy on work-unit** → Phase D (pioneer) or E (multi-deployment) if forced.
- **Branch / commit strategy** → after fresh-plan stabilizes (likely during Phase A).
- **D21 verification targets** (A2A peer + MCP server) → Phase C.
- **Standards-compat per-kind mapping** (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act) → split across Phase A (layer-3-affecting), B/C (impl-level), D (deployment-specific).

## Status of the existing pbs-bureau corpus

Treated as **preservation / input only**. Specific findings so far:

- `VISION.md` three axes (intertwining / sparring / authorship-preservation / defensibility / engaged-authorship): **moved from framework identity to shape policy** per D4. Practitioner-shape carries them.
- `arch/adapter.md` 5 Surfaces (Email / Accounting / MCP-Server / A2A-Peer / File-Sync): **superseded** — no specific protocols at framework-core per D2 + D17. Protocol identifiers are extension-registered.
- `arch/*` discipline mechanisms (audit / sparring / gate / authority-binding): **decomposed** per D8 — audit is state property; sparring/authority-binding are shape policy; gate is specialist+shape concern. No `discipline` kind at framework-core.
- `1-NEXT.md` F1-F4 plan: **paused** per 5-PIVOT-DECISION; further reversed by D1 (reusable framework now primary, PBS-Schulz secondary).
- Existing `arch/practitioner.md`, `arch/workflow-work-unit.md`, etc. — not yet processed against fresh-plan; treat as input when relevant.

## Branch state

- **Current development branch**: `fresh-plan`
- **Branched from**: `step-back-evaluation` at commit `4ed5bee`
- **Other branches**: `step-back-evaluation`, `lock-and-park`, `claude/identify-repo-S5zfO`, `main` (all at varying earlier points; not active)

## Repository layout in this branch

```
fresh-plan/
  README.md       <- this file
  decisions.md    <- the append-only ledger (D1-D25 currently)
```

## Cleanup notes

- A YouTube transcript was used as input early in the session (commenter feedback on agent UX provided independent confirmation of axis-2-as-architecture). It has been removed; the relevant findings are captured in this README's "Working preferences" note about anti-sycophancy.
