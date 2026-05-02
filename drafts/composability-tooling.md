# Composability tooling — DRAFT

> **STATUS: DRAFT — not locked, not final, candidate among many.** Exploratory capture of "what tooling enforces packaging-boundary discipline at L1-L4 producer levels + G composability gate." Surfaced session 16 (2026-05-02) during profiles + composability discipline work. Not load-bearing yet. Deferred to Phase 5+ ROADMAP per session-16 user direction.

## Origin

User direction during profiles work: composability + boundaries discipline must be "always in view" at every architectural decision. Tooling that helps enforce this discipline shouldn't be discussed now (don't sprawl scope) but should be captured for future engagement.

## The idea

The framework produces packageable artifacts at multiple levels (L1 specialist; L2 shape; L3 deployment template; L4 workspace instance). Each level has packaging-boundary concerns (per `profiles/G-composability-gate.md` — initial gate that fires first when designing producer-side artifacts):
- Marketplace distribution (future-conditional)
- Consulting deliverables
- Internal firm reuse
- OSS distribution
- Backup / migration / cloning

Without tooling, packaging discipline is enforced manually + visually. With tooling, packaging discipline becomes **structural** (per `feedback_wrong_shapes_impossible.md` discipline).

Candidate tools span L1-L4 producer-side validation + consumer-side workflows (G gate enforcement).

## Possible tools

### L1-side: Specialist tooling
- **Specialist self-containment validator** — checks specialist DEFINITION doesn't reference workspace-specific config; doesn't depend on practitioner-specific data
- **Specialist composition validator** — multiple specialists in workspace compose without conflicts; no naming collisions; no workflow definition collisions
- **Specialist packaging linter** — file structure + manifest + license metadata + provenance signing
- **Specialist version-bump tool** — semver discipline; breaking-change documentation; migration generator

### L2-side: Shape tooling
- **Shape definition validator** — policy bundle well-formed; mechanism configurations valid; cross-policy consistency
- **Shape variant composition validator** — DACH-planning extends planning-shape correctly; inheritance rules
- **Shape catalog discovery tool** — find shape variants matching deployment requirements

### L3-side: Deployment template tooling
- **Template composition validator** — specialist set + shape + Layer A compose cleanly; no version conflicts; no license conflicts
- **Template testing harness** — reference-deployment runs against template; smoke tests + scenario tests
- **Template versioning + migration tool** — template updates affecting existing deployments

### L4-side: Workspace tooling
- **Workspace serializer / deserializer** — export workspace state + entities + audit-trail to portable format; import to different substrate / clone
- **Workspace migration tool** — substrate-to-substrate migration; version-format upgrades
- **Audit-trail integrity verifier** — checks audit-trail completeness + tamper-evidence after migration / restore
- **Backup tool** — periodic workspace backup with versioning + restore points

### G consumer-side tooling (gate enforcement)
- **License + provenance verifier** — checks consumed artifact license compatibility + signing chain
- **Cross-substrate compatibility checker** — does this specialist work on substrate Y?
- **Cross-shape compatibility checker** — does this specialist activate fully in shape Z?
- **Specialist install + activation tool** — one-command install + activate + verify
- **Update notification + install tool** — track artifact updates; install with migration handling

## Architectural integration

Per `feedback_wrong_shapes_impossible.md` discipline: prefer tooling that makes wrong shapes IMPOSSIBLE over tooling that detects them after the fact:

- Specialist self-containment: best enforced via **structural constraint** at packaging time (specialist file structure prevents references to workspace-specific config)
- License verification: best enforced via **signed manifest** at install time (cryptographic verification; no install if signature invalid)
- Cross-shape compatibility: enforced via **shape policy** at activation time (shape policy declares specialist compatibility requirements; activation fails if incompatible)

Tooling that enforces structurally > tooling that lints after the fact.

## When this draft graduates

Per session-16 hybrid approach: this draft is captured now (while context is hot) but not developed. Graduates to ARCH topic OR ROADMAP feature commitment when:

- Phase 5 ROADMAP identifies composability tooling as ship-target
- First non-pioneer deployment surfaces packaging-boundary friction in practice
- Phase 6 specs work needs concrete tooling to enforce packaging contracts
- Community / external contributor pressure requires distribution tooling

Until graduation: stays as draft loose-thinking. Future-session reference for "what composability tooling could look like."

## Cross-references

- `profiles/G-composability-gate.md` (consumer-side concerns this tooling addresses; initial validation gate)
- `profiles/L1-specialist-creator.md` through `profiles/L4b-workspace-deployer-firm-it.md` (producer-side concerns)
- `profiles/INDEX.md` "Composability + multi-axis validation discipline" section
- `feedback_wrong_shapes_impossible.md` (structural-over-conventional discipline)
- `BACKLOG.md` Phase 5 entry: "Composability tooling — CLI / validators / linters that enforce packaging boundaries"
- `MAINTENANCE.md` cascade discipline (tooling decisions cascade through shape catalog + specialist authoring + deployment templates)
