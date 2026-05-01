# Doc system maintenance

This is the meta-doc that defines how the pbs-bureau corpus is organized and how it stays consistent. **Read at session start alongside `VISION.md` and `HANDOFF.md`.**

The doc system was designed in session 16 (2026-05-01) at start of the foundational rebuild. Two motivating concerns:

1. **Cognitive-load reduction** — the prior v0.35 corpus grew beyond easy handling (~10k+ lines of architectural docs); cursory reads produced pattern-matching failures in AI-assisted work. The layered structure makes the right depth for any question obvious; reading scope is bounded per question.
2. **Consistency across docs** — v0.35 contained internal contradictions (e.g., shape-neutrality + Option B floor; v0.34 location restructure not cascaded to shape-extension DR). These arose because cascade discipline was implicit. Making it explicit prevents recurrence.

---

## TOP-LEVEL RULE — Cascade discipline

**The doc system must stay in a consistent state. When you change any concept, decision, primitive, or term in any doc, identify every other place it appears and update each in the same commit (or a tightly-coupled sequence of commits explicitly marked as completing the cascade).**

### Direction of cascade

Changes propagate **down, up, and sideways** as needed:

- **DOWN** — changing a foundation propagates to dependent layers. Examples:
  - Glossary term redefined → every Layer 3 topic + Layer 4 DR + Layer 5 spec mentioning it must update
  - VISION axis refined → ARCH must update + Layer 3 topics referencing the axis must update
  - ARCH adds new primitive → Layer 3 topic file is created + Layer 5 spec defines schema + Layer 4 DR captures the decision

- **UP** — adding detail at a deeper layer can require overview update. Examples:
  - Layer 4 DR makes new decision touching architectural placement → Layer 3 topic updates + ARCH reference card updates if the decision shifts a placement rule
  - Layer 5 spec adds new schema field that's load-bearing → Layer 3 topic updates if the field affects the primitive's structural shape

- **SIDEWAYS** — peer docs at the same layer that share a concept boundary co-update. Examples:
  - Layer 3 `framework.md` and Layer 3 `shape.md` both describe the framework-vs-shape boundary; moving the boundary in one requires updating the other
  - Two DRs that compose architecturally (e.g., one adopts a Protocol pattern, another defines a specific Protocol implementation) update together when the pattern shifts

### How to find cascades

Before committing any non-trivial doc change:

1. **Grep the affected concept name** across all docs (`git grep <term>`). Every hit is a candidate cascade target.
2. **Review each hit** — does the change shift this hit's meaning? If yes, update. If no, explicitly verify in commit message ("verified consistent: <hit>")
3. **Cross-check the layer above and below** — does the change require ARCH overview update (up) or Layer 3 topic update (down)?
4. **When uncertain**, surface the cascade question explicitly to the user during the change rather than committing partial cascade

### Anti-patterns (what cascade prevents)

- **Contradictory claims across docs** — e.g., DR-A says "framework is shape-neutral"; DR-B (added later, same author) says "framework enforces practitioner-shape axis 3 on all shapes." Cascade would have caught the contradiction at write-time.
- **Stale references** — e.g., a DR references `extensions/shapes/<id>/` (its original framing); a later restructure moves to `extensions/framework/shapes/<id>/`; the original DR is not updated. Cascade catches this.
- **Vocabulary drift** — e.g., one doc uses "office" while another uses "workspace"; sessions pass before the drift is noticed. Cascade catches at term-rename time.
- **Decisions without overview reflection** — Layer 4 DR captures decision, but Layer 2 ARCH overview's reference card or primitive list isn't updated. Reader of ARCH doesn't see the decision exists.

---

## TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies

The framework provides **MECHANISMS** — universal interface contracts that any workspace shape can use; no shape-specific values. Shapes provide **POLICIES** over mechanisms — each shape configures which mechanisms are active, which are mandatory, which defaults apply.

This means:

- **Framework-level**: what's POSSIBLE (interface contracts; capabilities; primitives)
- **Shape-level**: what's MANDATED for a workspace archetype (policies; defaults; required-vs-optional)
- **Cross-cutting**: workspace, practitioner, session, workflow (orthogonal to mechanism/policy split)

