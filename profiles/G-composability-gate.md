# Profile G: Composability Gate — package consumer perspective

**Status: PRELIMINARY — full detail (cross-cutting validation gate)**

**Role**: G (initial gate; fires FIRST before producer-side design at L1-L4)
**Shape variation**: n/a (gate validates artifacts produced across multiple shapes)
**Archetype**: n/a (multi-mode consumption: consulting / internal-firm-reuse / OSS / marketplace / backup-migration)
**Scale**: varies (individual consultant; firm IT; OSS contributor; future marketplace)

**Why "Gate" not "L13"**: this profile is NOT a sequential lifecycle stage (L1-L9 cover those). It's a CROSS-CUTTING VALIDATION GATE that fires FIRST when designing any L1-L4 producer artifact. Lifecycle order: L1-L4 produce → consumers consume (downstream). Validation order: G fires first — does the design support consumer-side multi-mode consumption? If G fails, reshape. If G passes, proceed to multi-axis validation across L1-L9 producer profiles.

## Identity + context

This profile captures the **consumption side** of packaged framework artifacts produced at L1 (specialist), L2 (shape), L3 (deployment template), and L4 (workspace instance). Multiple consumption modes share architectural concerns:

| Consumption mode | Who consumes | What gets consumed |
|---|---|---|
| **Consulting service deliverable** | Consultant builds + delivers to client | Specialist (most common); shape (medium); deployment template (large engagement) |
| **Internal firm reuse** | Firm IT distributes to multiple practitioners within firm | Specialist; shape variants per office; workspace templates |
| **OSS / community distribution** | OSS contributor publishes; community downloads | Specialist (e.g., domain-specific specialists); shape extensions |
| **Marketplace** (FUTURE-CONDITIONAL) | Specialist seller distributes; specialist buyer integrates | Specialist (primary marketplace artifact); potentially shape; potentially template |
| **Backup / migration / cloning** | Practitioner migrates workspace; firm clones template; admin backs up | Workspace instance (state + content); deployment template |

This profile activates partially today (consulting + internal-firm-reuse + OSS + backup are real now) and fully later (marketplace if/when it materializes). Future-conditional marker: marketplace mode is speculative; profile validates that current framework decisions don't preclude marketplace support without committing to building marketplace.

## Day-in-the-life / usage flow

### Consulting deliverable mode

Consultant Sarah builds a specialist for client (financial-advisory firm) — captures firm's compliance workflows + bausteine + audit-emission patterns. Process:
- Sarah develops specialist locally (her own development workspace)
- Tests specialist against firm's representative work-units
- Packages specialist (file structure + dependencies + metadata)
- Delivers via signed handoff (firm imports specialist into their workspace template; activates per practitioner)
- Provides update path (Sarah issues v1.1 → firm updates)
- Contractual: Sarah's IP; firm licenses use; cannot re-distribute

