# Profile L4a: Workspace deployer — solo self-deploy

**Status: PRELIMINARY — skeleton (full content TBD)**

**Lifecycle stage**: L4 (deployer stage)
**Shape variation**: typically practitioner-shape; can be other shapes
**Archetype**: matches L5 archetype practitioner is part of
**Scale**: solo (single practitioner deploying their own workspace)

## Identity + context

Solo practitioner (could be same person as L5 practitioner-user) sets up their own workspace from a deployment template (L3) or from scratch. Pioneer reality: PBS-Schulz origin is L4a (Gunther deploying his own workspace). Often the practitioner IS the deployer in solo / very-small-firm cases.

Distinct from L4b (firm IT) — L4a has personal context + customization vs firm-policy-driven deployment.

## What this profile is intended to EXEMPLIFY

This profile stress-tests:
- **Solo deployment ergonomics**: how easy is workspace deployment for non-IT-specialist practitioner?
- **Template instantiation**: choosing template; configuring per-instance details (practitioner identity; jurisdiction; specialist set)
- **Customization boundary**: what L3 template fixes vs what L4a deployer configures
- **Substrate selection**: choosing substrate (Claude Agent SDK vs other); per-substrate setup mechanics
- **Adapter configuration**: email integration; document-signing; LaTeX compile — per-deployment configuration
- **Initial entity setup**: practitioner-record; default work-units; reference content
- **Update / re-deployment semantics**: practitioner-as-deployer updates own workspace
- **Backup + migration** for solo case (practitioner moves between machines; substrate change; etc.)

## Packaging boundary section

(Full content TBD — validates that deployed workspace can be backed up / migrated / cloned per L13 consumer profile.)

## TBD sections (full content)

- Day-in-the-life / usage flow (initial deployment + ongoing maintenance)
- Hybrid moments (deployment surfaces template gaps; flow back to L3)
- Capability composition (deployment tooling; setup wizards)
- Multi-user moments (n/a for solo case; degenerate to single user)
- Edge cases (substrate failure; substrate migration; corrupted state recovery)

## Status

PRELIMINARY — skeleton. Full content drafted in subsequent session(s). Pioneer experience grounds this profile (PBS-Schulz origin = L4a deployment).
