# Profile L3: Deployment template creator

**Status: PRELIMINARY — skeleton (full content TBD)**

**Lifecycle stage**: L3 (creator stage; composition level)
**Shape variation**: works across shapes (creates templates for multiple shape variants)
**Archetype**: domain-specific (template targets specific archetype like "AI Planungsbüro")
**Scale**: typically small team / consultancy / framework-affiliated authors

## Identity + context

Composes specialists (L1) + shape (L2) + Layer A content + sensible defaults + initial entity configurations into a "ready-to-deploy X" template. User's example: "AI Planungsbüro ready-to-deploy" — composes practitioner-shape + planning-domain knowledge (Layer A) + planning-specialists set + Brandenburg/DACH defaults + pioneer-derived workflow definitions.

This is a HIGHER COMPOSITION LEVEL than L1 or L2 — works on already-packaged artifacts. Output: a deployable template that L4 (workspace deployer) instantiates.

## What this profile is intended to EXEMPLIFY

This profile stress-tests:
- **Composition rules**: what gets fixed in template vs configurable per L4 deployment
- **Template boundary**: what's in template vs reserved for L4 customization
- **Multi-artifact composition**: specialist set + shape + Layer A + entities — clean composition required
- **Domain-targeted template design**: "AI Planungsbüro" assumes planning archetype; what defaults make sense
- **Template versioning + L4 migration**: template update affects existing deployments
- **License + IP composition**: specialist licenses (possibly OSS) + shape license (framework) + template license (composer's IP) — license stack must compose cleanly
- **Cross-substrate templates** (substrate-agnostic vs substrate-pinned templates)
- **Template testing**: how does L3 creator validate template before distribution? Test deployments? Reference deployment?

## Packaging boundary section

(Full content TBD — validates template packaging against L13 consumption modes.)

## TBD sections (full content)

- Day-in-the-life / usage flow (composing a deployment template)
- Hybrid moments (when composition surfaces specialist or shape gaps; flow back to L1/L2)
- Capability composition (template-development tooling; reference-deployment management)
- Multi-user moments (collaborative template development; community contribution to "AI Planungsbüro" template)
- Edge cases (template-update breaking existing deployments; specialist-shape composition conflicts within template)

## Status

PRELIMINARY — skeleton. Full content drafted in subsequent session(s) per BACKLOG. Concrete grounding from "AI Planungsbüro ready-to-deploy" composition once first template materializes.
