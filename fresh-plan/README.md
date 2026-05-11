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

## Session-end procedure (Claude: follow before stopping)

**When the user signals end of session, or when reaching a natural stopping boundary, run this checklist before the final message:**

1. **Working tree clean + branch reconciled + pushed.** `git status` shows no uncommitted modifications and is up to date with `origin/fresh-plan`. Any hosted-session-quirk push to `claude/identify-repo-...` reconciled per the "Reconciling after a hosted session" subsection. The 0-byte UUID-named file at repo root is an intentional session-JSONL smoke-reminder (per memory); leave it alone — don't commit, don't delete.
2. **Tests pass** (if impl work happened this session). `.venv/bin/python -m pytest -q` from `fresh-plan/impl/` is green; current count noted in the session-end message if it changed.
3. **Handoff snapshot current.** This README's "Current state (snapshot for handoff / session pickup)" section reflects: last ledger entry, current phase, current workstream, open threads. Update inline if session moves changed any of these.
4. **Forward-looking pointers tracked** per Surface-then-track + Track-with-minimum-viable-overhead. Every "deferred to X" / "future entry" / "would need a..." raised in this session has a tracked home (CONCEPTS open-questions / `<workstream>-followon-N` / commit-message reference). No orphan pointers.
5. **Stale doc audit.** Any doc *implicitly* invalidated by session work — typically `impl/README.md` after a B-workstream lands, or `CONCEPTS.md` roadmap row after a phase advances, or `decisions.md` references after a clarification entry — updated inline before the session-end message.
6. **Honest self-assessment.** Did pacing drift (e.g., many meta-commits vs feature commits)? Anything left half-finished? Surface in the final message rather than leaving for the next session to discover.

Then write the final session-end message in two distinct parts:

**Part 1 — Session summary (for the user)**. What landed, where we left off, what's the natural next move. Keep it short — the handoff snapshot in this README is the canonical state; this part is just an orientation pointer for the user.

**Part 2 — Pickup message (copy-pasteable for the next session)**. The user pastes this verbatim into a new chat to deterministically trigger the Session-start procedure. Format:

```
Read fresh-plan/README.md.

[Optional 1-sentence focus pointer. Omit entirely if no specific next-session orientation beyond "continue per handoff" — the README's Current-state section already names the next move. Include only when there's a specific question to hold, e.g., "Picking up at Bref refinement workstream" or "Decide D17 capability-vocabulary sharpening direction".]
```

