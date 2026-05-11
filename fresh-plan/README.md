# fresh-plan

Session-procedure anchor for `fresh-plan` work. Working disciplines, patterns, ledger conventions, branch state, current snapshot. For framework orientation (what fresh-plan is, the 8 kinds, layered structure, roadmap, status of inherited corpus), see `CONCEPTS.md`. For the append-only architectural ledger, see `decisions.md`.

## Session-start procedure (Claude: follow when invoked)

**When the user has directed you to this README** (e.g., "read fresh-plan/README.md"), follow these steps in order before responding to substantive prompts:

1. **Read this README in full** — session procedure + working disciplines + ledger conventions + current state.
2. **Read `CONCEPTS.md` in full** — framework orientation: what fresh-plan is, the 8 kinds, the layered model, the roadmap, status of the inherited pbs-bureau corpus.
3. **Read `decisions.md` in full** — the append-only ledger. Each entry is locked; supersedes-relationships are explicit. Key closure entries: **D5** (layer 1 identity), **D25** (layer 2; 8 kinds), **D35** (Phase A — layer 3 formal schemas + composition rules + versioning). **D26** + **D36** name the post-Phase-A roadmap. The latest entries reflect current state; check the bottom of the file.
4. **Confirm context tightly** — in 2–3 sentences, tell the user where work stands (last decision number; current phase per D26; any explicit open threads — including Phase B impl status at `fresh-plan/impl/` if relevant). Do not summarize the entire ledger; cite by entry number.
5. **Wait for user direction** — do not jump into work. The user may have specific next steps that don't follow the obvious path.

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

Structural conventions for `decisions.md` entries, distilled from D7 / D10 / D13 / D16 / D19 / D20 / D29 / D30 / D32 / D33 / D40 (substantive) and D8 / D11 / D14 / D17 / D22 / D23 (terse clarifications). **Revisable going forward when an entry's content makes the structure awkward** — structural reason, not aesthetic preference. Convention changes apply to *future* entries only; past entries stand as written under the prior convention (append-only ledger discipline stands per the operating discipline above).

Entries fall into two shape-classes — apply the shape that fits, don't inflate a one-line clarification into a full structure or compress a substantive lock into a paragraph.

