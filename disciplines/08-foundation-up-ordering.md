---
discipline: 8
title: Foundation-up workflow ordering
when_fires: Compositional / architectural work (GLOSSARY entries, DRs, ARCH topics, specs, layered design)
load_on_demand: true
---

# Discipline 8 — Foundation-up workflow ordering

When ordering compositional/architectural work (GLOSSARY entries, DRs, ARCH topics, specs, layered design), default to foundation-up: items others depend on come first; downstream items come last. Parallel-depth items batch with shared sharpening passes.

## Why

Locking downstream items first creates rework when their foundations land later (definitions need updating; cross-references need fixing). Foundation-up minimizes rework + ensures downstream items can cleanly reference locked foundations.

## How to apply

- Identify dependencies between items before ordering
- Lock items with no dependencies (or only on already-locked items) first
- Lock items that compose with multiple already-locked items last
- For parallel-depth items, batch them

## When NOT to apply

- Independent work (bug fixes, ad-hoc tasks) without inter-dependencies
- Chronological/event-driven order more important than dependency order
- Stakeholder timing forces non-foundation-up sequence
