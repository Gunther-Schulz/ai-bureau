# fresh-plan

Append-only decision ledger for a fresh framework dev plan, started 2026-05-08 on branch `fresh-plan`.

## What this is

A clean restart of framework architectural decisions. The existing `pbs-bureau` corpus (VISION, ARCHITECTURE, MAINTENANCE, GLOSSARY, arch/*, profiles/*, plugin/*, pbs/*, 1-5 numbered docs at repo root) is treated as **input, not as anchor**. Each prior artifact's status (inherit-as-is / inherit-with-modification / re-derive / discard / defer) is itself a future ledger decision.

The fresh-plan reverses the prior `5-PIVOT-DECISION.md` (which had paused the framework and made PBS-Schulz primary). Per D1: **reusable framework is primary; PBS-Schulz is the first deployment / proving ground; generality wins on conflict.**

## Reading order for a fresh session

1. **This README** — context + conventions.
2. **`decisions.md`** — the full ledger, D1 through closure (currently D25 = layer-2 close).
3. *(Optional, as background)* — `1-NEXT.md` through `5-PIVOT-DECISION.md` at repo root: prior planning trail. Superseded by D1; treat as input only.
4. *(Reference, when needed)* — pbs-bureau corpus files (`VISION.md`, `ARCHITECTURE.md`, `arch/*.md`, etc.). **Not** anchoring constraint; consult only as input when explicitly relevant.

## Key procedural conventions

- **Append-only**: entries are locked once added. Override = new entry that explicitly supersedes. Never edit a locked entry's substance; clarifications go in follow-up entries.
- **One question at a time**: discussion proceeds question by question; each answer locks before the next is opened.
- **Concrete examples before locking**: substantive decisions are grounded with worked examples that exercise the contract before the entry is written.
- **Multiple passes for substantive findings**: when a finding has cascading effects, do honest passes (solidify or refute) before locking.
- **Rolling refinement (option C)**: clear-now findings get supersedes/clarification entries when surfaced. The named refinement pass per D14 catches cross-cutting and late-emerging findings at closure of each layer.
- **Commit and push regularly**: each lock ≈ one commit, pushed to `origin/fresh-plan`. The session-stop hook complains about uncommitted/untracked files.

## Working preferences (observed during session)

- **Be honest, not sycophantic** — push back when something is wrong; don't agree just to agree. (Anti-sycophancy as architecture, not prompt — independent confirmation found in commenter feedback during the session.)
- **Surface tensions explicitly** — name when something feels off; don't paper over.
- **Tight responses** — concise communication; tables and bullets where they help.

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

## Open questions / next-decision candidates (post-D25)

1. **When to begin layer 3** (extension protocol + formal schemas).
2. **Open tension from D1**: PBS-Schulz daily work cannot pause while the reusable framework is built. A rule for "what runs PBS-Schulz daily during the rebuild" is needed at some point.
3. **Branch / commit strategy** going forward — `fresh-plan` is the live development branch; relationship to other branches (`step-back-evaluation`, `lock-and-park`, `main`) needs deciding when fresh-plan output stabilizes.
4. **Verification targets carried forward** to layer 3 + impl:
   - D21 workspace-as-A2A-peer deployability.
   - MCP-server-exposure parallel.
   - Standards-compatibility per-kind mapping for in-scope standards (PROV-O, VC, DID, CloudEvents, OpenTelemetry, AsyncAPI, JSON Schema, Activity Streams, EU AI Act compliance — per D24).
5. **Deferred refinement-pass candidates** — only revisit if downstream impl work surfaces concrete need:
   - Optional `parent-actor` slot on actor (D9) for sub-agent parent-child queries.
   - Workflow as containment hierarchy on work-unit.

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