### Atoms vs containers

- **mechanism** is the atom — a single interface contract; capability with defined input/output surface
- **policy** is the atom — a single configured value; requirement/default/constraint
- **framework** is the container — the shape-neutral universal layer; collection of mechanisms + protocols + architectural disciplines
- **shape** is the container — the policy-bundle archetype for a workspace archetype

### A-B-C scope model

Three placement categories. Framework C + Owner B are **derived** from framework/shape; Layer A is **orthogonal** (an independent axis for content layering by deployment context, not derived from the mechanism/policy split).

- **Framework C scope** (derived from `framework = mechanisms`) — home for DEFINITIONS (mechanism / shape / substrate / protocol-implementation / specialist DEFINITIONS); universal, immutable, distributable
- **Owner B scope** (derived from `framework + shape → workspace deployment`) — home for INSTANCES (workspace, workspace-scope managed entities including practitioner-record + Actor + Client, specialist instance content, work-unit-kind instances); deployment-specific
- **Layer A scope** (orthogonal — independent classification by content scoping) — home for LAYERED CONTENT (universal / domain-keyed / state-keyed content: references, doctypes, bausteine, prose conventions); varies by deployment context

A-B-C is **preliminary-locked** — revisable when concrete entity-md authoring exercises (Phase 3+) reveal mismatches.

Reading any entity-md instance, two questions are answerable independently:
1. Is this a DEFINITION (Framework C) / INSTANCE (Owner B) / LAYERED CONTENT (Layer A)?
2. What scope-key applies (universal / domain / state / specialist-id / workspace / etc.)?

The two questions are orthogonal: a reference can be universal-Layer-A; an entity-instance can be workspace-scope-Owner-B; a definition can be Framework C regardless of layer.

### Concept-by-concept (worked examples)

| Concept | Framework-level (mechanism) | Practitioner-shape (policy) |
|---|---|---|
| Audit emission | AuditEvent schema; `actor_kind` declared on every event; Pydantic gate dispatches every write | Audit granularity = claim-level; emission required for every output |
| Specialist modification | Specialist definition loaded; Pydantic schema declares conformity surface; modifications re-validate | Modifications require explicit re-conformance event |
| Authority binding | `actor_kind` enum includes `human`; AuditEvent records emitting actor | Human authority required in accountability-bearing output chain |
| Sparring | Sparring Protocol exists as runtime mechanism | Always-on; runtime pillar; output blocked until sparring fires |
| EU AI Act | (nothing) | (nothing — lives in eu-ai-compliance specialist) |
| Long-running work-units | (nothing — workspace + specialist suffice) | Practitioner-shape may activate a "project" specialist; legal-practice may activate "matter"; work-unit kind is specialist-defined |

### Recurring patterns: Protocol pluggability (the Protocol pattern)

Some framework primitives recur with a structural shape: **Surface + Implementations + Instance/binding** — the **Protocol pattern**. When this pattern manifests, the primitive has three aspects:

1. **Surface** (mechanism; framework-level): an abstract Protocol contract defining the interface
2. **Implementations** (Framework C definitions; distributable): concrete realizations of the surface
3. **Instance/binding** (Owner B; workspace-level): the running implementation a workspace selected/bound

Known instances (preliminary-locked; more may surface):

- **substrate** (locked) — Substrate Protocol surface + concrete substrates (Claude Agent SDK, MS Agent Framework) + workspace's running substrate per `workspace.md`
- **adapter** (canonical entry forthcoming) — Adapter Protocol surfaces per integration class + concrete adapters (e.g., gmail-adapter, lexware-adapter, MCP-protocol-based adapters) + workspace's active adapters
- **protocol** (architectural; canonical entry forthcoming) — the meta-concept: Coordination/Audit/Sparring/Trust/Time Protocol surfaces + their concrete implementations + per-shape-policy or per-workspace selection

**Naming**: "Protocol pattern" with explicit disambiguation from **Pydantic Protocol** (the Python typing concept; `typing.Protocol`). The architectural Protocol pattern is broader — it describes pluggable-subsystem structure regardless of implementation technique.

