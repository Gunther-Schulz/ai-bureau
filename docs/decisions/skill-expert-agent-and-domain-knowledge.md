# Decision record: Skill / expert / agent + where domain knowledge lives

**Status**: ACCEPTED (session 11, 2026-04-30)
**Owner**: ARCHITECTURE.md "AI-as-runtime hybrid-shape principle" + plugin-conventions §<TBD> + ROADMAP commitment #11 (slash command UX + skill-vs-agent formalization)
**Related**: `docs/decisions/ai-as-runtime-hybrid-shape.md` (#16 — distributed expertise as concrete application of the principle), `docs/decisions/office-vs-department.md` (#12 — singleton-department skill rule), `docs/decisions/governance-and-identity-sourcing.md` (decision 4 — prose conventions as deployment-instance content)

## Context

Topic 1 of session 11 surfaced four interconnected questions about the conceptual model of skills, experts, agents, and where domain knowledge lives:

1. **"Expert" as user-facing vocabulary** — should "expert" appear in slash commands / Cowork UX, or stay as "skill"?
2. **PM department default** — when scaffolding a new office that includes PM, does the default lean native-mode managed entities or adapter-mode?
3. **Skill vs plugin agent distinction** — when does a "Begründungs-writer expert" become an agent vs stay a skill?
4. **Fine-grained expertise** (e.g., "§13a-Verfahren expert") — separate skill or section-specific content within an existing skill?

The resolutions compose because they're all aspects of the same architectural concern: how the office abstraction expresses domain expertise to the practitioner and where that expertise actually lives.

## Decisions

### 1. "Expert" is per-deployment UX vocabulary; "skill" is the architectural entity

**The architectural entity stays `skill`** (no rename). The user-facing label is **per-deployment customizable** via an optional skill frontmatter field.

**Mechanism**: optional `display_label:` field in skill frontmatter:

```yaml
# draft-textteil-b/SKILL.md frontmatter
display_label: "Begründungs-Schreiber"   # PBS-Schulz UX label
```

When absent, falls back to skill `name` (current behavior). Slash commands surface the label in Cowork UI.

**Why not rename "skill" → "expert" globally**:
- Per pattern-vs-instance discipline: "expert" is one deployment's UX framing. Other deployments might use "specialist" / "co-author" / "Spezialist" / domain-specific names. Forcing one violates pattern level.
- Anthropic's plugin conventions use "skill" — alignment with ecosystem matters per glue-not-replacement.

**Why not pure prose convention** (per "Make wrong shapes impossible" discriminator):
- The slash command UI dispatches on display_label every render. That's not "every read/write" but it's a common dispatch path.
- Optional structured field is fine because it's a string with no semantic load (no failure mode to prevent). Either prose-convention OR optional structured field works architecturally; structured wins on ergonomics.

**Lands in**: `plugin-conventions.md` (new optional field documented) + `#11 Cowork integration` (slash command UX uses the label).

### 2. PM department default — builder prompts; no pre-chosen default

**No pre-chosen default for native vs adapter mode.** Setup-office (and v2 builder) prompts at scaffold time.

**Why**: per "Informed defaults: ship best-shape, not empty" — best-shape default for a high-variance choice is **a question with concrete options**, not a pre-pick.

Concrete flow: when scaffolding a department with adapter-eligible managed entities, setup-office asks:

```
Does this office use an external [PM tool / invoicing tool / HR system]?
  - Yes — pick from supported adapters: Asana / Jira / Linear / Trello / Lexware / Personio / ... / declare custom adapter to write later
  - No — generate native scaffold (PBS owns the entities)
```

PBS-Schulz answers "no PM tool" → native PM scaffold (or no PM department at all initially). Consulting client with existing Asana → adapter scaffold.

**Generalizes**: the same prompt pattern applies to any department with potential external-system overlap (PM, invoicing, HR, document-management, time-tracking). Per glue-not-replacement: when external system exists, adapt; when not, native.

**Lands in**: `setup-office` skill retrofit (#11 scope) + v2 builder scaffolding (constraint).

### 3. Skill vs plugin agent — invocation pattern wraps body; some bodies fit only one wrapper

**Skills and agents are NOT a hierarchy or strict orthogonal axes.** The accurate model:

- **Bodies** (the actual work logic) have inherent shape
- **Invocation patterns** wrap bodies — "skill" (user-driven) or "agent" (autonomous) or "both"
- Some bodies fit only ONE wrapper; some fit BOTH

**Skill invocation pattern** = user-driven, conversational, per-turn. State in MCP-gated entities. AI orchestrates per user input.

**Plugin agent invocation pattern** (per #11) = autonomous loops. Run between user turns. Watch for triggers, batch-process, react to external events.

**Examples**:

| Work body | Skill mode? | Agent mode? | Notes |
|---|---|---|---|
| Begründungs drafting (interactive sparring) | ✅ yes | ❌ no | Drafting requires axis-2 sparring (counter-argument, asymmetric knowledge respect, anti-sycophancy). Autonomous drafting breaks the sparring requirement. Skill-only. |
| Layered review of draft (interactive critique) | ✅ yes | ❌ no | Same — review is sparring-shaped. |
| Reference fetcher (corpus refresh) | ✅ yes (manual trigger) | ✅ yes (scheduled) | Both useful — skill for ad-hoc fetch; agent for scheduled refresh per #13 time-driven triggers. |
| Audit slice runner (batch over files) | ✅ yes (manual) | ✅ yes (scheduled / on-event) | Same. |
| Design-review target runner | ✅ yes (manual) | ✅ yes (per-pre-launch sweep) | Same. |
| Notification dispatcher | ❌ no (no human-meaningful invocation) | ✅ yes | Pure agent — runs continuously, dispatches per AuditEvent matches. |

**Generalization**:
- **Domain expertise** = skills. Drafting / reviewing / sparring are sparring-shaped → skill-only.
- **Coordination / monitoring / batch / external-event-reactive** = agent (often + skill mode for manual override).
- Some bodies (notification, scheduled fetch) are agent-only — no human-meaningful per-turn invocation.

**Lands in**: `plugin-conventions.md` (skill-vs-agent distinction documented) + `#11 plugin agent formalization` (concrete agent list per ROADMAP #11 — research-references-fetcher, audit-slice-runner, design-review-target-runner — annotated with their dual-mode capability).

### 4. Fine-grained expertise — content distributed across sources, NOT separate skills

**Fine-grained expertise (§13a-Verfahren, specific section, niche edge case) is CONTENT distributed across the existing architecture's sources. AI as runtime composes the expertise per use.**

**§13a-Verfahren expertise lives in**:

| Source | What it provides |
|---|---|
| **Process entity** `extensions/department/planning/processes/beschleumigtes.md` | The regulatory process flow — when §13a applies, what doctypes it produces, mandatory triggers, exceptions |
| **References** `BauGB.md` body (`## Key sections for our work`, `## Recent amendments to watch`) | §13a key sections, recent amendments, key citations |
| **Skill body** `draft-textteil-b/SKILL.md` | Knows to read process entity for verfahren-specific behavior |
| **Skill references** `draft-textteil-b/references/begruendungs-modules.md` | Section content per Verfahren type (incl. §13a-specific deviations) |
| **Memory bausteine** | Accumulated §13a-specific phrasings across past projects |

The Begründungs-writer expert (= `draft-textteil-b` skill), when handling a §13a project, reads the §13a process entity + corresponding references + applies §13a-specific patterns from memory. AI composes at runtime.

**Why NOT separate skills for fine-grained topics**:

Per entity-elevation 3-test (analogous for skills):
- §13a-Verfahren passes **stable identity** (it's a stable concept).
- §13a-Verfahren fails **state-of-record** (the Verfahren TYPE is a concept, not a stateful entity; state lives on the project that USES §13a).
- §13a-Verfahren fails **lifecycle** (the concept itself doesn't have a lifecycle; the project does).

Fails 3-test → does NOT elevate to separate skill.

**Generalization**: **expert ≠ topic.** Experts are SKILLS (broad workflow specialists with pattern-level scope). Narrow expertise is CONTENT (process entities + references + skill references + memory bausteine + corpus) the skill reads at runtime. AI-as-runtime hybrid-shape principle in action — markdown bodies as runtime fuel for the skill's workflow.

**Lands in**: AI-as-runtime hybrid-shape decision record (cross-reference) + plugin-conventions.md (skill granularity guidance — when to elevate vs when to keep as content).

## Composition with existing disciplines

| Discipline | Connection |
|---|---|
| **AI-as-runtime hybrid-shape** | Decision 4 is the canonical application — fine-grained expertise distributed as prose; AI fuses at runtime. Same shape as memories applying conventions at mint-time. |
| **Pattern-vs-instance** | Decision 1 (display_label per deployment) + decision 2 (no native/adapter default) both honor pattern-vs-instance — UX vocabulary + setup choice are deployment-instance, not pattern-level. |
| **Make wrong shapes impossible** | Decision 1 evaluated via discriminator — display_label is a stretchy choice (could be prose convention OR optional structured field); structured wins on ergonomics, no failure mode either way. |
| **Entity-elevation 3-test** | Decision 4 explicitly applies the 3-test (analogous for skills) — §13a-Verfahren fails the test for skill elevation; stays as distributed content. |
| **Glue-not-replacement** | Decision 2 — prefer adapter mode when external system exists; native when not. Per meta-rule 1 + glue-not-replacement principle. |
| **Sharp defer rule (v0.20)** | None deferred under instance-anchored rationale. All four decisions land at architectural level now (display_label field, setup prompt mechanism, skill-vs-agent distinction, fine-grained-expertise placement) — framework infrastructure. |

## Defers (per defer-instinct discipline)

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Concrete `display_label` rendering implementation in Cowork slash commands | #11 (Cowork integration) — slash command UX surface lives here | Pre-empting #11 design without concrete Cowork plugin shape; this DR specifies the field convention |
| **D2**: setup-office prompt UX (exact phrasing, adapter list curation, "declare custom adapter later" workflow) | #11 setup-office retrofit | Implementation detail; this DR specifies the principle (prompt at setup, no pre-chosen default) |
| **D3**: Skill-granularity discipline check (audit slice OR design-review target that flags over-elevated skills, parallel to entity-elevation slice 20 + target 11) | Future audit/design-review work; bundled with #9-followup or #11 | No clear case of over-elevation today; defer until pattern emerges |

## Constraints flowing to downstream commitments

### → #11 (Cowork integration)

- **Slash command UX uses `display_label`** when set in skill frontmatter; falls back to skill `name` when absent.
- **setup-office retrofit** prompts at scaffold time for native-vs-adapter per managed-entity-eligible department; does NOT pre-choose default.
- **Plugin agent formalization** annotates each concrete agent (research-references-fetcher, audit-slice-runner, design-review-target-runner) with its dual-mode capability (skill mode for manual / agent mode for autonomous).
- **Per session-11 governance-and-identity-sourcing decision 1**: skill bodies surface UX of approval workflow but DON'T enforce roles — the gate enforces. Same defense-in-depth applies to display_label rendering (UX convenience, not authorization signal).

### → plugin-conventions.md updates

- **New optional field**: `display_label: str` in skill frontmatter spec.
- **Skill-vs-agent distinction** documented as separate section.
- **Skill granularity guidance** documented — apply 3-test analogue before elevating fine-grained topics to separate skills.

### → AI-as-runtime hybrid-shape decision record (cross-ref)

- Decision 4 is a concrete application of the principle — distributed expertise across structured + prose layers, fused at runtime. Could add as a worked example in the hybrid-shape DR or rely on this DR's cross-ref.

### → setup-office skill retrofit (when #11 fires)

- Adds prompts for adapter-mode-eligible departments per decision 2.
- Records user's choice in office-config + audit event with `convention_applied` reference (per governance-and-identity-sourcing decision 4).

## Pattern-vs-instance check

| Domain | Decisions hold? |
|---|---|
| **Legal practice** | Yes — display_label "Brief-Schreiber" / "Counselor" / etc.; PM via legal practice management tool (Clio, Casemine) → adapter-mode default question; skill-vs-agent same axes (matter-coordinator agent watches for filing deadlines while drafting skills handle interactive work); precedent-specific expertise distributed across precedent.md entities + skill body + memory. |
| **Research lab** | Yes — display_label "Co-author" / "Manuscript-helper"; PM via institutional system → adapter; agent-mode submission-watcher; method-specific expertise distributed across method.md entities + skill body. |
| **Brand voice** | Yes — display_label "Brand-strategist" / "Voice-coach"; no PM department needed (single-skill-utility shape); skill-mode brand-asset-creator; tone-specific expertise distributed across tone.md guideline entities. |

All four decisions hold cross-domain. Pattern-level. ✓

## Revisit triggers

- A real second deployment chooses different vocabulary than "expert" (signal for display_label adoption rate).
- A skill-granularity case surfaces (someone wants to elevate `§13a-expert` as separate skill) → re-evaluate D3 (skill-granularity discipline check).
- Plugin agent formalization in #11 surfaces a body that doesn't fit either skill or agent wrappers → re-evaluate model.

None expected pre-RAG.

## Files touched by this commitment

- `docs/decisions/skill-expert-agent-and-domain-knowledge.md` — this file (NEW)
- `docs/plugin-conventions.md` — display_label field + skill-vs-agent distinction + skill granularity guidance (pending update)
- `HANDOFF.md` — brief reference to this DR (pending update)
- `ROADMAP.md` #11 — constraints recorded (display_label rendering + setup-office prompts + plugin agent dual-mode annotation)

No code changes this commitment. Implementation lives across #11 (Cowork integration + setup-office retrofit) + per-skill display_label adoption (per-deployment).
