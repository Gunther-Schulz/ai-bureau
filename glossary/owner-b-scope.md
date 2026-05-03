---
entry: Owner B scope
class: SCOPE-CLASSIFICATION
layer: cross-cutting
axis: cross-axis
vision_usage: implicit
---

# Owner B scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: cross-cutting
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory)

**Canonical**: The scope category for INSTANCES — deployment-specific entities owned at the workspace, specialist-instance, or work-unit-instance level; the placement home for entity-md instances that materialize in a particular deployment. Derived from `framework + shape → workspace deployment`.

**What it is**: One of three scope classifications. Owner B is the "instances" home — where definitions (Framework C) get DEPLOYED and bound to workspace context. Identity is by `owner_scope` + `owner_key` in entity-md frontmatter.

**Members**:
- workspace itself (workspace.md selecting shape + substrate + active specialists)
- workspace-scope managed entities (universal across shapes):
  - practitioner-record (system representation; per `practitioner` entry — bipartite: human cross-cutting, record at Owner B)
  - Actor (event emitter; one of `actor_kind: human / ai_runtime / external`)
  - additional managed entities per shape-policy mandate (NOT framework-level): each shape may mandate its own engagement-target managed entity — e.g., practitioner-shape mandates `Client` (engagement target for accountability-bearing service); autonomous-business-shape mandates `Customer`; research-lab-shape mandates `Funder` / `Co-author` / `Institution`; etc. Engagement-target entities are deliberately shape-policy-mandated rather than framework-level because they're not universal across archetypes (personal-OS-shape has no engagement-target).
- specialist instance content (entities owned within an active specialist instance — distinct from specialist DEFINITION which is Framework C)
- work-unit instances per Pattern B INSTANCE aspect (kind specialist-defined at DEFINITION aspect: `project` for planning bureau; `matter` for legal practice; `case` for medical practice; `engagement` for consulting; `manuscript` for research; `audit` for accounting)

**What it is NOT**:
- Not for definitions (those are Framework C)
- Not for layered content (that's Layer A)
- Not where the practitioner-as-human "lives" (the human is cross-cutting; only the practitioner-record is placed)

**Boundary test**: ask "is this a deployment-specific instance bound to a workspace, specialist instance, or work-unit?" If yes → Owner B. "Is this a distributable definition?" → Framework C. "Is this content varying by deployment context (domain/state)?" → Layer A.

**Composes with**:
- [workspace](workspace.md) — the central Owner B instance + container for workspace-scope managed entities
- [specialist](specialist.md) — instance content sits at Owner B (distinct from specialist DEFINITION at Framework C)
- [work-unit](work-unit.md) — Pattern B primitive: KIND DEFINITION at Framework C via specialist's bundle; INSTANCE at Owner B as workspace-scope managed entity
- [practitioner](practitioner.md) — record at Owner B; human itself cross-cutting
- [Framework C scope](framework-c-scope.md) — where the DEFINITIONS that get instantiated live

**Source**: derived from entity-md scope model; practitioner-record at Owner B per practitioner dual-aspect; orthogonal-to-Layer-A.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- `arch/scope-model.md` (Phase 3.5 forthcoming — Workspace + Framework C / Owner B / Layer A scope categories + entity placement)
