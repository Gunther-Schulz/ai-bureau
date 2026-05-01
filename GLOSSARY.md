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
- `mechanism` — atomic units of the framework (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `protocol` (architectural) — pluggable subsystems within the framework (canonical entry forthcoming)
- `shape` — counterpart in the framework/shape architectural relationship (canonical entry forthcoming; relationship locked in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `workspace` — deployment-instance container that integrates framework + shape + specialists + practitioners

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

## mechanism

- **Class**: PRIMITIVE (atomic; irreducible unit of the framework)
- **Layer**: framework-mechanism (this entry describes the atomic unit at the framework layer)
- **Axis**: cross-axis (mechanisms can serve any of the three VISION axes)
- **VISION usage**: implicit (VISION uses "mechanisms" in plural for trust/sparring/authorship mechanism classes; doesn't define "mechanism" as singular term — that's `MAINTENANCE.md` territory)

**Canonical**: An atomic interface contract within the framework — a single capability with defined input/output surface, available to any workspace shape; the smallest unit of "what's POSSIBLE" the framework provides.

**What it is**: The atomic unit of the framework. Mechanisms are universal — usable by any shape, no shape-specific values embedded. They define WHAT'S POSSIBLE; shape policies determine WHAT'S MANDATED out of those possibilities. Multiple mechanisms compose into the framework alongside protocols (pluggable subsystems) and architectural disciplines (rules), per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table):
- `AuditEvent` schema (Pydantic model contract for audit emission)
- `actor_kind` enum (declared on every audit event; framework-level guarantee)
- Pydantic gate (validator function dispatched on every contract-bearing write)
- Specialist conformity manifest schema (declaring a specialist's conformity surface as a Pydantic schema)
- Sparring Protocol surface (the architectural-protocol's interface contract, before any specific implementation)
- Source-grounding capability (every claim traceable to source; framework-level enforcement)
- Visible reasoning capability (Pydantic field on outputs requiring reasoning chain)

**What it is NOT**:
- Not a `policy` — policies are atomic CONFIGURED VALUES (defaults, requirements, constraints) within a shape's bundle; mechanisms are atomic INTERFACE CONTRACTS in the framework
- Not a `protocol` (architectural; canonical entry forthcoming) — a protocol's surface IS a mechanism, but the protocol-with-multiple-implementations structure adds composition beyond a single mechanism
- Not the `framework` itself — the framework is the CONTAINER of mechanisms (+ protocols + disciplines); a single mechanism is one element of the container
- Not a workspace-level or instance-level construct — mechanisms live at framework level with no shape-specific values
- Not an architectural discipline — disciplines are RULES about how to design (canonical homes: `MAINTENANCE.md` + `DISCIPLINES.md`); mechanisms are CAPABILITIES the framework provides

**Cross-archetype illustration**: All workspace shapes use the SAME mechanisms (e.g., the `AuditEvent` schema is the same Pydantic contract in practitioner-shape, autonomous-business-shape, etc.). What differs across shapes is which mechanisms are MANDATORY, the granularity at which they're invoked, and what defaults apply — these are policies (shape-level), not mechanism variations.

**Boundary test**: Three questions:
1. Is this an atomic capability with a defined input/output surface? → likely a mechanism
2. Is this shape-neutral (any shape could use it)? → likely a mechanism (lives in framework)
3. Is this a configured value (default, requirement, mandatory)? → it's a `policy`, not a mechanism

If a candidate fails test 2 (it IS shape-specific), it doesn't belong as a framework mechanism. Move to shape-extension.

**Composes with**:
- `framework` — contains mechanisms as its atomic interface contracts (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `policy` — counterpart atom in the framework=mechanisms / shape=policies framing
- `shape` — applies policies OVER mechanisms (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `protocol` (architectural) — pluggable subsystem within the framework (canonical entry forthcoming; relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "mechanism is the atom — a single interface contract; capability with defined input/output surface"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: examples per axis (audit emission, specialist modification, authority binding, sparring)

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: `framework`, `shape`, `policy`
- ARCH Layer 3 mechanism-detail topics (placeholder until Phase 3 — per-mechanism canonical detail)

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

## policy

- **Class**: PRIMITIVE (atomic; irreducible unit of a shape's bundle)
- **Layer**: shape-policy (this entry describes the atomic unit at the shape layer)
- **Axis**: cross-axis (policies can configure any axis-related mechanism)
- **VISION usage**: implicit (VISION doesn't use "policy" as a defined term; the framework=mechanisms / shape=policies framing is locked in `MAINTENANCE.md`, not VISION)

**Canonical**: An atomic configured value within a shape — a single requirement, default, or constraint configuring how a framework mechanism is used for that shape's archetype; the smallest unit of "what's MANDATED" a shape declares.

**What it is**: The atomic unit of a shape's policy bundle. Policies are shape-level — they configure framework mechanisms for a specific archetype, with shape-specific values. They define WHAT'S MANDATED (out of what the framework's mechanisms make POSSIBLE). Multiple policies compose into a shape's bundle; the shape is the container.

**Examples** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE concept-by-concept table; practitioner-shape policies):
- Audit granularity = claim-level (configures the framework's audit-emission mechanism)
- Sparring always-on as runtime pillar (configures the sparring mechanism)
- Human authority required somewhere in accountability-bearing output chain (configures authority-binding mechanism)
- Modifications require explicit re-conformance event (configures specialist-modification mechanism)
(Per other shapes, different policies configure the same mechanisms differently — see cross-archetype illustration below.)

**What it is NOT**:
- Not a `mechanism` — mechanisms are atomic INTERFACE CONTRACTS in the framework; policies are atomic CONFIGURED VALUES in a shape
- Not a `shape` — shape is the BUNDLE of policies (container); a single policy is one element
- Not a workspace-instance configuration — policies live at SHAPE level (in a shape definition's bundle); workspace deployments inherit them from the selected shape
- Not the framework — framework provides the mechanisms; policies live in shapes that layer over the framework

**Cross-archetype illustration** (same mechanism, different policies per shape): the framework provides the audit-emission MECHANISM (AuditEvent schema + `actor_kind` enum). Different shapes declare different POLICIES configuring it:
- Practitioner-shape policy: audit granularity = claim-level; emission required for every output
- Autonomous-business-shape policy: audit granularity = action-level; emission per task
- Personal-OS-shape policy: audit granularity = light; emission optional

Same mechanism (the framework's audit-emission contract); different policies (each shape's archetype-specific values).

**Boundary test**: Three questions:
1. Is this a configured value (a default, requirement, or constraint)? → likely a policy
2. Is this shape-specific (varies by archetype)? → likely a policy (lives in a shape's bundle)
3. Is this an interface contract any shape could use? → it's a `mechanism`, not a policy

If a candidate fails test 2 (it's universal across shapes; no archetype variation), it's not a policy — it's mechanism territory.

**Composes with**:
- `shape` — contains policies as its atomic bundle elements (atom-vs-container relationship per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `mechanism` — counterpart atom in the framework=mechanisms / shape=policies framing (mechanism = framework atom; policy = shape atom)
- `framework` — contains mechanisms over which policies are LAYERED (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `workspace` — selects a shape and inherits its policies

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Framework = mechanisms; Shape = policies" section: "policy is the atom — a single configured value; requirement/default/constraint"
- `MAINTENANCE.md` "Concept-by-concept (worked examples)" table: practitioner-shape column = examples of policies per axis

**See**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" section (atom-vs-container relationship + concept-by-concept worked examples)
- Other foundational meta-primitives + atoms: `mechanism`, `framework`, `shape`
- `Framework C scope` — where shape definitions (containing policy bundles) live
- ARCH Layer 3 per-shape policy-detail topics (placeholder until Phase 3)

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
- Not a single policy (shape is a BUNDLE)
- Not always practitioner-shape (PBS markets practitioner-shape; framework supports multiple shapes — see named-shapes catalog below)

**Cross-archetype catalog (named shapes — canonical per-shape detail forthcoming)**:
- **practitioner-shape** — workspace shape for accountability-bearing expert work; PBS marketed positioning + pioneer reference
- **autonomous-business-shape** — operator-supervised multi-agent shop
- **personal-OS-shape** — individual life-OS
- **knowledge-graph-shape** — corpus + curation; no workflow loop
- **federation-shape** — cross-node specialist sharing
- **hybrid-shape** — combinations of above

**Boundary test**: Three questions:
1. Is this an atomic unit contained within a shape (one element of its bundle)? → it's a `policy`
2. Is this an interface contract any shape could use? → it's a `mechanism` (lives in framework, not shape)
3. Is this a bundle of policies for a workspace archetype? → it's a shape

**Composes with**:
- `framework` — counterpart in the framework/shape architectural relationship (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- `policy` — atomic unit contained within a shape's bundle
- `workspace` — deploys exactly one shape via `workspace.md`
- `Framework C scope` — where shape DEFINITIONS live as distributable framework primitives
- `mechanism` — what shape policies configure (which active / mandatory / defaults; per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)

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

---

## substrate

- **Class**: PRIMITIVE (atomic; the deployment-runtime unit) — with **dual-nature** (Protocol surface = mechanism; implementations = Framework C definitions; running instance = workspace-bound at Owner B)
- **Layer**: dual-nature (framework-mechanism for the Protocol surface; Framework C for implementations; cross-cutting at workspace runtime)
- **Axis**: cross-axis (substrate hosts all axes' runtime behavior)
- **VISION usage**: implicit (VISION doesn't directly use "substrate"; concept lives in `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE + Framework C scope members)

**Canonical**: A deployment runtime that workspaces run on — defines the agent loop, tool/MCP-server registration, permission flow, hook events, and session/context primitives via a Protocol surface; concrete implementations (Claude Agent SDK, MS Agent Framework, future) live as Framework C definitions; a workspace selects exactly one substrate via its `workspace.md`.

**What it is**: One of the framework's mechanism categories (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE). The substrate provides the runtime contract any workspace operates on. The Protocol surface (interface contract) is universal/shape-neutral; specific implementations differ in how they realize that surface (e.g., Claude Agent SDK = Anthropic plugin runtime; MS Agent Framework = Microsoft agentic framework). **Substrate is an instance of the Protocol pattern** (per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE "Recurring patterns: Protocol pluggability"): Substrate Protocol Surface (mechanism; framework-level) + concrete Implementations (Framework C definitions: Claude Agent SDK, MS AF, future) + a running Instance bound to each workspace deployment (Owner B; via `workspace.md` `substrate:` field). NOT the same as specialist's dual-nature (specialist is bipartite definition+instance-content; no multiple implementations).

**What it is NOT**:
- Not the `framework` itself — framework is the universal mechanism layer; substrate is one mechanism category within the framework
- Not a `shape` — shape is the policy bundle archetype; substrate is a runtime-contract mechanism that shapes specify compatibility with (not equivalent)
- Not a `workspace` — workspaces select a substrate via `workspace.md`; substrate is what they run ON
- Not the `codebase` — substrate is the architectural runtime contract + its implementations; the codebase realizes one substrate impl

**Cross-archetype illustration**: All shapes use SOME substrate; not all shapes are compatible with all substrates. Examples (named, factually existing):
- **Claude Agent SDK** — Anthropic's plugin/agent runtime; archived as primary substrate per session-12 substrate eval
- **MS Agent Framework** — Microsoft's agentic framework; archived as second backend
- (Future substrates may emerge — e.g., specialized runtimes for Tier-3 / federation / autonomous-business shapes)

A practitioner-shape PBS-Schulz workspace might run on Claude Agent SDK; a knowledge-graph-shape workspace might run on a different substrate optimized for retrieval; the SAME framework mechanisms (audit emission, source-grounding, etc.) compose with each.

**Boundary test**: ask "what's the runtime contract this workspace operates on?" → it's the substrate. Three disambiguators:
1. Is this a runtime-contract Protocol surface or implementation? → substrate (mechanism + Framework C definition)
2. Is this a configured value in a shape's bundle? → it's a `policy`, not substrate
3. Is this a workspace-instance-level binding? → it's workspace configuration (workspace selects which substrate)

**Composes with**:
- `framework` — substrate is one mechanism category within the framework
- `mechanism` — the substrate's Protocol surface IS a mechanism (framework-level interface contract)
- `Framework C scope` — substrate IMPLEMENTATIONS live here as distributable definitions
- `shape` — shapes declare compatibility with substrates (not all shapes work on all substrates)
- `workspace` — workspace selects exactly one substrate via `workspace.md`
- `Owner B scope` — running substrate instance is bound to workspace deployment (Owner B)
- `protocol` (architectural) — substrate Protocol surface is one of the framework's architectural Protocols (canonical entry forthcoming)

**Source**:
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE" — substrate listed as Framework C definition member + framework-mechanism category
- `Framework C scope` GLOSSARY entry: "substrate definitions (runtime contracts: Claude Agent SDK, MS AF, future)"
- `workspace` GLOSSARY entry: "workspace runs on exactly one substrate"

**See**:
- `Framework C scope` (where substrate definitions live)
- `workspace` (which selects exactly one substrate)
- ARCH Layer 3 substrate-detail topics (placeholder until Phase 3 — Substrate Protocol method set; per-substrate implementation detail; deployment-tier framing; eval-framework integration; archived material to consult: `substrate-protocol-design.md`, `substrate-agentic-framework.md`, `sdk-deep-read.md`)

---

## workspace

- **Class**: PRIMITIVE (atomic; the deployment-instance unit)
- **Layer**: cross-cutting (workspace integrates framework mechanisms + shape policies + practitioners; orthogonal to mechanism/policy split per `MAINTENANCE.md` TOP-LEVEL ARCHITECTURE)
- **Axis**: cross-axis (workspace is the container in which all three VISION axes manifest)
- **VISION usage**: directly used (`VISION.md` thesis line 7 + cross-archetype examples throughout)

**Canonical**: The deployment-instance container that integrates framework mechanisms + shape policies + active specialists + practitioners + state into a coherent unit for accountability-bearing work; selects exactly one shape via its `workspace.md`; lives at Owner B scope.

**What it is**: The top-level deployment primitive — what gets bound when a practitioner deploys PBS for their work. A workspace is the central Owner B instance: its `workspace.md` selects shape + substrate + active specialists; its workspace-scope managed entities (practitioner-record, Actor, Client) live at Owner B; its layered content (references, doctypes, bausteine per Layer A) varies by domain/state context (configured via workspace's `scope.{domains, states}`).

**What it is NOT**:
- Not the `framework` — framework is the universal mechanism layer (what's POSSIBLE); workspace is one deployment instance built from framework + shape policies
- Not a `shape` — shape is the policy-bundle archetype (definition; lives in Framework C); workspace is an instance that SELECTS exactly one shape
- Not a `specialist` (canonical entry forthcoming) — specialist is composable expertise; workspace ACTIVATES specialists from the list in `workspace.md`
- Not a `session` (canonical entry forthcoming) — sessions are bounded interaction units WITHIN a workspace
- Not a single application running on a server — deployment-shape-agnostic (could be local, cloud, hybrid); not synonymous with "office" (prior naming, demoted session 13; workspace is broader)

**Cross-archetype illustration**:
- Planning bureau: "PBS-Schulz workspace"
- Legal practice: "Müller Law workspace"
- Research lab: "Smith Lab workspace"
- Solo creative: "Anna's Writing workspace"
- Knowledge graph: "BNatSchG knowledge workspace"
- Federation node: "Federation X workspace"

All workspaces are built from the same framework; they differ in selected shape (which configures policies), active specialists, and Layer A content per their domain/state scope.

**Boundary test**: ask "what's the deployment scope of this work?" The answer names a workspace.
- If answer is "a single feature" → it's a skill or specialist, not a workspace
- If answer is "the open-source product" → it's the framework, not a workspace
- If answer is "a configuration archetype" → it's a shape, not a workspace
- If answer is "a particular bounded interaction" → it's a session, not a workspace

**Composes with**:
- `shape` — workspace selects exactly one shape via `workspace.md` (the shape's policy bundle configures workspace's behavior over framework mechanisms)
- `framework` — workspace inherits framework's mechanisms; the selected shape's policies determine which are active/mandatory and what defaults apply
- `Owner B scope` — workspace lives as the central instance + container for workspace-scope managed entities (practitioner-record, Actor, Client)
- `specialist` — workspace activates a list of specialists per `specialists_active` field in `workspace.md` (canonical entry forthcoming)
- `practitioner` — workspace serves practitioner(s); records at Owner B (canonical entry forthcoming; dual-aspect: human cross-cutting, record at Owner B)
- `substrate` — workspace runs on exactly one substrate (selected via `workspace.md` `substrate` field)
- `session` — interaction units occur within a workspace (canonical entry forthcoming)
- `Layer A scope` — workspace's `scope.{domains, states}` configuration determines which Layer A content (references, doctypes, bausteine) applies

**Source**:
- VISION (`VISION.md`):
  - Line 7 (thesis): "A workspace pools and leverages codified expertise (bundled as specialists) to automate and support interactive practitioner workflows in a coherent manner"
  - Line 11: "any practitioner workspace shape (legal practice, research lab, creative studio, etc.)"
  - Multiple cross-archetype examples throughout
- `MAINTENANCE.md` "TOP-LEVEL ARCHITECTURE — Cross-cutting" classification (workspace listed as cross-cutting alongside practitioner, session, workflow)

**See**:
- `Owner B scope` (where workspace itself + workspace-scope managed entities live)
- `shape` (what workspace selects)
- `Layer A scope` (content scoping per workspace's domain/state configuration)
- ARCH Layer 3 workspace-detail topics (placeholder until Phase 3 — `workspace.md` schema; multi-practitioner workspace; legal-entity workspace context; deployment configurations)
