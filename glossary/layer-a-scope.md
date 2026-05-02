---
entry: Layer A scope
class: SCOPE-CLASSIFICATION
layer: cross-cutting
axis: cross-axis
vision_usage: implicit
---

# Layer A scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: cross-cutting (orthogonal to mechanism/policy split)
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory)

**Canonical**: The scope category for LAYERED CONTENT — content varying by deployment context (universal / domain-keyed / state-keyed). **Orthogonal axis** to framework/shape framing (about content scoping, not mechanism vs policy).

**What it is**: One of three scope classifications. Layer A is **independent** of the framework=mechanisms / shape=policies framing — it's an axis for content layering by domain/state context. Identity is by `layer_scope` + `layer_key` in entity-md frontmatter. Effective content for a workspace = universal + active-domains + active-states (workspace declares which apply via its scope configuration).

**Members**:
- references (e.g., legal texts; vary by jurisdiction)
- doctypes (e.g., B-Plan-Begründung is domain-specific)
- bausteine (saved text patterns; can be domain or state specific)
- memory prose (style-spec, korrektur-rules, verfahren docs; could be domain-specific)
- conventions (writing conventions per language / jurisdiction)
- domain-specific knowledge artifacts

**Layer values**:
- `universal` — applies to every deployment regardless of domain or jurisdiction
- `domain` — applies to deployments in specific domains (e.g., PV-FFA, Wind, Naturschutz, Innenentwicklung); multiple domains can be active simultaneously
- `state` — applies to deployments in specific jurisdictions (e.g., DE-BB, DE-BY, DE-BW, ...); multiple states can be active simultaneously

**What it is NOT**:
- Not derived from framework/shape (it's an INDEPENDENT classification axis)
- Not the same as framework's universal-vs-shape-specific distinction (Layer A is about CONTENT applicability by deployment context, not about mechanism vs policy)
- Not for definitions (those are Framework C)
- Not for instances (those are Owner B)

**Boundary test**: ask "does this content vary by deployment context (domain / state / universal)?" If yes → Layer A. "Is this a definition?" → Framework C. "Is this an instance bound to deployment?" → Owner B.

**Composes with**:
- [workspace](workspace.md) — workspace's scope configuration (active domains, active states) determines which Layer A content applies
- references / doctypes / bausteine / prose conventions — content kinds that live at Layer A

**Source**: 3-axis scope orthogonality (Layer A / Owner B / Framework C); orthogonal-to-framework/shape per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)