The pickup message MUST start with `Read fresh-plan/README.md.` (verbatim — this is the deterministic trigger for the Session-start procedure). Surface it as a clearly-marked code block in the session-end message so the user can copy-paste cleanly. Per `feedback_pickup_message_minimal.md` memory: 1–3 sentences max total; don't re-derive what the README/CONCEPTS/decisions.md already carry (signals doubt that they're in good state when they are).

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
- **Surface-then-track.** Every time a response contains forward-looking language ("deferred to Phase X", "future ledger entry", "would need a DSL / mechanism", "currently opaque — real semantics later", "TBD when Y arrives"), pair it with a concrete tracking proposal in the same response: where to persist (CONCEPTS open-questions / `<workstream>-followon-N` / candidate D-entry / commit-message follow-on flag) + proposed wording. Don't drop the pointer and carry on — the other party can't catch every one in real time; orphan pointers accumulate. Symmetric rule: every "this is deferred to X" pairs with "tracked here: [location]", or an explicit justification for why no tracking is needed (already-covered, too speculative-to-name).
- **Track with minimum-viable overhead.** Composes with Surface-then-track: pick the *lightest* persistence form that survives — commit-message reference < `<workstream>-followon-N` < CONCEPTS open-questions bullet < candidate D-entry — in ascending order of overhead. Don't auto-escalate to the heaviest form. The bar is "findable when it becomes load-bearing", not "tracked maximally now." Over-tracking drifts toward bookkeeping (multiple commits in a row producing no impl progress); under-tracking drops items. Calibrate to load-bearing-ness + when-it-will-matter.
- **Side-quest persistence rule.** Research, positioning, landscape analysis, competitive notes, vision-framing analysis → `market-context.md` (or similar research file). New ledger entries (D-N) *only* for architectural decisions. Positioning is deliberately deferred per discipline; keeping research separate from the ledger separates "thinking we do" from "decisions we lock."
- **Generic vs pioneer-instance discipline.** When building "generic" exemplars per D26 (e.g., B3's generic-shape impl), keep them deliberately neutral. Don't accidentally bake in pioneer-specific opinions. D26 explicitly says B3 is NOT practitioner-shape; the bias-avoidance is load-bearing for Phase E shape-neutrality validation.
- **Fixture vs canonical artifact placement.** Test fixtures (`impl/tests/fixtures/`) are *disposable test inputs*, not canonical artifacts. Canonical artifacts (substrate impls, shape impls, adapter impls) live at `impl/extensions/`. Don't promote a fixture to canonical without intent; don't duplicate work between the two. Example: `min-shape-ext` under B2 fixtures is a test-only minimal shape; the B3 generic-shape impl is a separate canonical artifact under `impl/extensions/`.
- **Steelman-then-resolve.** When a competing alternative surfaces (Kore.ai's orchestrator-vs-worker per D37; Sana's knowledge-as-core per D38; AEGIS-at-core per D40; the `extends` slot per D31; etc.), steelman it honestly + name it explicitly in the rejection rationale. The defense is part of the lock; future readers don't re-open the question. Pattern shape: D8 / D17 / D31 / D37 / D38 / D40.
- **Radical-autonomy framing as stress-test, not roadmap.** Periodically pressure-test fresh-plan's positioning against the strong-form "agents fully discover + self-organize structural work; humans become signees" scenario. Use it to avoid painting corners (composition rules should permit runtime discovery; event chain should be capability-card-compatible; etc.). But do not *position for* it — no Bucket A platform with shipping power (Gemini Enterprise, Microsoft Copilot Studio, Salesforce Agentforce, IBM watsonx, Kore.ai) publicly targets that scenario. Their actual stated direction (agents + orchestration + protocols + governance + persistent human-in-the-loop) is *more* friendly to fresh-plan's accountability-bearing positioning, not less. Position for the stated direction; use the radical extrapolation as periodic stress-test of architectural choices, not as the bet. Compose with the "Honest naming" + "Steelman-then-resolve" patterns.

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

- **Last ledger entry**: **D44** (extends D37 — queued subscriber-dispatch + loop backstop). Latest substantive Bref output to date.
- **Phase A**: closed at D35; refined by D34 + sharpened by side-quest batch D37-D40.
- **Phase B**: **impl side complete; Bref in progress; closure entry remaining.** B1 + B2 (+ followons) + B2b + B3 + B4 + B5 + B6 + B7 + B8 (D36 §C closure-criterion items 1–6 satisfied) committed; **168 tests pass**. Implementation discipline locked. All planned base classes extracted (Shape, Adapter, Specialist, Substrate). All planned vocabulary-registrations landed (work-unit.kind, adapter.protocol-or-transport). **Bref progress this session: 3 of 7 deliverables landed** (D39 closed impl-side; D43 rename `event-streaming` → `event-chain`; D44 queued dispatch). Then Phase B closure entry (analog of D25 / D35).
- **Side-quest research**: `market-context.md` captures adjacent products + landscape map (Kore.ai, Sana AI, AEGIS, Axon, big-consultancy / vertical-startup / thought-leader / muddle-through buckets). Not committed positioning; revisit Phase D or later.
- **Open threads at handoff**: **Bref (Phase B refinement workstream per D42)** — 4 of 7 deliverables remaining (canonical list in `CONCEPTS.md` open-questions): **(4) D19 activation-scope DSL design** *(wrinkle — needs Phase D pioneer activation expressions as concrete input; designing-in-the-abstract risks doing work Phase D will redesign; lean toward a deferral entry naming the Phase D home rather than sketch-now-lock)*; **(5) D33 migration-safety discipline** for shape versioning (policy text); **(6) D38 Sana-style worked-example validation** (validation artifact); **(7) `decisions.md` split** (mechanical, last). Plus three candidate standalone clarification entries (actor identity-binding slot, live in-place shape migration scope-cut, positioning lock — last needs source-grounded Bucket A platform reads first). Bref output = one substantive D-entry analogous to **D34** (Phase A's refinement output — structural template). Then **Phase B closure entry** analogous to **D35**. Real-wire MCP / direct-api / MS Agent Framework integration deferred to Phase C+.
- **Cross-session input — standards-compat engagement** (surfaced from another session's read of `event_chain.py` + `event.schema.json`): correctly diagnosed pure event-sourcing (no sidecar) + framework-can't-be-a-library. Proposed CloudEvents envelope alignment + W3C PROV-DM citation/export. **Both are already on D24's standards-compat tracker** (CONCEPTS line 142): (i) PROV-O event-chain mapping + (ii) CloudEvents envelope alignment, both flagged "Phase B-affordable; most are Phase C natural home." **Decision deferred to next session**: do we (a) lock a small standalone clarification entry citing PROV-DM + naming CloudEvents alignment as priority (lightweight; useful for external defensibility narrative); (b) formalize a parallel "standards-compat per-kind mapping" workstream analogous to D42 Bref formalization (heavier); or (c) leave on the CONCEPTS tracker and revisit at Phase C planning. Lean (a) or (c); (b) feels like over-formalization. Note: CloudEvents alignment is a **D43-class-but-larger** rename refactor (`payload-subtype` → `type`, `timestamp` → `time`, new `source` slot, `data` envelope), worth its own session + own substantive D-entry — NOT piggybacking onto Bref. PROV-JSON export adapter is Phase C deliverable per D24, not Bref.

## Cleanup notes

- A YouTube transcript was used as input early in the session (commenter feedback on agent UX provided independent confirmation of axis-2-as-architecture). It has been removed; the relevant findings are captured in this README's "Working preferences" note about anti-sycophancy.
