# D20 — 2026-05-08 — Work-unit kind

**Decision**: The work-unit kind specifies a unit of organized work tracked in workspace state per D7. Work-unit is an *instance* concept (specific work being / having been done), distinct from specialist (capability template). One kind covers all work-unit instances; the variation lives in `kind` (work-unit-kind discriminator, extension-registered like event payload-subtypes).

### Contract slots

- **`id`** — unique within workspace.
- **`kind`** — work-unit-kind identifier (extension-registered; open vocabulary; per the layer-3 extension protocol). Examples: `b-plan-section`, `invoicing-cycle`, `correspondence-thread`.
- **`status`** — lifecycle phase. Fixed core enum (see below).
- **`payload`** — kind-specific content (validated by the work-unit-kind extension declaration; framework doesn't validate payload shape at core).
- **`contributing-actors[]`** — required-with-explicit-empty: actors operating on this work-unit, with role-tags per D9 + D13.
- **`contributing-specialists[]`** — required-with-explicit-empty: specialists operating on this work-unit (each must have this work-unit's `kind` in its `supported-work-unit-kinds`).
- **`lifecycle`** — timestamp markers: `created-at`, `started-at`, `completed-at`. Richer lifecycle history derivable from events filtered by this work-unit's id.

### Core lifecycle status enum (fixed at framework-core)

- **`created`** — work-unit declared; not yet started.
- **`in-progress`** — actively being worked on.
- **`paused`** — work suspended; can resume.
- **`completed`** — work finished successfully.
- **`abandoned`** — work terminated without completion.

Five states. Fixed at core; extensions cannot add lifecycle states. Specific shape / specialist concerns (review flows, attestation, approval gates) are modeled as **events** within `in-progress`, not as separate states. Forces consistent lifecycle vocabulary across work-unit-kinds + makes status transitions structurally predictable.

### Work-unit-id and event chain

Per D10, the workspace has a single ordered event chain. Work-unit-events are a **derived view** by filtering events that reference the work-unit's id. This requires events to carry a work-unit-id reference where applicable.

**Refinement-pass finding for D10**: events should have a `work-unit-id` slot (optional; null when event is not associated with any work-unit; non-null otherwise). This makes per-work-unit views queryable without payload-rummaging. Queued for the named refinement pass per D14.

### Concrete example (illustrative; not part of core)

`wu-b-plan-3.2-hennigsdorf-2024` of kind `b-plan-section`, status `in-progress`, payload `{section-number: "3.2", project-id: "hennigsdorf-2024"}`, contributing-actors `[claude-primary as drafter, gunther-schulz as practitioner]`, contributing-specialists `[planning-document-work]`. Worked through in discussion that produced this decision.

### What is NOT in the work-unit kind contract

- **Work-unit-kind payload schemas** — extension-declared per kind (the `b-plan-section` extension declares what `payload` shape its instances have).
- **Lifecycle transition rules** (when can `in-progress` → `completed`?) — shape / specialist concern; framework checks allowed transitions but not the conditions for them.
- **Containment hierarchy** (work-units containing sub-work-units) — out of scope for now; would need its own decision if surfaced.
- **Work-unit-state mutation semantics** (atomic vs eventual) — implementation.
- **Cross-workspace work-unit federation** — out of scope.

**Rationale**: per I1, work-unit is the instance-shaped composable concept that the workspace tracks (paralleling specialist as the template-shaped composable concept); per I2, fixed core lifecycle states + structural slots give framework a basis to validate work-unit transitions and references; per I3, work-unit's events (via the work-unit-id slot on events, refinement pending) form the attribution-bearing record of how work proceeded.
