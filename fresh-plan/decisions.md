# fresh-plan decisions — index

Append-only ledger of architectural decisions. Each entry is locked once added; supersedes-relationships are explicit. **Per-entry content lives in `decisions/D<NN>-<slug>.md`** — this file is the chronological index. For entry conventions, see `README.md` "Ledger conventions"; for cross-cutting framework orientation, see `CONCEPTS.md`; for execution tracker (phases × workstreams), see `roadmap.md`.

## Conventions

- **Append-only**: existing entries do not get edited. Changes to existing decisions land as new entries (clarification / supersedes / extends pattern).
- **Cross-references** use D-numbers (e.g., "D44", "D34 §A.5") — *not* file paths. The D-number is canonical.
- **Filename scheme**: `decisions/D<NN>-<slug>.md` with two-digit zero-padding for lexicographic sort. Slug auto-derived from title.
- **Session-start procedure** loads this index + iterates all per-entry files in `decisions/` in numerical order.

## Index

- [D1](decisions/D01-build-target-conflict-rule.md) — Build target + conflict rule (2026-05-08)
- [D2](decisions/D02-framework-core-meta-layer-instances-extensions.md) — Framework-core = meta-layer; instances = extensions (2026-05-08)
- [D3](decisions/D03-core-is-layered-top-down.md) — Core is layered top-down (2026-05-08)
- [D4](decisions/D04-framework-core-has-no-substantive-identity-commitments.md) — Framework-core has no substantive identity commitments (2026-05-08)
- [D5](decisions/D05-framework-core-identity-layer-structural-commitments.md) — Framework-core identity layer (structural commitments) (2026-05-08)
- [D6](decisions/D06-layer-2-enumeration-approach-incremental-closure-check.md) — Layer 2 enumeration approach (incremental + closure check) (2026-05-08)
- [D7](decisions/D07-workspace-kind.md) — Workspace kind (2026-05-08)
- [D8](decisions/D08-no-discipline-kind-at-framework-core-layer-2.md) — No "discipline" kind at framework-core layer 2 (2026-05-08)
- [D9](decisions/D09-actor-kind.md) — Actor kind (2026-05-08)
- [D10](decisions/D10-event-kind.md) — Event kind (2026-05-08)
- [D11](decisions/D11-layering-clarification-formal-schema-is-layer-3-format-is.md) — Layering clarification: formal schema is layer 3, format is implementation (2026-05-08)
- [D12](decisions/D12-substrate-kind.md) — Substrate kind (2026-05-08)
- [D13](decisions/D13-shape-kind.md) — Shape kind (2026-05-08)
- [D14](decisions/D14-layer-2-refinement-pass-discipline.md) — Layer 2 refinement-pass discipline (2026-05-08)
- [D15](decisions/D15-standards-compatibility-criterion-for-refinement-pass.md) — Standards-compatibility criterion for refinement pass (clarifies D14) (2026-05-08)
- [D16](decisions/D16-adapter-kind.md) — Adapter kind (2026-05-08)
- [D17](decisions/D17-supersedes-d12-core-capability-vocabulary-strict-protocol.md) — Supersedes D12 core capability vocabulary (strict protocol-neutrality applied) (2026-05-08)
- [D18](decisions/D18-clarifies-d15-wording-per-strict-protocol-neutrality.md) — Clarifies D15 wording (per strict protocol-neutrality) (2026-05-08)
- [D19](decisions/D19-specialist-kind.md) — Specialist kind (2026-05-08)
- [D20](decisions/D20-work-unit-kind.md) — Work-unit kind (2026-05-08)
- [D21](decisions/D21-workspace-as-a2a-peer-deployability-requirement.md) — Workspace-as-A2A-peer deployability requirement (2026-05-08)
- [D22](decisions/D22-refinement-d9-substrate-binding-resolution-clarified.md) — Refinement: D9 substrate-binding resolution clarified (2026-05-08)
- [D23](decisions/D23-refinement-d10-events-gain-work-unit-id-slot-supersedes-d10.md) — Refinement: D10 events gain `work-unit-id` slot (supersedes D10 slot list) (2026-05-08)
- [D24](decisions/D24-refinement-pass-output-cross-kind-consistency-4a-flags.md) — Refinement-pass output: cross-kind consistency + 4a flags + standards-compatibility findings (2026-05-08)
- [D25](decisions/D25-layer-2-closure-final-kind-set-layer-2-complete.md) — Layer 2 closure (final kind set; layer 2 complete) (2026-05-08)
- [D26](decisions/D26-indicative-roadmap-for-post-layer-2-phases.md) — Indicative roadmap for post-layer-2 phases (2026-05-08)
- [D27](decisions/D27-phase-a-enumeration-approach.md) — Phase A enumeration approach (2026-05-09)
- [D28](decisions/D28-formal-schema-notation-json-schema-draft-2020-12.md) — Formal-schema notation: JSON Schema (Draft 2020-12) (2026-05-09)
- [D29](decisions/D29-extension-manifest-contract-validation-flow.md) — Extension manifest contract + validation flow (2026-05-09)
- [D30](decisions/D30-cross-kind-referential-integrity-composition-rules-part-1.md) — Cross-kind referential integrity (composition rules part 1) (2026-05-09)
- [D31](decisions/D31-supersedes-d13-d29-extends-removed-from-shape-and-extension.md) — Supersedes D13 + D29: `extends` removed from shape and extension manifest (2026-05-09)
- [D32](decisions/D32-boot-time-resolution-multi-binding-circular-deps-load-order.md) — Boot-time resolution: multi-binding, circular deps, load order (composition rules part 2) (2026-05-09)
- [D33](decisions/D33-identifier-graduation-versioning-policy-workstream-5.md) — Identifier graduation + versioning policy (workstream 5) (2026-05-09)
- [D34](decisions/D34-phase-a-end-of-phase-refinement-pass-output.md) — Phase A end-of-phase refinement pass output (2026-05-09)
- [D35](decisions/D35-phase-a-closure-final-artifacts-phase-a-complete.md) — Phase A closure (final artifacts; Phase A complete) (2026-05-09)
- [D36](decisions/D36-phase-b-planning-workstream-order-setup-decisions-closure.md) — Phase B planning: workstream order + setup decisions + closure criterion (2026-05-09)
- [D37](decisions/D37-clarifies-d19-multi-agent-orchestration-is-shape-policy-not.md) — Clarifies D19 — multi-agent orchestration is shape-policy, not framework-core (2026-05-11)
- [D38](decisions/D38-clarifies-d25-knowledge-corpus-is-not-a-framework-core-kind.md) — Clarifies D25 — knowledge / corpus is not a framework-core kind (2026-05-11)
- [D39](decisions/D39-clarifies-d7-3-extends-payload-composition-change-schema.md) — Clarifies D7 §3 + extends payload-composition-change schema — state is fully derived from the event chain (2026-05-11)
- [D40](decisions/D40-extends-d10-projection-query-contract-integrity-mechanism.md) — Extends D10 — projection / query contract + integrity-mechanism extension point (2026-05-11)
- [D41](decisions/D41-clarifies-d26-d36-two-substrate-parity-required-for-phase-b.md) — Clarifies D26 + D36 — two-substrate parity required for Phase B closure (2026-05-11)
- [D42](decisions/D42-clarifies-d14-d36-formalize-bref-as-named-phase-b.md) — Clarifies D14 + D36 — formalize Bref as named Phase B refinement workstream (2026-05-11)
- [D43](decisions/D43-supersedes-d17-rename-core-capability-event-streaming-event.md) — Supersedes D17 — rename core capability `event-streaming` → `event-chain` (2026-05-11)
- [D44](decisions/D44-extends-d37-subscriber-dispatch-is-queued-fifo-drain-with.md) — Extends D37 — subscriber-dispatch is queued (FIFO drain) with loop backstop (2026-05-11)
- [D45](decisions/D45-establishes-detection-surface-recovery-triad-as-standing.md) — Establishes detection-surface-recovery triad as standing requirement for runtime decisions (2026-05-12)
- [D46](decisions/D46-extends-d7-d32-boot-procedure-honors-detection-surface.md) — Extends D7 + D32 — boot procedure honors detection-surface-recovery triad (boot-procedure cluster per D45) (2026-05-12)
- [D47](decisions/D47-extends-d13-d17-d37-d44-subscriber-dispatch-hook-firing.md) — Extends D13 + D17 + D37 + D44 — subscriber dispatch + hook firing honor detection-surface-recovery triad (subscriber-dispatch cluster per D45) (2026-05-12)
- [D48](decisions/D48-extends-d16-adapter-cluster-honors-detection-surface-recovery.md) — Extends D16 — adapter cluster honors detection-surface-recovery triad (per D45 §C) (2026-05-12)
- [D49](decisions/D49-clarifies-d47-c-d-d48-b2-sharpen-surfaced-corrections.md) — Clarifies D47 §C + §D + D48 §B.2 — sharpen-surfaced corrections (step-count + missing handler-index defer + Recovery-row wording) (2026-05-12)
- [D50](decisions/D50-extends-d19-specialist-cluster-honors-detection-surface-recovery.md) — Extends D19 — specialist cluster honors detection-surface-recovery triad (per D45 §C) (2026-05-12)
- [D51](decisions/D51-extends-d29-d30-validation-cluster-honors-detection-surface-recovery.md) — Extends D29 + D30 §4 — validation cluster honors detection-surface-recovery triad (per D45 §C) (2026-05-12)
- [D52](decisions/D52-extends-d10-d13-d39-composition-change-cluster-honors-detection-surface-recovery.md) — Extends D10 + D13 + D39 — composition-change cluster honors detection-surface-recovery triad (per D45 §C) (2026-05-17)
- [D53](decisions/D53-extends-d38-sana-style-worked-example-validates-fresh-plan-core-kinds.md) — Extends D38 — Sana-style worked-example validates fresh-plan core kinds against knowledge-work use case (2026-05-17)
