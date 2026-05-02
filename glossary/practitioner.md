---
entry: practitioner
class: PRIMITIVE
layer: multi-aspect
axis: axis-3
vision_usage: directly-used
---

# practitioner

- **Class**: PRIMITIVE (atomic; the human-expert-author unit) — **bipartite** multi-aspect (Pattern C)
- **Layer**: multi-aspect (HUMAN aspect is cross-cutting; RECORD aspect is at Owner B as workspace-scope managed entity)
- **Axis**: axis-3 (primary anchor — practitioner is the axis-3 archetype, the role authorship preservation protects); cross-axis
- **VISION usage**: directly used (`VISION.md` lines 11, 15, 19 + axis 3 framing throughout)

**Canonical**: The human expert author who bears accountability for produced work — the natural person under whose name accountability-bearing output is signed and defended. Bipartite multi-aspect primitive (Pattern C; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Other multi-aspect primitives"): HUMAN (cross-cutting; the actual person, not "placed") + RECORD (Owner B; system representation including identity, credentials, signing authority, role bindings). Legal-entity context (firm-level contracting party) lives at WORKSPACE level (legal-entity workspace context), not at practitioner level — practitioner is always a natural person.

**What it is**: The role around which axis 3 (authorship preservation) is built. The practitioner is the human who signs the Begründung, the brief, the manuscript, the audit report — and who must be able to defend it later (the defensibility test). Architecturally this manifests in two aspects: the HUMAN itself (a person in the world; not a system entity; cross-cutting) AND a system RECORD (a managed entity at Owner B representing the practitioner — name, credentials, signing authority, role bindings). The HUMAN bears accountability legally + professionally; the RECORD is the system's stand-in that makes events traceable to a named person.

**Cardinality + lifecycle**: Practitioner-record cardinality per workspace = 1+ depending on shape (practitioner-shape solo workspace = 1; multi-practitioner-shape partnership workspace = N; legal-entity-shape workspace = N named practitioners under firm context). Lifecycle: practitioner-record created at workspace setup (initial practitioner) OR per-practitioner-addition (subsequent practitioners joining a multi-practitioner workspace). Mutability = mutable-with-audit (changes to credentials, signing authority, role bindings emit audit events; never silently rewritten). Records persist through workspace lifetime; deactivation semantics (practitioner leaving the firm) settled at ARCH Layer 3 — preliminary lock: deactivation marks record dormant, not deleted (preserves audit-trail attribution to historic outputs).

**What it is NOT**:
- Not an `actor` — actor is the broader event-emitter category; practitioner is one specific actor kind (`actor_kind: human` for practitioner-emitted events)
- Not a `specialist` — specialist is composable codified expertise (a tool the workspace activates); practitioner is the human author who employs the workspace's specialists
- Not a `workspace` — practitioners work IN workspaces; workspace serves the practitioner
- Not the `substrate`'s Instance aspect (informally "the AI runtime") — substrate's running instance is the AI side of the workspace; practitioner is human (the AI is co-worker, not the author)
- Not multiple-kinds-of-practitioner — practitioner is singular always; kind variation (solo / partnership / legal-entity-firm) lives at WORKSPACE LEVEL (multi-practitioner workspace; legal-entity workspace context), NOT at practitioner level

**Cross-archetype illustration**: practitioners across archetypes share the same role-shape (human author bearing accountability) but differ in workspace configuration:
- **Solo practitioner workspace** (PBS-Schulz pioneer): Gunther Schulz — one practitioner per workspace
- **Multi-practitioner partnership** (e.g., Müller Schmidt Weber Law): three individual practitioners sharing a workspace; each bears accountability for their own work
- **Legal-entity firm** (e.g., architecture firm): firm is the legal-entity contracting party; named architect signs each project as practitioner
- **Research lab**: principal investigator + collaborators as practitioners
- **Solo creative**: single practitioner workspace

In all cases: practitioner is one human (or natural-or-legal-person bearing accountability); workspace contains 1+ practitioners as workspace-scope managed entities.

**Boundary test**: Three questions:
1. Is this the human who signs + bears accountability for produced work? → it's a practitioner (the HUMAN aspect)
2. Is this the system's representation of that human (identity, credentials, signing authority)? → it's the practitioner-RECORD (the Owner-B aspect)
3. Is this the broader event-emitter category? → it's an `actor` (practitioner is one specific actor kind)

**Composes with**:
- [workspace](workspace.md) — workspace serves practitioner(s); multi-practitioner workspaces host N practitioners as workspace-scope managed entities; legal-entity workspace context binds firm + named practitioners
- [actor](actor.md) — practitioner is one actor kind (`actor_kind: human` per `event` schema)
- [authorship preservation (axis 3)](authorship-preservation.md) — practitioner is the role axis 3 protects
- [Owner B scope](owner-b-scope.md) — practitioner-RECORD lives here as workspace-scope managed entity (the HUMAN aspect doesn't "live" anywhere in the system; cross-cutting)
- [defensibility](defensibility.md) — operational test of axis 3; the test asks "will the practitioner be able to defend this six months from now?"
- [work-unit](work-unit.md) — practitioners are the human authors signing work-unit outputs; defensibility test asks "will the practitioner defend THIS work-unit's outputs?" (the work-unit is the bounded artifact per which defensibility is judged)
- [claim](claim.md) — practitioners are accountable for individual claims they author; the defensibility test resolves at claim granularity (practitioner defends each claim under regulatory/professional challenge)
- [category collapse](category-collapse.md) — the cognitive-state-bound force operating IN the practitioner; degrades practitioner's mental category of the AI from higher-engagement to lower-engagement state regardless of architectural intent
- [rubber-stamping](rubber-stamping.md) / [answer-machine AI](answer-machine-ai.md) / [oracle AI](oracle-ai.md) / [validator AI](validator-ai.md) / [tacked-on AI](tacked-on-ai.md) — axis-failure modes that manifest in the practitioner's engagement state at different moments (workflow integration / reasoning / attestation)

**Source**:
- VISION (`VISION.md`):
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Line 15: "expert practitioners (planners, lawyers, researchers, accountants, creatives, consultants, advisors)"
  - Line 19: "this document remains the practitioner-shape articulation"
  - Multiple references throughout axis 3 framing
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Other multi-aspect primitives": "practitioner — bipartite of different shape: HUMAN (cross-cutting; the actual person; not 'placed') + RECORD (Owner B; system representation)"
- Locked GLOSSARY entries: [authorship preservation](authorship-preservation.md) ("practitioner — the role this axis protects"); [actor](actor.md) ("practitioner is one specific actor kind"); [Owner B scope](owner-b-scope.md) ("practitioner-record (system representation...)"); [workspace](workspace.md) ("workspace serves practitioner(s); records at Owner B")

**See**:
- [authorship preservation (axis 3)](authorship-preservation.md) (the axis practitioner anchors)
- [workspace](workspace.md) (which serves practitioner; multi-practitioner workspace handles kind variation)
- [actor](actor.md) (broader category; practitioner is one kind)
- [Owner B scope](owner-b-scope.md) (where practitioner-record lives)
- ARCH Layer 3 practitioner-detail topics (placeholder until Phase 3 — multi-practitioner workspace mechanics; legal-entity workspace context; signing-practitioner-per-work-product configuration; archived material to consult: `office-level-managed-entities.md` for practitioner-record schema)
