# Profile L9: Shape catalog curator

**Status: PRELIMINARY — skeleton (full content TBD)**

**Lifecycle stage**: L9 (ecosystem stage; shape catalog maintenance)
**Shape variation**: meta (curates across multiple shapes)
**Archetype**: framework-affiliated maintainer; possibly community
**Scale**: typically small team or framework-affiliated authors

## Identity + context

Maintains the catalog of shape variants over time. Distinct from L2 (shape definer) — L2 creates new shapes from scratch; L9 curates the catalog of already-existing shapes + their variants. Tasks:
- Maintaining shape variants (DACH-planning vs UK-planning vs US-planning per jurisdiction)
- Cross-shape consistency checking (do related shapes use compatible vocabulary?)
- Versioning + migration governance for shapes
- Deprecation + archival of obsolete shapes
- Quality / review for new shape contributions
- Documentation + discovery (helping L1-L4 actors find appropriate shape)

This profile becomes more important as ecosystem matures (multiple shapes; multiple variants per shape; multiple contributors).

## What this profile is intended to EXEMPLIFY

This profile stress-tests:
- **Shape catalog versioning**: shape variants update over time; L4 deployers + L3 template creators consume specific versions
- **Shape variant inheritance**: DACH-planning extends planning-shape; what changes vs inherits
- **Cross-shape composition rules**: shape A + shape B for a workspace simultaneously valid?
- **Shape catalog discovery**: how do L4 deployers find appropriate shape?
- **Shape deprecation**: shape no longer maintained; existing deployments still using it
- **Shape contribution + review**: community contributes shape variant; quality / review process
- **Cross-jurisdictional shape variants** (DACH vs UK vs US planning shapes, etc.)
- **Shape catalog governance**: who decides what's official vs experimental vs deprecated
- **Per-version compatibility matrix**: shape v1.5 compatible with framework v0.40+ but not v0.35

## Packaging boundary section

n/a — L9 profile (curates packaged artifacts; not packaging itself).

## TBD sections (full content)

- Day-in-the-life / usage flow (catalog maintenance cycle)
- Hybrid moments (catalog work surfaces shape design issues; flow back to L2)
- Capability composition (catalog management tooling; per-shape testing infrastructure)
- Multi-user moments (this is core; community contribution + review chains)
- Edge cases (shape catalog corruption; deprecated-shape-still-in-use; community dispute over shape direction)

## Status

PRELIMINARY — skeleton. Full content drafted in subsequent session(s). Curator role becomes load-bearing as ecosystem matures beyond pioneer-only deployments.
