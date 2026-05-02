# Profile L4b: Workspace deployer — IT admin at firm

**Status: PRELIMINARY — skeleton (full content TBD)**

**Lifecycle stage**: L4 (deployer stage)
**Shape variation**: practitioner-shape (firm-deploys-for-employees) or autonomous-business-shape (firm IT deploying business workspace)
**Archetype**: varies (firm's archetype determines deployment shape)
**Scale**: small firm (10-50 practitioners) to mid-size (50-200) to large firm

## Identity + context

IT administrator at firm with multiple practitioners. Deploys workspace template (L3) across many practitioners; manages updates, governance, multi-user policies, backup, security. Firm IT's concerns are different from L4a solo case: governance, policy enforcement, audit at firm-aggregate level, multi-tenant boundaries.

L6 (multi-user collaborator) concerns surface here: when L4b deploys multi-practitioner workspace, governance + visibility + authority are L4b's responsibility to configure correctly.

## What this profile is intended to EXEMPLIFY

This profile stress-tests:
- **Multi-tenant deployment**: many practitioners; per-practitioner customization vs firm-wide policy
- **Multi-user governance**: who can modify shape variants; who can activate new specialists; authority binding for capability changes
- **Per-office customization**: regional Layer A variants (NYC office Layer A vs LA office Layer A) within unified firm template
- **Update governance**: firm IT controls specialist version-bumps; per-practitioner adoption vs firm-wide forced update
- **Audit at firm-aggregate level**: cross-practitioner audit-trail aggregation; compliance reporting
- **Backup + disaster recovery** at firm scale
- **Security + access control**: who can read which practitioner's work; authority boundaries
- **License governance**: firm license vs per-practitioner; license accounting
- **Onboarding / offboarding**: new practitioner gets workspace; departing practitioner workspace handed off

## Packaging boundary section

(Full content TBD — validates firm-internal redistribution / template re-use / cross-office variation against L13 consumer profile.)

## TBD sections (full content)

- Day-in-the-life / usage flow (firm-wide deployment + ongoing IT operations)
- Hybrid moments (firm-policy + per-practitioner customization conflicts)
- Capability composition (firm IT tooling; admin dashboards)
- Multi-user moments (this profile IS multi-user; governance + authority + visibility throughout)
- Edge cases (departing practitioner work-unit reassignment; firm-policy change cascading; security incident)

## Status

PRELIMINARY — skeleton. Full content drafted in subsequent session(s). Multi-user governance concerns may surface architectural decisions affecting workspace primitive's multi-tenant story.
