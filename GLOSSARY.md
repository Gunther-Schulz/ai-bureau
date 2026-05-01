# Glossary

Canonical source for term definitions across the pbs-bureau corpus. Per `MAINTENANCE.md` cascade discipline, all docs cite GLOSSARY for term meaning rather than redefining.

## How entries are structured

Each entry is tagged on 4 axes (per `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section):

- **Class**: PRIMITIVE (atomic) / META-PRIMITIVE (container) / DERIVED (composition) / SCOPE-CLASSIFICATION
- **Layer**: framework-mechanism / shape-policy / cross-cutting / dual-nature / framework-meta
- **Axis**: axis-1 / axis-2 / axis-3 / cross-axis (where applicable)
- **VISION usage**: directly used / implicit / derived-from-VISION-terms / framework-meta

Tags are a means, not an end. If an entry is clearer with fewer tags, drop the extras.

**On entry-by-entry locking (cascade prevention of inherited-framing bias)**: GLOSSARY is built foundation-up. Earlier entries may forward-reference terms not yet locked; later entries reference earlier ones. Discipline:

1. **Greenfield-draft** new entries from VISION + `MAINTENANCE.md` (locked architectural commitments) + first principles — NOT from prior entries' cross-references to this term as anchors
2. **Minimize embedded descriptions** of not-yet-locked terms — use brief role tags + cross-ref to authoritative source (`MAINTENANCE.md` or forthcoming entry); don't carry the not-yet-locked term's "definition" inline in current entry
3. **Cascade-pass after locking** per `MAINTENANCE.md` cascade discipline — review all prior cross-references to the new term; reconcile inconsistencies in the same commit

This prevents earlier-drafted cross-refs from biasing later canonical definitions.

**The three axes** referenced in tags map to VISION axes:
- **axis-1** = intertwining (workflow embedding)
- **axis-2** = sparring (interaction mode)
- **axis-3** = authorship preservation (outcome orientation)

Each axis has its own glossary entry below; full claims live in `VISION.md`.

Entries are alphabetical (case-insensitive). Cross-references are explicit; reading any entry should make the term's place in the architecture immediately clear.

---

## authorship preservation (axis 3)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-3
- **VISION usage**: directly used (`VISION.md` axis 3 — third interlocking principle)

**Canonical**: The architectural commitment that the practitioner remains the defensible expert author of everything PBS produces on their behalf — capable of defending, signing, and standing behind the produced work; per VISION axis 3.

**What it is**: The third VISION axis. PBS is an output-producing tool for an expert practitioner; the produced work goes out under the practitioner's name; the practitioner is legally and professionally accountable. Authorship preservation protects this professional/legal standing — no rubber-stamping, no signature without engagement, no work the practitioner can't defend. The operational test for this axis is `defensibility`.

**What it is NOT**:
- Not "user understanding" in the abstract (it's about *defending under regulatory or professional challenge*)
- Not capacity-building (capacity-building is a side effect when it happens; authorship preservation is the actual purpose)
- Not generic "human-in-the-loop" (humans-in-loop without engagement still rubber-stamp)
- Not output quality (quality is necessary but insufficient — the practitioner must be able to DEFEND it)

**Cross-archetype illustration**: legal practice signing briefs; medical practice signing case notes; planning bureau signing Begründungen; auditor signing audit reports — same axis applies wherever the practitioner-author bears regulatory/professional accountability.

**Boundary test**: ask "will the practitioner be able to defend this output six months from now under regulatory or professional challenge, having forgotten the details?" If no, axis 3 fails.

**Composes with**:
- `defensibility` — operational test for this axis (canonical entry forthcoming)
- `authorship mechanisms` — class of axis-3 mechanisms (canonical entry forthcoming)
- `practitioner` — the role this axis protects (canonical entry forthcoming)
- `practitioner-shape` — workspace shape where this axis is mandated (canonical entry forthcoming; see `shape` named-shapes catalog)

**Source**: VISION axis 3 (third principle of the thesis); "Authorship preservation, not rubber-stamping" section; the defensibility test.

**See**:
- VISION's "Authorship preservation, not rubber-stamping (axis 3)" section for full claim
- ARCH Layer 3 axis-3-mechanism topic (placeholder until Phase 3)

---

## framework

- **Class**: META-PRIMITIVE (container; the bounded category that contains mechanisms, protocols, and architectural disciplines)
- **Layer**: framework-meta (this entry describes the framework layer itself)
- **Axis**: cross-axis (the framework supports all three VISION axes; specific support per axis lives in mechanisms)
- **VISION usage**: directly used (`VISION.md` lines 17, 21, 72)

**Canonical**: The shape-neutral universal layer of the pbs-bureau architecture — the bounded set of mechanisms (atomic interface contracts), architectural protocols (pluggable subsystems), and architectural disciplines that any workspace shape can compose with.

**What it is**: The "what's POSSIBLE" boundary. The framework defines the universe of capabilities, contracts, and rules available to any workspace. The framework/shape architectural relationship — what's POSSIBLE (framework) vs what's MANDATED (shape) — is locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. The framework is the open-source, marketed product's foundation; PBS-Schulz is one practitioner-shape deployment built from the framework.

The framework includes:
- **mechanisms** (audit emission, source-grounding, sparring Protocol surface, etc.)
- **architectural protocols** (Coordination, Audit, Sparring, Trust, Time as pluggable subsystems with multiple implementations)
- **architectural disciplines** (cascade discipline, no-defer principle, preliminary-lock principle, make-wrong-shapes-impossible, AI-as-runtime hybrid-shape, pattern-vs-instance, glue-not-replacement)

**What it is NOT**:
- Not a specific shape's configuration (shape is the policy layer OVER the framework)
- Not the substrate (substrate is one mechanism within the framework's scope; framework is the layer that contains substrates among other mechanisms)
- Not the codebase per se (framework is the architectural layer; the codebase is one realization of the framework's mechanisms)
- Not a workspace or deployment instance (workspaces are BUILT FROM framework + shape policies + practitioners + state)
- Not market positioning or strategic claims (framework is shape-neutral; positioning lives in `STRATEGY.md`)

**Cross-archetype illustration**: All workspace archetypes share the SAME framework; they differ in which shape's policies they apply over framework mechanisms. Example shapes: practitioner-shape (PBS marketed positioning), autonomous-business-shape, personal-OS-shape, knowledge-graph-shape, federation-shape, hybrid-shape. Per-shape policy specifics live in canonical shape entries forthcoming (see `shape` entry for the meta-primitive). Same framework underwrites all archetypes; shape policies determine what each one mandates.

**Boundary test**: Two questions:
1. "Is this thing shape-specific (only valid for one shape)?" If yes → not framework; it's shape-policy or shape-specific primitive.
2. "Is this thing an interface contract any shape could use?" If yes → framework-mechanism (lives within the framework).

If a candidate concept fails test 1 (it IS shape-specific), it doesn't belong in the framework. Move to shape-extension.

**Composes with**:
- `mechanism` — atomic units of the framework (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; canonical entry forthcoming)
- `protocol` (architectural) — pluggable subsystems within the framework (canonical entry forthcoming)
- `shape` — counterpart in the framework/shape architectural relationship (canonical entry forthcoming; relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `workspace` — deployment-instance container that integrates framework + shape + specialists + practitioners (canonical entry forthcoming)

**Source**: VISION (`VISION.md`):
- Line 17: "The framework underneath is workspace-shape-neutral. Framework primitives support multiple workspace shapes via shape-extension pattern"
- Line 21: "The framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
- Line 72: "PBS does NOT claim the framework is restricted to practitioner shape — framework is shape-neutral; positioning is practitioner-focused"

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section (the foundational architectural commitment)
- ARCH Layer 2 overview + Layer 3 framework-detail topics (placeholder until Phase 3)
- Other foundational meta-primitives: `shape`, `mechanism`, `policy`

---

## Framework C scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: framework-meta (placement category for framework primitive definitions)
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory; VISION doesn't directly use this term)

**Canonical**: The scope category for framework primitive DEFINITIONS — universal, immutable, distributable; the placement home for entity-md instances that define mechanisms, shapes, substrates, protocol-implementations, and specialist DEFINITIONS. Derived from `framework = mechanisms` (mechanism definitions live here) plus the framework's other distributable elements.

**What it is**: One of three scope classifications (Framework C / Owner B / Layer A) governing where entity-md instances live. Framework C is the "definitions" home — distributable, marketplace-listable (per ROADMAP v3), immutable at definition level. Identity is by `framework_kind` + `framework_key` in entity-md frontmatter.

**Members**:
- mechanism definitions (atomic interface contracts authored at framework level)
- shape definitions (policy bundles for an archetype)
- substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)
- protocol-implementation definitions (concrete impls: always-on-sparring, claim-level-audit, etc.)
- specialist DEFINITIONS (canonical entry forthcoming; dual-nature primitive: DEFINITION here, INSTANCE-CONTENT in Owner B)

**What it is NOT**:
- Not for instances (those go to Owner B)
- Not for layered content varying by domain/state (that's Layer A)
- Not for runtime state

**Boundary test**: ask "is this a distributable definition that any workspace shape could potentially use?" If yes → Framework C. "Is this an instance bound to a deployment?" → Owner B. "Is this content varying by domain/state?" → Layer A.

**Composes with**:
- `framework` — Framework C IS where framework primitive definitions live
- `shape` — shape definitions live in Framework C
- `mechanism`, `substrate`, `protocol`, `specialist` (DEFINITION) — all live in Framework C
- `Owner B scope` — where INSTANCES of Framework C definitions get deployed

**Source**: derived from session-15 entity-md scope model restructure; refined session 16 under `framework = mechanisms` / `shape = policies` framing.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## intertwining (axis 1)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-1
- **VISION usage**: directly used (`VISION.md` axis 1 — first interlocking principle)

**Canonical**: The integration depth where AI is a continuous co-worker IN the workflow itself, not a discrete feature bolted onto an unchanged workflow; per VISION axis 1.

**What it is**: The first VISION axis. AI participates in real work output — drafts, retrieves, decides, acts as orchestrating colleague — rather than offering convenience features (summarize this; format that) on the side. Requires architectural support: persistent state, orchestration, source-grounding, audit trail, continuous awareness, and explicit human-authority gates.

**What it is NOT**:
- Not "more AI" or "better AI" (it's a different SHAPE of integration, not a different magnitude)
- Not "AI agents" generically (most "AI agent" demos are still tacked-on)
- Not requiring AI to do the bulk of the work (could be 20% mechanical labor; the integration depth matters, not the labor share)
- Not generic "automation" (automation can be tacked-on too)

**Cross-archetype illustration**: planning bureau co-drafting Begründungen with AI in real workflow; legal practice with AI as co-worker on briefs; research lab with AI as co-author on manuscripts; auditor with AI as co-worker on audit findings — all instances of axis 1's deep integration.

**Boundary test**: ask "is the AI a participating colleague in actual work production, or a discrete convenience feature on the side?" If feature-on-the-side → tacked-on AI (failure mode for axis 1).

**Composes with**:
- `tacked-on AI` — the failure mode contrasted (canonical entry forthcoming)
- `intertwined AI` — positive mode (canonical entry forthcoming)
- `co-worker` — relational claim about AI's mode of participation (canonical entry forthcoming)
- `trust mechanisms` — class of axis-1 mechanisms (canonical entry forthcoming)
- `workflow` — what intertwining intertwines WITH (canonical entry forthcoming)
- `category collapse` — risk to axis 1 (canonical entry forthcoming)

**Source**: VISION axis 1 (first principle of the thesis); contrast table (tacked-on vs intertwined).

**See**:
- VISION "The thesis" axis 1 + tacked-on/intertwined contrast table
- VISION "Implications" → "Workflow as precondition" + "Category-collapse risk"
- ARCH Layer 3 axis-1-mechanism topic (placeholder until Phase 3)

---

## Layer A scope

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
- `workspace` — workspace's scope configuration (active domains, active states) determines which Layer A content applies
- references / doctypes / bausteine / prose conventions — content kinds that live at Layer A

**Source**: predates session-16 rebuild (3-axis scope orthogonality from earlier ARCH); refined session 16 to clarify orthogonal-to-framework/shape status.

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## Owner B scope

- **Class**: SCOPE-CLASSIFICATION
- **Layer**: cross-cutting
- **Axis**: cross-axis
- **VISION usage**: implicit (ARCH territory)

**Canonical**: The scope category for INSTANCES — deployment-specific entities owned at the workspace, specialist-instance, or work-unit-instance level; the placement home for entity-md instances that materialize in a particular deployment. Derived from `framework + shape → workspace deployment`.

**What it is**: One of three scope classifications. Owner B is the "instances" home — where definitions (Framework C) get DEPLOYED and bound to workspace context. Identity is by `owner_scope` + `owner_key` in entity-md frontmatter.

**Members**:
- workspace itself (workspace.md selecting shape + substrate + active specialists)
- workspace-scope managed entities:
  - practitioner-record (system representation; canonical `practitioner` entry forthcoming; dual-aspect: human cross-cutting, record at Owner B)
  - Actor (event emitter; canonical entry forthcoming)
  - Client (engagement target; canonical entry forthcoming)
  - additional managed entities per workspace's needs
- specialist instance content (entities owned within an active specialist instance — distinct from specialist DEFINITION which is Framework C)
- work-unit instances (kind specialist-defined: `project` for planning bureau; `matter` for legal practice; `case` for medical practice; `engagement` for consulting; `manuscript` for research; `audit` for accounting)

**What it is NOT**:
- Not for definitions (those are Framework C)
- Not for layered content (that's Layer A)
- Not where the practitioner-as-human "lives" (the human is cross-cutting; only the practitioner-record is placed)

**Boundary test**: ask "is this a deployment-specific instance bound to a workspace, specialist instance, or work-unit?" If yes → Owner B. "Is this a distributable definition?" → Framework C. "Is this content varying by deployment context (domain/state)?" → Layer A.

**Composes with**:
- `workspace` — the central Owner B instance + container for workspace-scope managed entities
- `specialist` — instance content sits at Owner B (distinct from specialist DEFINITION at Framework C)
- `work-unit` (kind specialist-defined) — instances at Owner B
- `practitioner` — record at Owner B; human itself cross-cutting
- `Framework C scope` — where the DEFINITIONS that get instantiated live

**Source**: derived from session-15 entity-md scope model restructure; refined session 16 (practitioner-record added per practitioner dual-aspect; orthogonal-Layer-A clarified).

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section "A-B-C scope model"
- ARCH Layer 3 entity-md spec (placeholder until Phase 3)

---

## shape

- **Class**: META-PRIMITIVE (container; the category of policy bundles, not a single policy itself)
- **Layer**: framework-meta (this entry describes the shape layer concept itself)
- **Axis**: cross-axis (shapes can have policies serving any axis)
- **VISION usage**: directly used (`VISION.md` lines 11, 17, 19, 21, 72)

**Canonical**: A workspace archetype — a bundle of policies layered over framework mechanisms, configuring what's MANDATED for that archetype. Shape definitions are themselves framework primitives (live in Framework C scope); a workspace selects exactly one shape via its `workspace.md`.

**What it is**: A shape provides the "what's MANDATED" layer for a workspace archetype, per the framework/shape architectural relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE. Each shape declares its policies + may add shape-specific primitives needed for its archetype. PBS as marketed product positions on practitioner-shape; the framework underneath is shape-neutral and supports multiple shapes.

**What it is NOT**:
- Not a workspace (a workspace IS DEPLOYED as a specific shape's archetype; the shape is the configuration definition)
- Not the framework (shape sits OVER framework per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; framework is the universal mechanism layer)
- Not a deployment instance (shape DEFINITIONS are universal/distributable; live in Framework C scope; per-deployment selection happens via `workspace.md`)
- Not a single policy (shape is a BUNDLE; `policy` canonical entry forthcoming)
- Not always practitioner-shape (PBS markets practitioner-shape; framework supports multiple shapes — see named-shapes catalog below)

**Cross-archetype catalog (named shapes — canonical per-shape detail forthcoming)**:
- **practitioner-shape** — workspace shape for accountability-bearing expert work; PBS marketed positioning + pioneer reference
- **autonomous-business-shape** — operator-supervised multi-agent shop
- **personal-OS-shape** — individual life-OS
- **knowledge-graph-shape** — corpus + curation; no workflow loop
- **federation-shape** — cross-node specialist sharing
- **hybrid-shape** — combinations of above

**Boundary test**: Three questions:
1. Is this an atomic unit contained within a shape (one element of its bundle)? → it's a `policy` (canonical entry forthcoming)
2. Is this an interface contract any shape could use? → it's a `mechanism` (canonical entry forthcoming; lives in framework, not shape)
3. Is this a bundle of policies for a workspace archetype? → it's a shape

**Composes with**:
- `framework` — counterpart in the framework/shape architectural relationship (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `policy` — atomic unit contained within a shape's bundle (canonical entry forthcoming)
- `workspace` — deploys exactly one shape via `workspace.md` (canonical entry forthcoming)
- `Framework C scope` — where shape DEFINITIONS live as distributable framework primitives
- `mechanism` — what shape policies configure (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE; canonical entry forthcoming)

**Source**:
- VISION (`VISION.md`):
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Line 17: "Framework primitives support multiple workspace shapes via shape-extension pattern"
  - Line 19: "this document remains the practitioner-shape articulation"
  - Line 21: "framework breadth (which shapes the framework supports + how the framework structurally encodes value claims) is ARCH territory"
  - Line 72: "framework is restricted to practitioner shape — framework is shape-neutral"
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" for framework/shape relationship + concept-by-concept worked examples
- `Framework C scope` (where shape definitions live)
- ARCH Layer 3 shape topic + per-shape detail (placeholder until Phase 3)
- Other foundational meta-primitives: `framework`, `mechanism`, `policy`

---

## sparring (axis 2)

- **Class**: DERIVED (claim/mode defined in VISION)
- **Layer**: cross-cutting
- **Axis**: axis-2
- **VISION usage**: directly used (`VISION.md` axis 2 — second interlocking principle)

**Canonical**: An interaction mode where AI challenges, generates counter-arguments, names uncertainty, and resists giving easy answers; load-bearing runtime mechanism per VISION axis 2 (not optional skill).

**What it is**: The second VISION axis. AI participates in sparring-mode interaction, distinct from oracle-mode (humans submit AI's answer as their own; performance same as AI alone) or validator-mode (humans ask AI to support preconceptions; sycophancy loop; performance worse than AI alone). Per Vivienne Ming's research, only sparring-mode produces value rivaling or beating prediction markets. Sparring keeps the practitioner critically engaged.

**What it is NOT**:
- Not optional skill called per-task (it's a load-bearing runtime PILLAR in practitioner-shape)
- Not antagonistic-AI for its own sake (sparring is in service of the practitioner-author's growing capacity, not for confrontation)
- Not sparring-always (oracle mode is right for fact lookup; sparring overhead misplaced for trivial questions)
- Not the same as "sparring mechanisms" (the mechanisms — counter-argument, confidence calibration, etc. — are framework-level capabilities; sparring is the MODE characterized by these mechanisms)

**Cross-archetype illustration**: legal practice sparring on legal arguments; research lab sparring on methodology + manuscript claims; planning bureau sparring on Begründung argumentation choices; auditor sparring on audit-finding interpretations — same axis applies wherever practitioner faces nontrivial judgment calls.

**Boundary test**: ask "does the AI challenge / generate counter-arguments / surface uncertainty, or deliver easy answers?" If easy-answers → answer-machine failure mode (axis 2 failure).

**Composes with**:
- 8 sparring sub-mechanisms (canonical entries forthcoming): `counter-argument`, `confidence calibration`, `visible reasoning`, `selective friction`, `asymmetric knowledge respect`, `anti-sycophancy`, `commit-to-recommendations`, `what's-missing`
- `sparring mechanisms` — class of axis-2 mechanisms (canonical entry forthcoming)

**Source**: VISION axis 2 (second principle of the thesis) + Vivienne Ming foundation; "Sparring partner, not answer machine" section.

**See**:
- VISION "Sparring partner, not answer machine (axis 2)" section + Foundations Vivienne Ming subsection
- ARCH Layer 3 axis-2-mechanism topic (placeholder until Phase 3)