Architectural concerns:
- Specialist self-containment (no leakage to Sarah's dev workspace)
- Versioning + migration semantics (firm's existing workflow_instances on v1.0 — what happens at v1.1 update?)
- License / IP boundary clear in metadata
- Audit trail of specialist version-bumps + per-deployment install timestamps

### Internal firm reuse mode

Mid-size legal firm has 50 practitioners across 5 offices. Firm-internal IT distributes shared specialist set:
- Senior partner authors specialist (tax-litigation specialist)
- IT packages + tests against representative practitioners
- IT deploys to all 50 practitioners' workspace templates
- Per-office customization: NYC office adds NY-specific Layer A content; LA office adds CA-specific
- Updates flow firm-IT-controlled (not per-practitioner adoption)
- Multi-tenant governance: who can modify? Senior partner only; junior practitioners use as-distributed

Architectural concerns:
- Specialist + per-office shape variations compose cleanly (shape catalog curator concern: L9)
- Update governance (who authorizes specialist version-bump for entire firm?)
- Multi-practitioner licensing (firm license vs per-practitioner)
- Audit trail across all 50 deployments

### OSS / community distribution mode

Domain expert publishes open-source specialist (immigration-law specialist) on community ecosystem. Process:
- Author packages specialist with documentation + license (e.g., Apache 2.0)
- Publishes to OSS distribution (git repo; possibly future framework registry)
- Adopters discover; download; install; activate; provide feedback
- Contributors fork; extend; PR upstream
- Versioning per semver; breaking changes documented

Architectural concerns:
- License compatibility (OSS license at specialist level + framework license at substrate level)
- Specialist-to-specialist composition (immigration-law + general-legal-practice base specialist; do they compose cleanly?)
- Provenance + signing (does the specialist do what its README claims? trust mechanism?)
- Cross-jurisdictional applicability metadata (this specialist applies to US immigration; not directly applicable to DE/EU)

### Marketplace mode (FUTURE-CONDITIONAL)

If specialist marketplace materializes (Phase 5/6+):
- Specialist seller publishes paid specialist
- Specialist buyer purchases + downloads + activates
- Revenue tracking + payouts
- Quality / review / rating system
- Version governance + update notifications
- License + IP boundary enforced contractually

Architectural concerns (forward-validation now):
- Specialist signing / provenance (anti-spoofing)
- Revenue tracking (per-install events; per-use events?)
- Specialist versioning + migration governance
- Marketplace-specific metadata (price; ratings; license tier)
- Refund / dispute mechanics

Profile activates fully if marketplace builds; meanwhile validates current framework decisions don't preclude marketplace support.

### Backup / migration / cloning mode

Practitioner-A migrates from substrate-X to substrate-Y. Or firm clones template from one deployment to another. Or admin backs up workspace state for disaster recovery.

Architectural concerns:
- Workspace serialization: what's captured? state + entities + audit-trail + memory + workspace.md
- Substrate-portability: workspace state separable from substrate-specific runtime state
- Cross-deployment migration: workspace from substrate-X imports to substrate-Y
- Versioning of workspace format (state evolution over time; backward compat)
- Audit-trail integrity through migration

## Hybrid moments

**Multi-mode at once**: Same artifact (specialist) gets distributed across multiple modes simultaneously:
- Sarah builds specialist for consulting client (mode 1)
- Sarah ALSO publishes redacted version on OSS (mode 3)
- Eventually firm-internal-reuse: client's firm distributes within itself (mode 2)
- Future: same specialist could go on marketplace (mode 4 if materializes)

Architectural design must support overlap: specialist is the same architectural artifact; consumption mode varies.

**Mode evolution over time**:
- Specialist starts as private dev → consulting deliverable → eventually OSS → eventually marketplace
- Framework decisions made for "private dev" must not preclude later modes

**Composition across consumed artifacts**:
- Workspace consumes deployment template (L3) + multiple specialists (L1) + shape (L2) + Layer A content (cross-cutting)
- Each comes from possibly-different consumption channels (OSS specialist + consulting-delivered shape + internal template)
- Composition compatibility matters: specialist X from OSS works with shape Y from consulting?

## Capability composition

n/a — this profile is about CONSUMING capabilities packaged at L1-L4, not configuring them. Consumption capabilities provided by framework infrastructure: install / activate / update / migrate / backup mechanisms.

Future tooling (per drafts/composability-tooling.md) provides operational capabilities aligned with G's gate function:
- Specialist installer / validator
- Shape installer + variant resolution
- Template composition validator
- Workspace export / import / migrate
- Audit-trail integrity verifier across migration

## Multi-user moments

G is inherently multi-actor:
- Producer (L1-L4 author) ↔ Consumer (validated via G)
- Distribution intermediary (consulting firm; OSS maintainer; firm IT; future marketplace)
- Per-mode governance (consulting contract; firm policy; OSS license; marketplace TOS)

Multi-user concerns are PER-MODE not PER-WORKSPACE:
- Mode 2 (firm reuse): firm IT governs distribution across 50 practitioners
- Mode 3 (OSS): community governance via OSS norms (PRs, code of conduct, license enforcement)
- Mode 4 (marketplace): platform governance (TOS, dispute resolution)

## Edge cases

**License conflict**: OSS specialist (Apache 2.0) used inside firm's proprietary deployment template. Acceptable per Apache 2.0; but template's downstream consumers must respect Apache attribution. License composition rules — explicit metadata required.

**Versioning conflict**: workspace running specialist v1.0; specialist updated to v2.0 with breaking changes. Workspace's running workflow_instances snapshot to v1.0 definition (per workflow primitive's versioning semantics); future workflow_instances can use v2.0. Migration is explicit.

**Provenance gap**: who built this specialist? OSS specialist with anonymous contributor; can workspace TRUST it for accountability-bearing work? Provenance metadata + signing required.

**Cross-substrate consumption**: workspace deployed on Claude Agent SDK; specialist from consultant built against MS Agent Framework. Specialist must be substrate-agnostic OR explicitly substrate-pinned; consumer must verify before install.

**Cross-shape consumption**: practitioner-shape specialist (mandates audit-emission) used in personal-OS-shape workspace (light audit). Shape's policy bundle determines if specialist activates fully or partially. Shape composition rules.

**Backup-restore-migration round-trip**: workspace backed up; restored to different substrate; some events lose substrate-specific metadata. Audit-trail integrity check fires. Acceptable for disaster recovery; not acceptable for routine migration.

## What this profile EXEMPLIFIES

This profile stress-tests:
- **Composability + boundary discipline** at L1-L4 (specialist / shape / template / workspace artifacts must package cleanly for multi-mode consumption)
- **Framework decisions don't preclude future consumption modes** (especially marketplace forward-compatibility)
- **License + IP + provenance metadata** as architectural concerns at packaging time
- **Versioning + migration semantics** (specialist updates; workspace serialization format evolution)
- **Substrate-portability + substrate-pinned variation** (some artifacts substrate-agnostic; some explicitly pinned)
- **Shape-portability + shape-pinned variation** (some artifacts shape-agnostic; some shape-specific)
- **Cross-mode artifact lifecycle** (private dev → consulting → OSS → marketplace as evolution path)
- **Distribution intermediary governance** (consulting contract; firm IT; OSS license; marketplace TOS — different governance models compose with framework artifacts)
- **Trust + signing + verification** (especially for OSS + marketplace; consulting + firm-internal less so)

## Architectural concerns this profile surfaces

- Specialist self-containment is non-negotiable (every L1 packaging concern; no leakage to author's dev workspace)
- Workspace serialization format must be architectural commitment (Phase 6 spec; backward-compat discipline)
- Versioning semantics for specialists / shapes / templates (semver-like; breaking-change documentation)
- License metadata at every packaged artifact level (specialist license; shape license; template license; workspace license)
- Provenance + signing mechanism (Phase 5/6+ for marketplace; lighter for OSS)
- Cross-shape composition rules (when specialist from one shape activates in workspace of different shape)
- Cross-substrate composition rules (when artifact built against substrate-X used on substrate-Y)
- Migration / backup / restore mechanics with audit-trail integrity (Phase 6+ tooling)

## Composability tooling (per drafts/composability-tooling.md)

This profile maps directly to tooling needs:
- Specialist validator (self-containment check)
- Shape composition validator (multi-shape compatibility check)
- Template composition validator (specialist + shape + Layer A composability)
- Workspace serializer + deserializer (with audit-trail integrity)
- License + provenance metadata schema + verifier
- Versioning + migration tools (specialist version-bump; shape variant resolution; workspace format migration)

Tooling deferred to Phase 5+ ROADMAP per session-16 user direction. This profile validates current architectural decisions support future tooling without precluding it.

## Status

**PRELIMINARY** — full detail for cross-cutting profile. Multiple consumption modes; some active today (consulting + firm-reuse + OSS + backup), one future-conditional (marketplace). Profile evolves as actual consumption events surface integration friction.
