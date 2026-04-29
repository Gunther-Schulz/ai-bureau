# Session handoff — pbs-bureau

End of session 7 (2026-04-29). This session expanded the pre-RAG
architectural commitments from session 6's three (state.md gate +
audit-trail-v1 + sparring-v1) to **twelve**, driven by sharper
review of where session-6 commitments left load-bearing legacy in
place. Three reversals/extensions, three new mechanisms, a
late-session pattern-vs-instance discipline + best-effort split
work item (#9) from a meta-vision discussion about the AI-office
builder, two market-context-driven additions (#10 A2A schema
gate, #11 Cowork as primary end-user runtime) after researching
Claude Connectors / MS Agent Framework 1.0 / Gemini Enterprise
Agent Platform / Claude Cowork, and a final session-end insight
(#12 Office-vs-department modularization) after deep comparison
with Anthropic's open-source `knowledge-work-plugins` repo +
brand-voice partner-built plugin — recognizing that PBS today
conflates "office" with "single department." Plus a corrective
overselling check that produced an honest market-context section
in the v2 builder ROADMAP entry.

**Critical session-end pivots**:
- Commitment #11 (Cowork integration) revised from 1-2 sessions
  to 3-5 sessions under "deep + complete integration, no sunk
  costs" directive — full adoption of Anthropic's plugin shape
  including slash commands as primary user surface, plugin agents
  formalized (lifted from deferred-to-v1+), `pbs.local.md`
  migration from `office-config.yaml`, etc.
- Commitment #10 (A2A schema gate) pulled to **position 1** in
  the pre-RAG queue — smallest commitment, informs every
  downstream schema decision.

**Recommended next-session order**: **#10 (A2A) first → #12
(department modularization) → #11 (deep Cowork integration)**,
then resume #6/#7/#9/#8/C/D queue.

**Phase 1 — task A retrofit (state.md gate)**:
- 8 skills (orchestrator, survey-project, draft-cover-mail,
  validate-checklist, review-draft, draft-textteil-b/c,
  promote-to-skill) declare `get_project_state` /
  `update_project_state` in `mcp_tools_required` + route through
  the gate. Direct Read/Write of state.md eliminated.
- Audit slice 14 verification: clean.

**Phase 2 — fail-closed corollary** (meta-rule 4 reads-side
symmetry): when MCP is unreachable, contract-bearing reads MUST
surface to user and stop, never bypass via direct filesystem
Read. Decision record `mcp-fallback-policy.md` + ARCHITECTURE.md
v0.6 → v0.7 + slice 14 brief extended with violation pattern 5
(declared fail-open in fallback strings). Plugin-wide sweep:
all 19 skills' `fallback_when_mcp_absent` rewritten under the
rule.

**Phase 3 — trigger convention simplification**: old
`{phrase, lang}` structured form retired for flat concept
labels. LLM matches semantically across languages without
explicit translation pairs. Decision record `trigger-convention.md`.
Plugin-wide sweep: all 19 skills' triggers collapsed to concept
labels. German technical anchors preserved (UNB, Stellungnahme,
Festsetzungen).

**Phase 4 — audit-trail v1 → v2 reversal**: dual-write discipline
retired for single-write architecture. Decision record
`audit-trail-v2.md` (supersedes v1). Skills call
`record_audit_event` only; gate-side `record_decision` MCP tool
atomically mirrors to `decisions.md`. Five prose sources retired
(`module-decisions.md`, `correspondence-log.md`, references
`changelog.md`, `state.md.phase_history` field) — render-time
prose synthesis via new `render_audit_trail` MCP tool. Two stay:
`decisions.md` (legal-defense provenance) + `snapshots/`
(artifact bytes).

**Phase 5 — design-review target 9 + audit slice 18 (Subsumption
+ Legacy Retirement)**: the audit-trail v1→v2 reversal exposed a
generic gap — adding new mechanisms without explicitly asking
"what does this subsume?" leaves load-bearing legacy in place
by inertia. Target 9 makes the question MANDATORY at design
time (prospective check); slice 18 catches what target 9
missed (retrospective sweep across all decision records,
ARCHITECTURE entities, plugin entities).

**Phase 6 — bootstrap-write tools promotion**: `author-manifest`
+ `setup-office` currently scaffold contract-bearing files via
direct Write. Promoted from v1.x ROADMAP to pre-RAG commitment
#7. Sketches: `create_manifest` + `create_office_config` MCP
tools wrap the loader for first-write through the gate.

**Phase 7 — pre-action framing skill (new pre-RAG commitment
#8)**: completes the prep → implementation → review cycle.
Today's meta-skills (audit, design-review) are post-action only;
new skill (working name `frame-task` / `scoping`) fires before
non-trivial work to surface scoping/approach/constraints/success.
Pre-RAG-worthy because it's preventive of design errors that
compound after launch.

**Phase 8 — pattern-vs-instance discipline + commitment #9 (late-
session, after AI-office-builder vision discussion)**:

- **AI-office builder long-horizon vision** added to `ROADMAP.md`
  v2: a meta-skill that takes a domain spec + accumulated
  architectural patterns + infrastructure templates and scaffolds
  complete working AI offices for any knowledge-work domain
  (legal practice, research, engineering, medical, regulatory,
  etc.). PBS becomes one instance of a pattern; the builder
  produces more instances. Distinct from the v1.x library-reuse
  story (audit + design-review extraction): builder is generative
  reuse.
- **Pattern-vs-instance discipline** added to `ARCHITECTURE.md`
  (v0.7 → v0.8): every architectural commitment must work at
  pattern level (test: would this work for hypothetical legal-
  practice / research-paper-review / engineering-doc office?),
  not just for PBS. PBS is the pioneer instance per VISION.md;
  the architecture is the pattern. Connected to all session-7
  commitments — they were pattern-level by construction; the
  discipline makes that property explicit and load-bearing.
- **Single-domain-pioneer constraint analysis**: empirical 2-3-
  hand-instances validation is wrong for this constraint (user
  is planning-domain expert, won't authentically build offices
  in other domains). Working method is best-effort split via
  careful reasoning + immediate PBS-regression validation
  (signal #1) + deferred-possibly-indefinite second-domain
  validation (signal #2).
- **Commitment #9 — Pattern-vs-instance best-effort split**:
  reasoning + implementation + PBS regression validation, all
  bundled. 1-2 sessions of dedicated work. Outputs: refactored
  schemas (ProjectState core/extension split, office-config
  core/extension split, doctype-manifest generalization),
  retrofitted skills, passing PBS tests, documented split
  rationale per commitment so a future second domain can
  validate the reasoning rather than redo it.
- **Design-review target 10 (Pattern-vs-instance check,
  prospective)** + **audit slice 19 (Pattern-vs-instance scan,
  retrospective)**: same prep-vs-review pairing as target 9 +
  slice 18. Catches PBS-coupling at pattern layer at design time
  (target 10) and across the whole stack retrospectively (slice
  19).
- **VISION.md extended**: pioneer-instance milestones now
  include "First office *generated by an AI-office builder*
  rather than hand-built" — the long-arc endpoint of the pioneer
  framing.
- **plugin/CLAUDE.md** — pattern-vs-instance discipline summary
  pointing at ARCHITECTURE for full rule.

**Plus ROADMAP additions** (deferred but tracked):
- **Generalize + publish domain-agnostic skills** (priority
  clarified mid-session): primary scope is `audit` +
  `design-review` (most clearly domain-agnostic, battle-tested
  as session quality framework). Secondary candidates
  (watch-list, memory-record pattern, orchestrator infrastructure,
  promote-to-skill, backend) listed under "under consideration"
  — interesting but uncommitted, needs empirical battle-test
  before splitting.
- **AI-office builder** (v2 long-horizon vision): generative
  reuse — meta-skill that scaffolds new domain offices from
  spec + patterns. Distinct from library reuse above.

The session 7 commitment count went from 3 (session 6's) to 9
pre-RAG items. Phase 1 corpus download deferred until all 9
land. Cleanest framing: this session was the architectural
hardening BEFORE first project bind, not a delay of RAG.

---

## Read order for next session

1. **This file (HANDOFF.md)** — current state
2. **`ARCHITECTURE.md`** — **v0.8** post-session-7. Meta-rule 4
   gained a fail-closed-for-reads corollary (symmetric with the
   write-side persistence boundary). New "Pattern-vs-instance
   discipline" + single-domain-pioneer validation strategy
   (added as meta-discipline before the meta-rules). 4 meta-rules
   + scope-orthogonality layering convention, 5 entity types,
   Memory now has 4 sub-kinds (prose, records, audit-log,
   audit-log-v2-canonical).
3. **`docs/decisions/`** — three new session-7 decision records:
   - `mcp-fallback-policy.md` (fail-closed corollary)
   - `trigger-convention.md` (concept labels, semantic match)
   - `audit-trail-v2.md` (single-write, supersedes v1)
   - Plus session-6 records still authoritative (sparring-output-v1,
     audit-trail-v1 with SUPERSEDED header, backend records)
4. **`ROADMAP.md`** — **9 pre-RAG v1 commitments at the top**
   (was 8; commitment #9 added late-session). Generalize-and-
   publish entry in v1.x (priority clarified to primary =
   audit + design-review only). AI-office builder v2 long-horizon
   vision entry.
5. **`docs/plugin-conventions.md`** — §11 (triggers convention) +
   §11b (fail-closed fallback policy with anti-patterns + writing
   rules for `fallback_when_mcp_absent`)
6. **`VISION.md`** — extended: pioneer-instance milestones include
   "First office generated by AI-office builder"; new section
   "The pioneer-instance commitment as architectural discipline"
   linking VISION → ARCHITECTURE pattern-vs-instance discipline.
7. **`docs/audits/`** — session-6 first-runs + session-5 audit-pre-rag
8. **`docs/design-reviews/`** — session-6 target-8 first run +
   session-5 foundations-20260429
9. **`docs/rag-pipeline-decisions.md`** — Phase 0/1/2/3/4 phasing
10. **`docs/backend-conventions.md`** — Backend idioms
11. **`plugin/CLAUDE.md`** — meta-rule 4 summary now includes the
    fail-closed corollary one-liner; new "Pattern-vs-instance
    discipline" section pointing at ARCHITECTURE for full rule
12. **`plugin/skills/audit/`** — **0.8.0** (slices 1-16 + 18 + 19;
    surfaces 1-12; slice 17 still deferred per audit-trail-v2
    simplification; brief extended with violation pattern 5)
13. **`plugin/skills/design-review/`** — **0.7.0** (targets 1-10)
14. **`plugin/skills/orchestrator/`** — **0.10.0** (state.md gate
    routed; references/state-format.md still reflects v1 layout
    — needs update to v2 once dropped sources actually retire)
15. All other 16 skills — single-bumped per session-7 changes (see
    "Skill versions snapshot" below)

---

## ⏳ Pre-RAG gating items (12 commitments, post-session-7 state)

The 12 v1 commitments enumerated in ROADMAP.md "v1 commitments"
section. **Revised recommended execution order** (session-7
late-insight pivot, with A2A pulled to position 1):

```
Session 8:    #10 (A2A schema gate decision)                  1 session
Session 9:    #12 (department modularization design)          1 session
Session 10-13: #11 (deep Cowork integration refactor)         3-5 sessions
Session 14+:  #6 → #7 → #9 → #8                               per existing queue
              C (sparring-output integration)
              D (plugin version bump)
Then:         Phase 0 items 4 + 5 → Phase 1 corpus
```

**Why #10 first**: smallest commitment (~half-day to 1 session,
decision + minor schema additions). Informs every downstream
schema decision — #6 audit-trail v2 (AuditEvent shape), #7
bootstrap-write tools (interface shape), #9 pattern-vs-instance
split (which schemas need A2A-friendly identity), #12 department
identity (departments may communicate via A2A internally). Doing
A2A last means risk of schema refactor on every prior item.

**Why #12 second**: department-aware namespacing affects slash
commands (#11 work) AND skill frontmatter conventions. Doing
#11 without #12 means redoing slash command names + skill fields
once departments land. #12 also wants to know A2A decisions
(whether departments are A2A-shape agents internally), so #10 → #12
order makes sense.

**Why #11 third (3-5 sessions)**: "deep + complete integration,
no consideration for sunk costs" directive (session 7). Adopt
Anthropic's plugin shape wholesale where it differs — slash
commands as primary surface, plugin agents formalized,
`pbs.local.md` migration, etc.

**Why #6/#7/#9 after**: building audit-trail v2 + bootstrap-write
tools + pattern-vs-instance refactor on the old shape, then
refactoring under deep Cowork integration, would be cost-heavier
than landing the new shape first.

### Already shipped session 6 + 7 (architectural backstops only)

1. ✅ **Unified audit trail** — schema + Pydantic + 2 MCP tools
   shipped session 6 (per v1). v2 reversal (session 7) makes the
   skill-side simpler than originally planned.
2. ✅ **Sparring-output structural promotion** — schemas + MCP tool
   + plugin-conventions field shipped session 6.
3. ✅ **State.md MCP gate** — Pydantic + 2 MCP tools shipped
   session 6. **Skill retrofits done session 7.**
4. ✅ **Fail-closed corollary** — done session 7 (decision record
   + meta-rule 4 corollary + slice 14 brief + 19-skill sweep).
5. ✅ **Trigger-convention simplification** — done session 7.

### Remaining for next-immediate-session-before-RAG

6. **Audit-trail v2 retrofit** (per `audit-trail-v2.md`):
   - **Backend**: build `record_decision` MCP tool (atomic
     dual-write inside the gate); build `render_audit_trail` MCP
     tool (deterministic prose synthesis). Add
     `user_confirmation` event kind to AuditEvent; expand
     `decision`/`module_decision` `details` to require
     `reasoning_full_text`. Drop `phase_history` field from
     ProjectState; write migration script.
   - **Skills**: orchestrator + save-baustein + record-feedback
     + draft-textteil-b/c + review-draft + research-references
     declare `record_audit_event` (and `record_decision` where
     applicable) in `mcp_tools_required` + invoke at appropriate
     checkpoints. **Single-write per v2** — NO dual-write to
     prose sources from skills.
   - **Migration**: `backfill_audit_trail` walks legacy prose
     sources, emits events, optionally retires the subsumed source
     files after round-trip render comparison. Today: zero
     projects bound; backfill is academic until first-bind.

7. **Bootstrap-write MCP tools** (per ROADMAP commitment #7):
   - Build `create_manifest` + `create_office_config` MCP tools
     (Pydantic-validated first-write through loader; replace
     direct Write).
   - Skill retrofits: `author-manifest` + `setup-office` declare
     the new tools in `mcp_tools_required` + use them in body.
     Drop the "known bypass" caveat from fallback strings.
   - Audit slice 14 re-run after retrofit confirms no remaining
     contract-bearing direct Write.

8. **Pre-action framing skill** (per ROADMAP commitment #8):
   - Design + scaffold a new meta-skill (working name
     `frame-task` or `scoping`).
   - Triggered on non-trivial task starts (orchestrator routes
     here before routing to implementation specialists).
   - Outputs a brief framing artifact (problem, scope, approach,
     constraints, success-criteria) that implementation skills
     consume.
   - **Order note**: schedule AFTER #9 — the framing skill
     codifies the pattern-vs-instance reasoning produced by #9
     into a repeatable check.
   - Decision: build skill bundle (SKILL.md + references/);
     decide if it warrants a PROCEDURE.md (probably yes — phase
     gates).

9. **Pattern-vs-instance best-effort split** (per ROADMAP
   commitment #9):
   - **Reasoning + implementation + PBS regression validation**,
     bundled. 1-2 sessions; could be small (semantic) or large
     (structural) refactor — won't know until the reasoning pass
     surfaces what needs changing.
   - **Targets**: `ProjectState` core/extension split;
     `office-config` core/extension split; doctype-manifest
     schema generalization; review MCP tool interfaces for
     PBS-coupling; review decision records for pattern-level vs
     PBS-only framing.
   - **Output**: refactored Pydantic + skill retrofits + passing
     PBS tests + `pattern-vs-instance-split-rationale.md`
     documenting per-commitment reasoning.
   - **Order note**: schedule AFTER #6 + #7 (so #9 examines
     stable post-v2 schemas + bootstrap-write tool interfaces);
     BEFORE #8 (#8 codifies #9's reasoning).
   - **Validation**: signal #1 (PBS regression passes) is the
     immediate empirical check. Signal #2 (right-boundary
     validation across domains) waits for second-domain
     implementation, possibly indefinite. Working method is
     best-effort split per single-domain-pioneer constraint.

10. **A2A schema compatibility + Gemini Enterprise pattern
    emulation decision gate** (per ROADMAP commitment #10) —
    **POSITION 1** (pulled forward, session 7 late insight,
    expanded session-7-final to include proactive emulation):
    - Two-sided decision gate:
      - **(A) Defensive — A2A-shape compatibility**: AuditEvent
        / ProjectState / MCP server get A2A-shape-compatibility
        additions now (cheap pre-RAG) vs deferred (expensive
        once data accumulates).
      - **(B) Proactive — Gemini Enterprise pattern emulation**:
        which Google archetypal choices to adopt *now* in our
        single-big-model archetype (per row of comparison table
        in v2 "Gemini Enterprise migration path" section). Per-
        row decisions: orchestrator/internal-A2A-shape,
        backend/HTTP-MCP, persistent-state/office-memory-concept,
        cross-department-workflow/A2A-internal-messages, audit-
        trail/agent-identity, governance/data-classification +
        Model-Armor + Agent-Simulation analogues.
    - Output: `docs/decisions/a2a-and-gemini-pattern-emulation.md`
      documenting both sides per row.
    - Scope: 1 session (was ~half-day; expanded for proactive
      emulation per row of comparison table).
    - Order rationale: smallest commitment, informs every
      downstream schema decision (#6 AuditEvent, #7 bootstrap-
      write tool interfaces, #9 pattern-vs-instance split, #12
      department identity + cross-department messaging shape,
      #11 Cowork agent identity). First in pre-RAG queue.

11. **Cowork as primary end-user runtime — DEEP integration**
    (per ROADMAP commitment #11, revised session-7 late under
    "no sunk costs" directive) — **POSITION 3**:
    - Cowork natively supports MCP + Skills + Plugins. Anthropic
      ships open-source `knowledge-work-plugins` repo (cloned
      to `~/dev/reference/knowledge-work-plugins/`) with 11
      domain plugins + 5 partner-built plugins.
    - **Scope directive**: deep + complete integration. Adopt
      Anthropic's plugin shape wholesale where it differs from
      ours. No preservation of current implementations just
      because we built them.
    - **Concrete work items** (3-5 sessions total):
      - Plugin shape: `.mcp.json`, `marketplace.json`,
        `CONNECTORS.md`, polished README
      - Slash commands as primary user surface, department-
        namespaced (`/planning:draft-begruendung`, etc.)
      - Plugin agents formalized (lift from deferred-to-v1+):
        `research-references-fetcher`, `audit-slice-runner`,
        `design-review-target-runner`
      - Migrate `office-config.yaml` → `pbs.local.md`
      - Skill frontmatter alignment (their fields + our extras
        + `<example>` blocks + `department:` field per #12)
      - **Test in actual Cowork** (not just Claude Code) —
        end-to-end deploy + workflow test
    - Output: `docs/decisions/cowork-deployment.md` + extensive
      refactor work touching every user-facing surface.
    - Order: AFTER #12 (department namespacing); BEFORE
      #6/#7/#9/#10 if possible (so audit-trail v2 + bootstrap-
      write + pattern-vs-instance land in the new shape).

12. **Office-vs-department modularization design** (per ROADMAP
    commitment #12, session-7 late insight) — **POSITION 2**:
    - **The architectural insight**: PBS today conflates "office"
      with "single department" (planning-document-work). Real
      offices contain multiple departments (planning + PM +
      invoicing for a planning bureau). brand-voice (Anthropic's
      partner-built plugin) is a single-department plugin —
      that comparison surfaced the gap.
    - **Outputs** (1 session, primarily design):
      - `docs/decisions/office-vs-department.md` — architectural
        distinction + chosen implementation approach
      - Skill frontmatter convention: `department: <slug>` field
      - Office-config schema: `departments.<name>` sections
      - Memory taxonomy decision: department axis vs domain
        forking (open question)
      - Cross-department workflow patterns documented
      - Setup integration design (extends `setup-office` or
        adds `integrate-department` skill)
    - **Method**: examine current PBS skills; classify each as
      office-level scaffolding vs department-of-planning-work;
      design the explicit boundary; specify how PM + invoicing
      departments would slot in.
    - **Order**: schedule FIRST (before #11) because Cowork
      integration's slash command namespacing + skill frontmatter
      need department-aware shape. Doing #11 first means redo
      work.
    - **Scope**: design + decision record, not heavy
      implementation. PM + invoicing departments themselves are
      future work (post-RAG, when Schulz Planungsbüro actually
      needs them).

### Sparring-output integration (still per v1 plan, unchanged)

- `review-draft` declares `output_schema: ReviewOutput` in
  frontmatter; body adds Output Format section.
- `orchestrator` PROCEDURE.md Checkpoint 13: declare phase-
  specific `RecommendationOutput` schema; call
  `validate_skill_output` post-output; loop on missing-fields
  up to 3x.
- Heuristic markdown-field parser refinement after first
  real-use feedback.

### Plugin version bump

- `plugin.json` 0.3.0 → 0.5.0 (v1 commitments 4-9 are
  substantial — multiple new MCP tools, new entity sub-kind
  retired, new frontmatter conventions, fail-closed corollary,
  pattern-vs-instance refactor). Run `bash dev-link.sh` after.

### Then — Phase 0 items 4 + 5

After all v1 commitments land:
- **Phase 0 item 4 — Feature-survey skill**: greenfield-the-vision
  sibling to audit + design-review. Will likely benefit from
  pre-action framing skill being in place first.
- **Phase 0 item 5 — Testing methodology + harness**: discussion-
  first. `docs/rag-testing-strategy.md` output.

### Then — Phase 1 corpus download

The actual RAG ingest start. Fetch all 57 entries via
`research-references` full refresh. **No embeddings yet** — raw
fetch + checksum + manifest population only.

---

## Key paths reference

| Path | Purpose |
|---|---|
| `/home/g/dev/Gunther-Schulz/pbs-bureau/` | This repo |
| `VISION.md` | Three-axis thesis (canonical "why") |
| `ARCHITECTURE.md` | **v0.9** + fail-closed corollary + pattern-vs-instance discipline + office-vs-department open question |
| `ROADMAP.md` | 12 pre-RAG commitments at top; generalize-publish in v1.x (primary scope = audit + design-review); AI-office builder in v2 with market-context + 5 takeaways |
| `~/dev/reference/knowledge-work-plugins/` | Cloned Anthropic plugins repo for study (legal, enterprise-search, cowork-plugin-management, brand-voice) |
| `docs/decisions/mcp-fallback-policy.md` | Session-7 fail-closed corollary record |
| `docs/decisions/trigger-convention.md` | Session-7 concept-labels record |
| `docs/decisions/audit-trail-v2.md` | Session-7 reversal record |
| `docs/decisions/audit-trail-v1.md` | SUPERSEDED (header note added) |
| `docs/decisions/sparring-output-v1.md` | Session-6 v1 commitment |
| `docs/decisions/backend-{test-layout,logging,mcp-error-format}.md` | Session-5 backend records |
| `docs/audits/boundary-adherence-20260429.md` | Slice 14 first run (session 6) |
| `docs/audits/invalidation-contract-20260429.md` | Slice 15 first run (session 6) |
| `docs/audits/validation-gate-20260429.md` | Slice 16 first run (session 6) |
| `docs/design-reviews/vision-arch-coupling-20260429.md` | Target 8 first run (session 6) |
| `docs/design-reviews/foundations-20260429.md` | Session-5 design-review |
| `plugin/skills/audit/` | **0.8.0** — slices 1-16 + 18 + 19 |
| `plugin/skills/design-review/` | **0.7.0** — targets 1-10 |
| `plugin/skills/orchestrator/` | **0.10.0** |
| `plugin/CLAUDE.md` | Updated meta-rule 4 summary (fail-closed line) |
| `docs/plugin-conventions.md` | §11 (triggers) + §11b (fallback policy) |
| `~/.config/pbs-bureau/office.yaml` | v3 (session 6 migration) |

---

## Skill versions snapshot (post-session 7)

| Skill | Version | Change session 7 |
|---|---|---|
| audit | **0.8.0** | + slice 18 (legacy retirement) + slice 19 (pattern-vs-instance scan); slice 14 brief extended with violation pattern 5 |
| author-manifest | **0.4.0** | trigger collapse + fallback note about ROADMAP gap |
| design-review | **0.7.0** | + target 9 (Subsumption check) + target 10 (Pattern-vs-instance check) |
| draft-cover-mail | **0.6.0** | state.md gate + trigger collapse |
| draft-textteil-b | **0.5.0** | state.md gate + trigger collapse + fallback rewrite |
| draft-textteil-c | **0.5.0** | state.md gate + trigger collapse + fallback rewrite |
| orchestrator | **0.10.0** | state.md gate + meta trigger format |
| promote-to-skill | **0.5.0** | state.md gate + fallback rewrite + trigger collapse |
| record-feedback | **0.4.0** | fallback rewrite (fail-closed for bausteine) + trigger collapse |
| research-references | **0.5.0** | fallback tightened + trigger collapse |
| review-draft | **0.5.0** | state.md gate + fallback rewrite + trigger collapse |
| save-baustein | **0.4.0** | fallback rewrite (fail-closed for bausteine) + trigger collapse |
| setup-office | **0.6.0** | fallback notes ROADMAP gap + trigger collapse |
| survey-project | **0.5.0** | bind_project + update_project_state in tools_required + trigger collapse |
| validate-bausteine | **0.4.0** | fallback rewrite (fail-closed for bausteine) + trigger collapse |
| validate-checklist | **0.6.0** | state.md gate + manifest fail-closed + trigger collapse |
| validate-latex-style | **0.5.0** | trigger collapse + fallback tightened |
| verify-citations | **0.5.0** | manifest fail-closed + trigger collapse |
| watch-list | **0.2.0** | bauseine fail-closed + trigger collapse |
| plugin.json | 0.3.0 | unchanged this session; will bump 0.5.0 after session 8 retrofits |

---

## MCP tools shipped session 7

None this session — all session-7 work was at the markdown / skill
/ documentation layer. The session-6 tools (5 new) remain the
current backend surface. New backend tools planned for session 8:
- `record_decision` (audit-trail v2)
- `render_audit_trail` (audit-trail v2)
- `create_manifest` (bootstrap-write)
- `create_office_config` (bootstrap-write)
- (plus AuditEvent schema additions: `user_confirmation` event,
  `reasoning_full_text` in details)

---

## Working-style notes (carried + new)

1. **Pre-action framing matters more than post-action review** for
   architectural correctness. The audit-trail v1 → v2 reversal
   exposed the gap: review skills caught the redundancy
   *retrospectively*. Target 9 + slice 18 + the future framing
   skill aim to catch this *prospectively*. The user's framing:
   "preparation → implementation → review" — the prep layer was
   missing.

2. **Legacy retirement is the default, not the exception.** When
   adding a new mechanism, asking "what does this subsume?" is
   mandatory. Inertia ("we're used to it," "it's established")
   isn't a load-bearing reason. Names the specific role the
   legacy plays that the new doesn't fill, or retire.

3. **Decision-record reversals are normal and tracked.** The
   `Supersedes` / `superseded by` chain in decision records IS
   the architecture's evolution log. Each reversal teaches
   something — v1→v2 audit-trail teaches "always ask
   subsumption before adding alongside."

4. **Plugin-wide sweeps after policy changes are forced moves.**
   The fail-closed corollary touched 19 skills' fallback strings;
   the trigger convention touched 19 skills' triggers. Both
   sweeps were tedious but unavoidable — a policy that doesn't
   apply uniformly is worse than no policy. Future policy
   changes will follow the same pattern.

5. **Fail-closed for contract-bearing reads is symmetric with
   the write-side rule.** Pre-session-7 the persistence boundary
   was write-asymmetric (skills couldn't write contract-bearing
   files but could read them via fallback). v0.7 closes this
   asymmetry. Audit slice 14's violation-pattern 5 catches
   regression.

6. **Memory captures**: existing 6 feedback memories carry forward.
   The "leave legacy behind" principle is now in
   ARCHITECTURE.md (target 9 + slice 18) — more durable than
   memory.

7. **PBS as pioneer instance is now architectural discipline,
   not framing.** Pre-session-7, "pioneer instance" lived in
   VISION.md as commitment language. v0.8 elevates it to working
   discipline (`ARCHITECTURE.md` "Pattern-vs-instance discipline"):
   every commitment must be checked against pattern-level
   generalization. The single-domain-pioneer constraint is named
   explicitly — empirical 2-3-domains validation is wrong for
   this constraint, best-effort split is the working method.

8. **Two-signal validation framing** (session 7 late insight):
   when validation evidence is partial, name what each available
   signal tells you and what it doesn't. Signal #1 (split
   doesn't break PBS) is checkable now; signal #2 (right
   boundary across domains) waits for second-domain
   implementation. Doing the split now extracts maximum
   immediate validation; deferring extracts none and pays
   migration cost later.

---

## Session 7 commits (chronological)

| # | Commit | Theme |
|---|---|---|
| 1 | `66e25b9` | session 7 main batch: state.md retrofit + fail-closed corollary + trigger convention + audit-trail v2 + target 9 + slice 18 + bootstrap-write promote + framing skill ROADMAP |
| 2 | `cdc92d5` | ROADMAP: clarify generalize-skills priority (audit + design-review primary; secondary candidates uncommitted) |
| 3 | `24ac10c` | ROADMAP: add v2 long-horizon vision — AI-office builder |
| 4 | `ecc1b8c` | session 7 final: pattern-vs-instance discipline (v0.7→v0.8) + commitment #9 + design-review target 10 + audit slice 19 + VISION pioneer-instance extension + plugin/CLAUDE.md discipline summary + HANDOFF refresh |
| 5 | `bfd0313` | session 7 epilogue: market context + commitments #10 (A2A) and #11 (Cowork runtime) |
| 6 | `0bb0253` | session 7 closing: deep-Cowork-integration directive (no sunk costs) + commitment #12 (office-vs-department modularization) + ARCHITECTURE v0.8→v0.9 + revised execution order (#12 → #11 → rest) |
| 7 | (this commit) | session 7 final-final: A2A pulled to position 1; revised execution order #10 → #12 → #11 → rest. ROADMAP + HANDOFF order notes updated. |

All pushed to origin/main.

---

## Misc context for next session

- **User's machine**: Linux, RTX 5090 (32GB VRAM). Python 3.13.
- **Plugin cache symlink**: bump `plugin.json` AND re-run
  `bash dev-link.sh` after session-8 retrofits.
- **Hooks active**: `restrict-bash-paths.py`,
  `restrict-file-paths.py` in dotfiles. Hidrive path whitelisted.
- **Settings symlink**: verify
  `~/.claude/settings.json -> dotfiles/claude/settings.json`
  before any operation that might write settings.
- **Office-config**: v3 on disk; no `path_classification` block.
- **No projects bound yet**: the session-7 retrofits are
  design-time-pending until first project bind. Backfill is
  academic until first-bind.
- **Auto-memory** at `~/.claude/projects/.../memory/`:
  - `feedback_blocked_actions.md`
  - `feedback_judgment_and_automate.md`
  - `feedback_push_after_commit.md`
  - `feedback_refine_pareto.md`
  - `feedback_defer_instinct.md`
  - `feedback_llm_instruction_tightness.md`
