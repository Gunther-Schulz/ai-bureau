# Archive index

v0.35 corpus from sessions 1-15 (2026-04-26 to 2026-05-01). Archived session 16 (2026-05-01) at start of foundational rebuild.

This corpus is **REFERENCE for the rebuild**, not active architecture. Each piece is "first experiment" — read selectively, lift what's right with citation, document divergence in new docs when shapes differ. Don't bind the rebuild to archive shapes; vocabulary lock comes first (Phase 2 of rebuild).

**NOT archived (anchors carrying forward into the rebuild)**:
- `VISION.md` — three-axis thesis (intertwining + sparring + authorship preservation); preliminary-lock anchor
- `memory/` — feedback files (lessons learned) + bausteine + universal prose (style-spec, korrektur-rules, verfahren docs); the actual user knowledge
- `.claude/`, `.gitignore`, `dev-link.sh` — operational / infrastructure (some may need archive later if they reference archived plugin/skills)

## Top-level documents

- **`ARCHITECTURE.md`** — v0.35 (3231 lines). 6 design disciplines + 3 operational principles + 4 meta-rules + reference card + three-category scope model + Option B floor + workspace shapes catalog.
- **`ROADMAP.md`** — 25 v1 commitments (#10 + #12 + #16 + #18 + #21 + #22 shipped) + v2 (AI-workspace generator) + v3 (specialist marketplace) horizons.
- **`HANDOFF.md`** — sessions 1-15 running handoff (1414 lines).

## docs/decisions/ (30 DRs, alphabetical)

- `a2a-and-gemini-pattern-emulation.md` — A2A schema compatibility per row; Tier 3 platform pattern (later reframed beyond Gemini-specific)
- `ai-as-runtime-hybrid-shape.md` — AI-as-runtime principle; structured for machine contracts; prose for semantics; three-layer frontmatter contract
- `audit-trail-v1.md` — SUPERSEDED by v2; dual-write architecture (later reversed to single-write)
- `audit-trail-v2.md` — Single-write architecture; AuditEvent schema; render-from-events; supersedes v1
- `backend-logging.md` — Backend logging conventions
- `backend-mcp-error-format.md` — MCP error envelope format; `_error` sentinel
- `backend-test-layout.md` — Backend test directory layout
- `closest-neighbors-deep-read.md` — Competitive landscape deep-read (Letta + OpenSail + PAI + Paperclip + commercial scan); 5/6 distinctness axes; ~10 adoption opportunities
- `counter-vision-engagement.md` — Substantive engagement with service-as-software opposing thesis; multi-disciplinary citations
- `entity-md-scope-model-restructure.md` — v0.34 three-category scope model (Layer A / Owner B / Framework C); Definition vs instance binding pattern
- `eval-framework-adoption.md` — Hybrid MS AF eval primitives + scenarios as entities
- `governance-and-identity-sourcing.md` — Identifier conventions; identity sourcing; convention versioning
- `greenfield-architecture-review.md` — Session 11 max-effort greenfield review; disqualifying criteria for substrate eval; sparring-mechanism structural/behavioral split reasoning
- `in-process-mcp-server.md` — TransportMode + MCPServerHandle + discovery API + governance
- `mcp-fallback-policy.md` — Fail-closed corollary; fallback bans; retry behavior
- `office-level-managed-entities.md` — Client + Actor as office-level entities; cross-department reference convention (terminology superseded session 13)
- `office-vs-department.md` — Office-vs-department modularization (terminology superseded session 13 to workspace-vs-specialist)
- `permission-abstraction.md` — Unified request_permission; 7 PermissionDecisionKinds; Permission/Quality gates
- `positioning-three-tier-framework.md` — Sub-DR B; three-tier framework (Infrastructure/Workspace/Specialist); ICP refinement; marketplace = of specialists
- `pre-action-framing-skill.md` — frame-task meta-skill; FramingOutput Pydantic schema; commitment #8
- `sdk-deep-read.md` — Claude Agent SDK + MS AF code-level deep-read; R3a-R3d findings
- `shape-extension-and-architectural-floor.md` — Shape-extension framework + Option B floor (3 axioms); contains contradiction with shape-neutrality claim (surfaced session 16)
- `skill-expert-agent-and-domain-knowledge.md` — Skill vs expert vs agent terminology; display_label; fine-grained expertise placement
- `sparring-output-v1.md` — ReviewOutput + RecommendationOutput Pydantic schemas; sparring mechanisms structural elevation
- `subagent-primitives-adoption.md` — Subagent case-by-case adoption + per-substrate extension Protocols pattern
- `substrate-agentic-framework.md` — #18 substrate eval; Claude Agent SDK + MS Agent Framework dual-substrate; Substrate Protocol pattern; Tier 3 reframing
- `substrate-protocol-design.md` — Common Substrate Protocol surface (Pydantic) + per-substrate extensions; boundary criteria
- `terminology-and-specialist-primitive.md` — Sub-DR A; Office→Workspace; Specialist NEW primitive; Department demoted to optional groupings
- `trigger-convention.md` — Concept labels for skill triggers; convention-direction discriminator
- `vision-realignment-session14.md` — VISION axis refinements + R1-R8 sharpening; Option B architectural inheritance lock

## docs/conventions/

- `entity-md-spec.md` — Entity-md spec; Layer 1/2/3 frontmatter; cross-ref syntax; body conventions per type; three-category scope model implementation

## docs/audits/ + docs/design-reviews/ (first runs)

- `audits/boundary-adherence-20260429.md` — Slice 14 first run
- `audits/invalidation-contract-20260429.md` — Slice 15 first run
- `audits/validation-gate-20260429.md` — Slice 16 first run
- `design-reviews/foundations-20260429.md` — Foundations design review
- `design-reviews/vision-arch-coupling-20260429.md` — Target 8 first run

## Other docs/

- `strategic-positioning.md` — DACH/EU positioning; competitive landscape; funding path (consulting + grants + Cherry); ICP refinement
- `validation-gating-overview.md` — Five-layer validation systems-view (L1 runtime structural / L2 runtime conventional / L3 retrospective scan / L4 prospective design / L5 external boundary)
- `plugin-conventions.md` — Plugin authoring conventions; §11 (triggers) + §11b (fallback policy)
- `backend-conventions.md` — Backend code conventions
- `rag-pipeline-decisions.md` — RAG architecture decisions (Phase 0/1/2/3/4 phasing)
- `what-this-is.md` — Outsider-shareable framing (session 11)
- `audit-pre-rag.md` — Pre-RAG architecture audit
- `office-config.schema.yaml` — Office config YAML schema (terminology + structure superseded by v0.34 restructure)

## extensions/framework/ (session 15 prototype)

Framework primitive entity-md instances built against v0.34 schema BEFORE foundational vocabulary lock. Useful as concrete-shape reference; rebuild may produce different schemas.

- `shapes/practitioner/shape.md` — practitioner workspace shape; PBS pioneer reference
- `substrates/claude-agent-sdk/substrate.md` — Claude Agent SDK substrate
- `substrates/ms-agent-framework/substrate.md` — MS Agent Framework substrate
- `protocols/event-coordination/protocol.md`
- `protocols/always-on-sparring/protocol.md`
- `protocols/claim-level-audit/protocol.md`
- `protocols/practitioner-judgment-trust/protocol.md`
- `protocols/turn-based-time/protocol.md`
- `specialists/planning-document-work/specialist.md` — domain-anchored specialist DEFINITION; bundles 15 PBS skills

## backend/ (working code, archived to remove rebuild bias)

MCP server implementation embodying v0.35 architectural decisions. Pre-launch; no production data; no migration cost. Phase 6 rebuilds against locked architecture.

- `mcp-server/` — Python package: Pydantic schemas (ProjectState with `departments_active`, AuditEvent with session-13 schema, sparring-output v1 + RecommendationOutput, manifest models), MCP tool implementations, integration adapter scaffolding, audit-trail v2 single-write, logging conventions, test layout
- `README.md` — backend-specific README

## plugin/ (working skills, archived to remove rebuild bias)

19 skill bundles authored against v0.35 vocabulary (`department:` frontmatter pre-rename to `specialist:` per session-13 sweep that was deferred to #11 single-touch refactor; old slash-command namespacing).

- `CLAUDE.md` — plugin-level meta-rule 4 summary
- `skills/` — orchestrator, save-baustein, record-feedback, draft-textteil-b, draft-textteil-c, review-draft, validate-checklist, validate-bausteine, validate-latex-style, verify-citations, research-references, draft-cover-mail, survey-project, promote-to-skill, watch-list, audit, design-review, author-manifest, setup-office (19 total)
- `templates/` — workspace-style overlays + skeletons (universal + per-domain)

## .claude-plugin/ (plugin manifest, co-archived with plugin/)

- `plugin.json` — Anthropic plugin manifest pointing at `plugin/skills/`; archived alongside plugin to keep coherent

## extensions/{universal,domain,state}/ (PBS-Schulz content, archived to remove rebuild bias on scope structure)

User's accumulated content. Archived because the *shape* it lives in (Layer A scope orthogonality + jurisdiction-keying + manifest YAML structure) embodies architectural decisions about scope model + hybrid-shape adoption that the rebuild may reshape. Content is genuine user knowledge that carries forward; lifted into new shape during Phase 6.

- `extensions/universal/doctypes.yaml` — universal doctypes manifest (B-Plan-Begründung, Stellungnahme, etc.)
- `extensions/universal/references-manifest.yaml` — universal legal references manifest (BauGB, BNatSchG, BauNVO, UVPG, ROG)
- `extensions/domain/{Innenentwicklung,Naturschutz,PV-FFA,Wind}/` — domain-keyed content per planning domain
- `extensions/state/{BB,BE,BW,BY,HB,HE,HH,MV,NI,NW,RP,SH,SL,SN,ST,TH}/` — Bundesland-keyed content (16 German states)
- `extensions/README.md` — extensions structure README

## README.md (top-level, archived to remove rebuild bias)

Top-level project README likely describes v0.35 architecture (workspace/specialist/skill primitives, three-axis VISION explanation, plugin install instructions referring to archived plugin). Kept content available for reference; new README produced after rebuild lands.

## How to use this archive during rebuild

1. **Identify** which archive pieces touch the topic the rebuild is addressing
2. **Read** them directly — don't pattern-match from this index or from prior summaries (the failure mode that motivated the rebuild)
3. **Lift** what's correct with citation in the new doc
4. **Document** divergence in the new doc when the rebuild reaches different conclusions; cite the archived shape and explain why we go differently
5. **Don't bind** the rebuild to archive shapes — Phase 2 vocabulary lock comes first; archive is consulted in Phase 3+ as evidence-of-prior-experiment

## Status note (known issues this corpus contains)

Surfaced during session 16 rebuild-launch clarifications:

1. **Foundational vocabulary not crisply defined** — "framework" / "shape" / "mechanism" / "policy" / "practitioner" used heavily but not glossary-grade defined; "Protocol" has dual-use (Pydantic Protocol vs architectural pluggable subsystem like Sparring Protocol) without disambiguation
2. **Shape-neutrality + Option B floor contradiction** — `shape-extension-and-architectural-floor.md` line 117 claims shape-neutrality while same DR establishes a floor enforcing practitioner-shape values across all shapes
3. **VISION-scope vs framework-scope contradiction** — VISION self-scoped to practitioner-shape (post session 14), but Option B floor enforces axis 3 (a practitioner-shape value claim) on all shapes
4. **Instance-anchoring leakage** — multiple primitives reflect PBS-instance / EU-jurisdiction / solo-human-author shape rather than pattern-level: `project` enum value in Owner B; `groupings` primitive (department-shape vestige); practitioner = solo-human-only; "anti-Art-25-trap" naming at floor; `ai_act_article_mapping` field at substrate level; 6-month retention as substrate default
5. **"Mechanism vs policy" vocabulary** absent from corpus — used loosely in session-16 conversation but never established in any DR
6. **Filesystem location drift** — shape-extension DR references `extensions/shapes/<id>/` (its original framing); v0.34 entity-md restructure moves Framework C definitions to `extensions/framework/shapes/<id>/`; not reconciled in shape-extension DR

The rebuild addresses these at root by locking vocabulary first (Phase 2) then rebuilding ARCH + DRs + ROADMAP against the locked vocabulary (Phase 3+).
