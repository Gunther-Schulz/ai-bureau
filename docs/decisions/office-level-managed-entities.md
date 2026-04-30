# Decision record: Office-level managed entities — Client + Actor as new entity tier (commitment #15)

> ## ⚠ NAMING SUPERSEDED session 13 per #22 (`docs/decisions/terminology-and-specialist-primitive.md`)
>
> "Office-level managed entities" → **"Workspace-scope managed entities"**.
> Structural decisions (Client + Actor as cross-cutting entity tier;
> cross-department reference convention `<entity>_id: str`; native + adapter
> delivery modes) **REMAIN VALID** with renamed primitives:
>
> | Old (this DR) | New (Sub-DR A) |
> |---|---|
> | Office-level managed entities | Workspace-scope managed entities |
> | `OfficeEntity.managed_entities` | `WorkspaceEntity.workspace_scope_entities` |
> | `extensions/office/entities/...` | `extensions/workspace/entities/...` |
> | Cross-department references | Cross-specialist references |
> | Department-level entities | Specialist-level entities |
>
> File rename to `workspace-scope-managed-entities.md` deferred (cross-refs
> across multiple files). Use **`terminology-and-specialist-primitive.md`**
> (Sub-DR A) for current primitive vocabulary.

**Status**: ACCEPTED (session 11, 2026-04-30; backfill DR for ROADMAP commitment #15 originally scoped session-9 followup #2); **NAMING SUPERSEDED session 13 per #22 Sub-DR A**
**Owner**: ROADMAP commitment #15; ARCHITECTURE.md entity-elevation discipline; entity-md-spec (Layer 2 schemas)
**Related**: `office-vs-department.md` (#12 — supersedes naming session 13); `governance-and-identity-sourcing.md` (decision 5 — same registration shape workspace + specialist; decisions 1-3 — Actor as identity primitive); `ai-as-runtime-hybrid-shape.md` (#16 — entity-md hybrid-shape contract); `audit-trail-v2.md` (#6 — `actor_kind` references Actor.id); `terminology-and-specialist-primitive.md` (Sub-DR A — supersedes naming)

## Context

Per `office-vs-department.md` (#12, session 9), the office abstraction contains 0..N departments. Each department contributes its own managed entities (Project for planning, Invoice for invoicing, etc.). Cross-department coordination is event-shaped per #10's transport-portability constraint.

But some entities are **shared across departments** — referenced by planning + invoicing + PM, etc. The shared entities are:

| Entity | Used by departments | Why office-level |
|---|---|---|
| **Client** | planning (project's client), invoicing (billing target), PM (engagement subject), legal (matter's client) | A client isn't owned by one department — it's an office-level relationship referenced by all |
| **Actor** | every department (audit attribution, governance, role enforcement, sparring partner identity) | An actor isn't a department member — they're an office member; multiple departments include them |

Today these are scattered:
- Actor lives in `office-config.actors[]` (semi-typed config) per session-7 setup
- Client doesn't exist yet — referenced informally in project state (`client: <string>`)

Session-9 followup #2 introduced the **office-level managed entities concept** — entities that are office-owned (not department-owned) but cross-referenced by departments. Per governance-and-identity-sourcing decision 5, office-level + department-level entities follow the SAME registration shape (per Bundle A close-out).

This DR consolidates the architectural design that's been scattered across:
- ROADMAP commitment #15 entry (high-level)
- `office-vs-department.md` "office-level managed entities" subsection (concept introduction)
- `governance-and-identity-sourcing.md` decision 1 (Actor.roles primitive for governance) + decision 2 (identity sourcing native vs adapter) + decision 3 (identifier conventions) + decision 5 (same registration shape)
- `ai-as-runtime-hybrid-shape.md` (entity-md schemas for Client + Actor)

into a focused decision record specifically for the **Client + Actor entity tier**.

## Decisions

### 1. Two office-level managed entities — Client and Actor

**Decision**: Client + Actor are first-class office-level managed entities with their own Layer 2 Pydantic schemas + entity-md instances.

#### Client entity

**Layer 2 schema** (extends `EntityBase`):

```python
class ClientEntity(EntityBase):
    legal_name: str                              # Full legal entity name
    primary_contact: str                         # Actor.id reference
    address: Address                             # Structured address
    billing_contact: str | None = None           # Actor.id (defaults to primary_contact)
    default_payment_terms: int = 30              # days net
    default_currency: str = "EUR"                # ISO 4217
    mode: Literal["native", "adapter"] = "native"
    adapter: str | None = None                   # adapter id when mode=adapter
    # ...
```

Per #16 hybrid-shape: structured fields above + body sections for free-form prose:
- `## Communication preferences` (PDF email vs portal, formal vs informal, German vs English)
- `## Billing conventions` (deviations from default_payment_terms; volume discounts; retainer structure)
- `## Project history summary` (high-level relationship narrative)
- `## Watch-outs` (prior issues; sensitivities; escalation contacts)

**Storage**: `extensions/office/clients/<client-id>.md`. ID convention per office (per governance-and-identity-sourcing decision 3) — typically firstname-lastname for individuals, slug-of-legal-name for companies.

#### Actor entity

**Layer 2 schema** (extends `EntityBase`):

```python
class ActorEntity(EntityBase):
    kind: Literal["internal", "external", "system"]
    roles: list[str] = []                        # Per governance decision 1 — role primitive
    email: str | None = None
    departments: list[str] = []                  # For internal actors — which departments they work in
    mode: Literal["native", "adapter"] = "native"
    adapter: str | None = None                   # adapter id when adapter mode
    # ...
```

Body sections per #16:
- `## Role + responsibilities` (free-form description)
- `## Working preferences` (sparring style, language, tone)
- `## Capabilities + limits` (what they're authorized to do; expertise areas)

**Storage**: `extensions/office/actors/<actor-id>.md`. ID convention per office (per governance-and-identity-sourcing decision 3).

### 2. Office-level entity registration

**Decision**: per Bundle A close-out + governance-and-identity-sourcing decision 5, office-level entities are registered in `extensions/office/office.md` (the office-level registration file, parallel to `department.md`). Same `managed_entities` shape:

```yaml
# extensions/office/office.md frontmatter (Layer 2)
managed_entities:
  client:
    pydantic_class: extensions.office.entities.client.ClientEntity
    instances_at: "extensions/office/clients/{id}.md"
    # native default; mode comes from per-instance frontmatter

  actor:
    pydantic_class: extensions.office.entities.actor.ActorEntity
    instances_at: "extensions/office/actors/{id}.md"
    # adapter mode supported per-instance — see governance-and-identity-sourcing decisions 2-3
```

The registration uses SHORT form (`client`, `actor`) as map keys; gate composes full namespaced types as `office.client` + `office.actor` per entity-md-spec §3.2.

### 3. Cross-department reference convention

**Decision**: cross-department references to office-level entities use `<entity>_id: str` Layer 2 fields on the referencing entity. Gate validates references exist at write-time; no FK enforcement at storage layer.

**Examples**:

```python
class ProjectEntity(EntityBase):              # type: planning.project
    client_id: str                             # references office.client
    primary_actor_id: str                      # references office.actor (project lead)
    # ...

class InvoiceEntity(EntityBase):               # type: invoicing.invoice
    client_id: str                             # references office.client
    issued_by_actor_id: str                    # references office.actor
    # ...

class TimesheetEntity(EntityBase):             # type: pm.timesheet
    actor_id: str                              # references office.actor
    project_id: str                            # references planning.project
    client_id: str                             # references office.client (denormalized for query convenience)
    # ...
```

**Validation at gate**: when `write_entity` is called, gate validates `<entity>_id` fields point to existing entities (read the referenced file; verify type matches the reference's expected type). Read-time validation flags but doesn't fail (allows reading projects that reference deleted clients — surfaces dangling-reference, doesn't break the read).

**Why string IDs not Pydantic relations**: hybrid-shape (#16) — entity references are stable string IDs, not in-memory Pydantic graphs. Per `closer to knowledge graph + document store` framing.

### 4. Adapter mode for office-level entities

**Decision**: both Client and Actor support `mode: native | adapter` per managed-entity concept (per `office-vs-department.md`). Per-deployment choice.

**Native**: PBS owns the entity data. Schema fields validated at gate; instance md files at `extensions/office/clients/<id>.md` + `extensions/office/actors/<id>.md`.

**Adapter**: external system owns the entity data. PBS reads via adapter (Pydantic Protocol per #9 Bundle E):

- **Client adapter examples**: Lexware (uses Lexware's customer records); Salesforce (Salesforce accounts); HubSpot (HubSpot contacts).
- **Actor adapter examples**: Personio / BambooHR (HR system as identity source); Microsoft Entra (corporate directory); Coolify SSO (OAuth identity).

When adapter mode, the entity-md file contains:
- Frontmatter Layer 1 + Layer 2 with `mode: adapter` + `adapter: <id>` + `adapter_config_ref: <office-config path>`
- Body: free-form prose about how this office uses the external system (per #16 worked example 3)

### 5. Identifier uniqueness convention

**Decision**: per governance-and-identity-sourcing decision 3, identifier uniqueness is per-deployment + documented in `extensions/office/conventions/<entity>-conventions.md`. Common strategies:

| Entity | Common strategies |
|---|---|
| **Client** | Slug of legal name (`maxsolar`, `solarfaktor`); hierarchical for subsidiaries (`maxsolar-de`, `maxsolar-pl`); UUID-based when external system dictates |
| **Actor** | Firstname-lastname for individuals (`gunther-schulz`, `hendrik-meyer`); HR-system internal ID for adapter mode (`actor-12345`); email-prefix derived (`alice-mueller-schulz-de`) |

The deployment chooses + documents the convention; AI applies at mint time per governance-and-identity-sourcing decision 4 (prose-rules pattern).

### 6. Body conventions per office-level entity

**Recommended sections** per type, in entity-md-spec §6 catalog format:

#### `office.client`

```markdown
## Communication preferences
## Billing conventions
## Project history summary
## Watch-outs
```

#### `office.actor`

```markdown
## Role + responsibilities
## Working preferences
## Capabilities + limits
```

Audit slice 21 + design-review target 12 verify presence + non-emptiness; gate doesn't reject body for missing sections (per #16 recommended-not-enforced pattern).

## Composition with existing disciplines

| Discipline | Connection |
|---|---|
| **Entity-elevation 3-test (v0.13)** | Both Client + Actor pass: stable identity (legal entity, person), state of record (mode/adapter, roles, contact), lifecycle (active/archived/etc.). 3-test confirms elevation warranted. |
| **Office-vs-department (#12)** | Office-level entities are the natural shape for cross-department references. Per #12 entity-elevation, projects + invoices + timesheets are department-level (department-owned); clients + actors are office-level (office-owned, department-shared). |
| **AI-as-runtime hybrid-shape (#16)** | Both entities follow the three-layer frontmatter contract (Layer 1 universal + Layer 2 type-specific + Layer 3 deferred to #9). Body is free-form prose. AI composes per-context behavior at runtime from frontmatter + body + cross-refs. |
| **Make wrong shapes impossible (v0.21)** | Cross-department references via typed `<entity>_id: str` fields with gate-validation are STRUCTURAL. The convention "skill A reads skill B's file at known location" anti-pattern (per failure-mode catalog implicit-contract-between-skills entry) is replaced with the gate-mediated reference validation. |
| **Glue-not-replacement (v0.15)** | Adapter mode is the explicit application — Client adapter lets Salesforce stay the source-of-truth for client data; Actor adapter lets Personio stay the source-of-truth for HR data. PBS coordinates without replacing. |
| **Sharp defer rule (v0.20)** | Per session-11 sharp-defer audit, this commitment lands at first-bind framework infrastructure (consulting clients deploying with multi-department offices need Client + Actor at first bind). Not deferred per "PBS only has Gunther + Hendrik today" framing. |

## Defers (per defer-instinct discipline)

| Defer | Home | Specific cost being avoided |
|---|---|---|
| **D1**: Concrete adapter Protocol shape (subscribe vs poll vs both) | #9 Bundle E (restored from #11 deferral per session-11 sharp-defer audit) | Designing Protocol without first concrete adapter implementation context; #9 Bundle E produces Protocol; #15 + #11 + #13 implement against it |
| **D2**: Specific adapter implementations (Lexware, Salesforce, Personio, etc.) | Per-deployment + #11 (Cowork integration's invoicing/PM scaffolding) for first concrete adapter | Each adapter has its own integration cost + scope; bundling with #15 would balloon scope |
| **D3**: Layer 3 per-deployment customization fields for Client/Actor | #9 Bundle B (Layer 3 mechanism decision pending) | Pre-empting Bundle B's Layer 3 mechanism choice |
| **D4**: Schema-version migrations when Client/Actor schemas evolve | Bundled with #9's schema migration framework | Migration framework lands once for all entity types |

Each defer names a specific home + chronological-valid cost being avoided.

## Constraints flowing to downstream commitments

### → #6 (audit-trail v2 retrofit)

- **`AuditEvent.actor`** field references `Actor.id` (office-level managed entity). Replaces today's free-form actor string. `actor_kind` distinguishes how actor relates to event (human / skill / external_agent per #10).
- **Approval events** (`approval_requested`, `approval_granted`, `approval_rejected`): `details.approving_actor` references `Actor.id`. Per governance-and-identity-sourcing decision 1, role enforcement uses `Actor.roles` at gate.
- **`record_decision` flows**: every decision event captures `actor` reference to the responsible Actor.

### → #11 (Cowork integration)

- **First concrete adapter implementations** when invoicing/PM scaffolding ships:
  - Lexware adapter for Invoice entity (department-level, but uses Client cross-ref).
  - Possibly Personio adapter for Actor entity (depends on bureau).
- **Slash command UX**: `/setup-actor`, `/setup-client` for explicit invocation when conversational context isn't natural.

### → #13 (deployment flexibility)

- **Multi-user auth**: per governance-and-identity-sourcing decision 1, Actor.roles is the role primitive for gate-level enforcement. Multi-user readiness requires Actor entity available + populated.
- **Tier 2 cloud deployment**: Actor entity adapter mode (Personio / BambooHR / etc.) is common at small-company scale.

### → #14 (Memory Bank)

- **`search_memory`** can filter by actor (`who saved this baustein?`) + by client (`bausteine related to this client's projects`). LanceDB memory index includes actor + client metadata.

### → #9 (Department contract)

- **Cross-department references**: `<entity>_id: str` convention applies to office-level references. Gate validation at write-time. Bundle B's gate signature considers this in the cross-ref validation tightness decision.

### → governance-and-identity-sourcing.md (cross-DR)

- This DR's Client + Actor schemas implement the entity-tier portion. governance-and-identity-sourcing decision 1-3 + 5 cover the GOVERNANCE + IDENTITY SOURCING + REGISTRATION SHAPE; this DR covers the SCHEMA + ENTITY-TIER definition. They compose; cross-ref each other.

## Pattern-vs-instance check

Generalizes to:

| Domain | Office-level entities |
|---|---|
| **Legal practice** | Client (matter's client); Actor (lawyers, paralegals, opposing counsel referenced as actors); plus possibly Court (referenced by litigation department's matters) — could be office-level or universal-scope |
| **Research lab** | Client (granting agency, sponsoring institution); Actor (PIs, postdocs, collaborators); plus possibly Funder (similar to Court) |
| **Brand voice** | Client (the brand client); Actor (creative director, copywriter, designer) |
| **Healthcare clinic** | Patient (analogous to Client — entity-shaped because billing + matter-of-record); Actor (clinicians, admin staff); plus Insurer |

The Client + Actor pattern generalizes; per-domain there might be ADDITIONAL office-level entities (Court, Funder, Insurer, etc.), each evaluated per entity-elevation 3-test.

## Pioneer-instance check

PBS validates:
- **Actor** today: Gunther + Hendrik are the actors. `actor_kind="human"`, `kind="internal"`. Test: does the schema serve session-by-session attribution? Yes (per #6 retrofit).
- **Client** today: Maxsolar, Solarfaktor, etc. as project clients. Test: does the schema serve `<project>.client_id` cross-ref? Yes.

Adapter mode validates when first concrete adapter ships in #11.

## Revisit triggers

- **First adapter-mode Client deployment** (e.g., consulting client with Salesforce as CRM): validate Client schema + adapter Protocol composition.
- **First adapter-mode Actor deployment** (e.g., Personio integration): validate Actor schema + adapter Protocol + governance role enforcement composition.
- **Multi-tenant scenarios** (Tier 3 / cross-org federation): cross-tenant Client/Actor isolation may require additional schema fields.
- **Per #14 Memory Bank lands**: confirm actor/client metadata indexes correctly + filter queries work.

## Files touched (when this commitment lands)

- `docs/decisions/office-level-managed-entities.md` — this file (NEW, backfill)
- `extensions/office/entities/client.py` — `ClientEntity` Pydantic
- `extensions/office/entities/actor.py` — `ActorEntity` Pydantic
- `extensions/office/clients/*.md` — Client instances per deployment
- `extensions/office/actors/*.md` — Actor instances per deployment
- `extensions/office/office.md` — registration declaring `managed_entities.client` + `managed_entities.actor`
- `docs/conventions/entity-md-spec.md` — Layer 2 schema scaffold for Client + Actor (already partially exists)
- `backend/mcp-server/src/pbs_mcp/audit_trail.py` — `actor` field references Actor.id
- `ROADMAP.md` — commitment #15 marked shipped + cross-ref this DR