### Other multi-aspect primitives (NOT Protocol pattern)

Some primitives have multi-aspect / dual-nature structure but do NOT follow the Protocol pattern:

- **specialist** — bipartite: DEFINITION (Framework C; distributable bundle) + INSTANCE-CONTENT (Owner B; entities owned within the deployed specialist). NO multiple implementations: a specialist IS its definition.
- **practitioner** — bipartite of different shape: HUMAN (cross-cutting; the actual person; not "placed") + RECORD (Owner B; system representation).

Each has its own dual-nature description in its GLOSSARY entry; not generalized as Protocol pattern. Don't conflate.

### Glossary entry classification

Each GLOSSARY entry tags itself with:

- **Class**: PRIMITIVE (atomic) / META-PRIMITIVE (container) / DERIVED (composition) / SCOPE-CLASSIFICATION
- **Layer**: framework-mechanism / shape-policy / cross-cutting / dual-nature
- **Axis**: axis-1 / axis-2 / axis-3 / cross-axis (where applicable)
- **VISION usage**: directly used in VISION / implicit / derived-from-VISION-terms / framework-meta

Reading any GLOSSARY entry, the layered approach is structurally visible: foundational atom or derived? framework-territory or shape-territory? which axis does it serve? does VISION use the term?

(Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.)

---

## The 5-layer model

| Layer | What lives there | Where | Reading scope at session start | Line budget per doc |
|---|---|---|---|---|
| **0 — Entry** | README + HANDOFF + MAINTENANCE (this file) | Top-level | **Always read** | ~100 / lean log / ~150 |
| **1 — Foundations** | VISION + GLOSSARY | Top-level | **Always read** | ~1000 / ~500 |
| **2 — Overview** | ARCHITECTURE + ROADMAP + STRATEGY | Top-level | Read on substantive sessions | ~500 each |
| **3 — Architecture detail** (topical) | `docs/architecture/<topic>.md` | per primitive / discipline / cross-cutting concern | Read when working in that area | ~500 each, 15-20 topics total |
| **4 — Decision records** | `docs/decisions/<decision>.md` | narrow single-decision capture | Read when re-examining specific decision | ~150-300 each, ≤15-25 total |
| **5 — Specs** | `docs/specs/<spec>.md` | schemas, file formats, code conventions | Read when implementing against contract | ~500 each, ~5-8 specs |

**Memory** (orthogonal, not layered): `memory/` — feedback files + bausteine + universal prose. Persistent state, not architecture.

**Active reading at session start**: Layer 0 + Layer 1 ≈ ~1.7k lines. Constant per session, not proportional to corpus size.

### Layer 0 — Entry

- **README.md** — one-screen project description; what PBS is; how to enter; pointers to Layer 1
- **HANDOFF.md** — lean session log; ~30-100 lines per session; rotate older sessions to `archive/handoffs/HANDOFF-sessions-N-M.md` when active HANDOFF crosses ~500 lines (keep current session + last 2 entries active)
- **MAINTENANCE.md** — this file; doc system rules

### Layer 1 — Foundations (anchored; rarely change)

- **VISION.md** — three-axis thesis + foundations + pioneer-instance commitment + falsification criteria. **Anchored** per preliminary-lock principle (`memory/feedback_preliminary_lock.md`); revise only on real-world falsification per VISION's own criteria.
- **GLOSSARY.md** — canonical vocabulary. **ONE home for every term definition.** Each entry: one-sentence canonical definition + non-examples + cross-archetype examples + boundary tests + cross-references to Layer 3 topic where the term has structural detail. Layer 3+ docs cite GLOSSARY rather than redefining terms.

### Layer 2 — Overview

- **ARCHITECTURE.md** — structural primitives (1-line each) + design disciplines (1-line each) + reference card (where things go) + pointers to Layer 3 topics. **Cannot describe mechanisms in detail**; that's Layer 3 territory.
- **ROADMAP.md** — commitments + horizons; lean
- **STRATEGY.md** — market positioning + competitive landscape + funding + ICP. Architectural-adjacent, not architecture itself

### Layer 3 — Architecture detail (topical)

`docs/architecture/<topic>.md` — one file per major architectural concern.