- **Substantive entries** (new kind, new contract, major mechanism, scope-defining roadmap, end-of-phase closure). Open with `## D<N> — <YYYY-MM-DD> — <one-line title>`. Then a bold `**Decision**:` paragraph stating the lock crisply. Then numbered sections (`### A.` / `### B.` / etc. — or named subsections when the entry isn't multi-axis). Then `### What is NOT in this decision` enumerating explicit deferrals + out-of-scope items. Close with `**Rationale**:` paragraph + `**Cross-references**:` line listing related D-N's. Pattern: D7 / D10 / D13 / D16 / D19 / D20 / D29 / D30 / D32 / D33 / D40.
- **Clarification / supersedes / refinement entries** (narrow scope: clarify one slot, supersede one slot of a prior entry, codify a refinement-pass finding). Open with the same `## D<N> — <YYYY-MM-DD> — <one-line title>` header (often with "Clarifies D<M>" or "Supersedes D<M>" in the title). Then a bold `**Decision (clarifies/supersedes D<M>)**:` paragraph stating the change. Optional short paragraph or named subsection if real internal structure warrants it; otherwise omit. Close with `**Cross-references**:` line. Numbered sections + "What is NOT" + multi-paragraph rationale generally NOT used — forcing them onto a narrow clarification inflates unhelpfully. Pattern: D8 / D11 / D14 / D17 / D22 / D23.
- **Worked-example inclusion.** Substantive entries (esp. those defining new contracts) include a worked example exercising the contract — either inline (`### Worked example`) or in a cited fixture / schema file. Distinct from the operating discipline "Concrete examples before locking" (which is about *grounding the thinking*) — this is about *including the example in the entry's own text* so future readers see what conformance looks like. Pattern across D29 / D30 / D32 / D33 / D40. Clarification entries typically don't need a fresh example — they cite back to the example in the entry they clarify.

## Implementation discipline (framework code)

How impl code under `fresh-plan/impl/` gets structured. Distinct from *Working patterns* (process-level) and *Ledger conventions* (entry shape) — this is about *how the code expresses the framework's contracts*.

- **Contract-driven abstraction, not DRY-driven.** When a kind contract is locked in `decisions.md` (D-entry) or `schemas/` (formal schema), the runtime impl extracts a base class / interface that *reads off the contract*. Concrete classes satisfy the base. The base exists from the *first* concrete impl, not the third — the abstraction shape is given by the contract, not by accumulated example-code.
  - Right: `class Adapter:` base reads off D16 + `adapter.schema.json`; `MCPToolAdapter(Adapter)` + `DirectAPIAdapter(Adapter)` satisfy it.
  - Right: `class Shape:` base reads off D13 + `shape.schema.json`; `GenericShape(Shape)` is one impl; `PractitionerShape(Shape)` joins in Phase D without retrofit.
  - When NOT to extract: if the "abstraction" would just name shared code without a contract-level reason (classic DRY-driven), don't. If only one concrete impl exists AND no second is imminent in the next 1-2 workstreams, the base can wait — but the extraction is a *known follow-up*, not forgotten.
  - The rule-of-three (wait for three examples) is application-code wisdom. It does NOT apply to framework code where the contract is already a priori — there the contract IS the abstraction.
- **No sunk cost on impl code.** Existing impl code (`impl/src/`, `impl/extensions/`, `impl/tests/`) is not protected from refactoring when a discipline agreement warrants restructuring. Prior commits do not grant code "lock-in" status; if convention changes mid-Phase, reorganize.
  - *Carve-out — append-only ledger.* This rule does NOT apply to `decisions.md`. Past D-entries stand as written; supersedes entries are how decisions evolve.
  - *Carve-out — convention text itself.* "Naming conventions" / "Ledger conventions" / "Implementation discipline" — convention changes apply to *future* work; whether existing in-tree references get retrofit'd in the same commit is a judgment call (typically yes for impl code; the same-commit retrofit is what makes the principle visible).

**Revisability of this section**: structural reason required — e.g., a pattern emerges that doesn't fit contract-driven-vs-DRY-driven cleanly. Not aesthetic preference. Revision = update this section + adjust in-tree code in the same commit when the principle change implies it.

---

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

## Current state (snapshot for handoff / session pickup)

- **Last ledger entry**: **D40** (extends D10 with projection / query contract + integrity-mechanism extension point; cites AEGIS as canonical first example).
- **Phase A**: closed at D35; refined by D34 + sharpened by side-quest batch D37-D40.
- **Phase B**: **in progress.** B1 + B2 (+ followons) + B3 (D13 shape, with `Shape` base + `GenericShape(Shape)`) + B4 (D16 MCP-server adapter stub, with `Adapter` base + `MCPToolAdapter(Adapter)`) + B5 (D16 direct-api adapter stub, `DirectAPIAdapter(Adapter)`) committed; 133 tests pass. Implementation discipline locked (contract-driven abstraction; no sunk cost) — `provision.py` helper extracted; base classes added in retrospect. D39 out-of-band-state tensions remain queued for end-of-Phase-B refinement. B6 (specialist) is next per D36 workstream order.
- **Side-quest research**: `market-context.md` captures adjacent products + landscape map (Kore.ai, Sana AI, AEGIS, Axon, big-consultancy / vertical-startup / thought-leader / muddle-through buckets). Not committed positioning; revisit Phase D or later.
- **Open threads at handoff**: B6 (specialist; next per D36 — Specialist base class written from the start per Implementation discipline); B7 / B8; D39 out-of-band-state tensions (manifest-declared actors at boot; work-unit record carry); end-of-Phase-B refinement (per D14 / D34); Phase B closure entry (analog of D25 / D35); real-wire MCP / direct-api integration deferred to Phase C+ (current adapters are stubs); Substrate base extraction deferred until second concrete substrate (Phase C).

## Cleanup notes

- A YouTube transcript was used as input early in the session (commenter feedback on agent UX provided independent confirmation of axis-2-as-architecture). It has been removed; the relevant findings are captured in this README's "Working preferences" note about anti-sycophancy.