Each file: motivation + structural shape + how it composes with other primitives/disciplines + decisions made (linking to Layer 4 DRs) + specs needed (linking to Layer 5).

**Single abstraction level per file**: structural mechanisms for primitives; decisional reasoning for disciplines.

### Layer 4 — Decision records

`docs/decisions/<decision>.md` — ONE narrow decision per DR.

Format: context + decision + rationale + alternatives considered + composition with disciplines + revisit triggers.

If work decomposes into multiple decisions, write multiple DRs — never Sub-DR A + Sub-DR B in same file.

Referenced FROM Layer 3 topics; not standalone reading.

Supersession via header notes when a DR is superseded by a later one (existing pattern).

### Layer 5 — Specs

`docs/specs/<spec>.md` — implementation contracts.

Schema definitions, file format specs, code conventions, plugin authoring conventions, MCP tool conventions.

Versioned: semver if breaking; date if non-breaking.

---

## Cross-reference discipline (the navigability rule)

**Read references go DOWN the layers, not laterally:**

- Layer 0 → Layer 1 + 2 (entry pointers)
- Layer 2 → Layer 3 (overview points at topic detail)
- Layer 3 → Layer 4 + 5 (topic points at decisions + specs)
- Layer 4 → Layer 5 (decisions reference specs they implement)

**No lateral peer-references except within the same layer.** If two Layer 3 topics share a concept, that concept either:
- Belongs in GLOSSARY (Layer 1 — vocabulary)
- Belongs in ARCHITECTURE (Layer 2 — overview/reference card)
- Belongs in a third Layer 3 topic that both reference

**No upward read-references.** Layer 4 doesn't reference Layer 3 (Layer 3 references Layer 4). Forces hierarchy clarity.

**Note distinction**: cross-references are about READ direction (navigability). Cascade discipline is about WRITE direction (consistency when changing). When you change Layer 1 GLOSSARY, the change cascades DOWN to Layers 2-5 even though no Layer 1 doc references downward.

---

## Other maintenance disciplines

1. **Single abstraction level per doc.** If a Layer 2 doc starts describing mechanism details, split the detail to Layer 3. If a Layer 3 doc starts describing schemas, split the schema to Layer 5.
2. **Line budget as forcing function.** When a doc exceeds budget, decompose to next layer.
3. **One decision per DR** (Layer 4). If a decision splits, write multiple DRs.
4. **GLOSSARY is the single source for term definitions.** Layer 3+ docs may discuss structural detail about a primitive but cite GLOSSARY for canonical definition. If two docs define the same term, that's a cascade violation.
5. **Versioning per layer**:
   - VISION + ARCHITECTURE versioned (semver-ish on architectural significance)
   - DRs dated (no version; supersession via header note)
   - Specs semver
   - Topics + GLOSSARY versioned only on breaking changes (date for non-breaking)
6. **Periodic prune.** At major version boundaries: which docs no longer earn their keep? Collapse to broader topic / archive. Don't let dead docs accumulate.

---

## When this doc itself changes

This doc is Layer 0 — it governs the doc system itself. Changes to MAINTENANCE.md require especially careful cascade because they affect everything. When changing MAINTENANCE.md:

1. Identify what existing structure or discipline is being changed
2. Verify all docs currently following the prior rule still hold OR list which docs need updating to follow the new rule
3. Update HANDOFF.md to flag the rule change for future-session readers

---

## Memory composition

This doc composes with memory feedback files in `memory/`:
- `feedback_apply_principle_uniformly.md` — when applying any principle (including cascade), test all categories independently rather than letting inherited framings narrow the scope
- `feedback_vision_arch_grounding.md` — when assertions about doc content are needed, re-ground in source rather than pattern-matching from summaries
- `feedback_pattern_not_instance_defers.md` — never defer; if a cascade is uncertain because external info is missing, surface as watch-list entry naming the specific external signal
- `feedback_preliminary_lock.md` — every architectural decision is preliminary-locked; cascade applies even when revisiting "locked" prior decisions
- `feedback_propose_before_commit.md` — at decision phases (changing structure, primitives, disciplines), propose first; at content phases (filling in topic detail), persist directly
