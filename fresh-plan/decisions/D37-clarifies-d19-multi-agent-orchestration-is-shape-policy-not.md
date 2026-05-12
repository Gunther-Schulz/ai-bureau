# D37 — 2026-05-11 — Clarifies D19 — multi-agent orchestration is shape-policy, not framework-core

**Decision (clarifies D19 + D8)**: Multi-agent orchestration semantics — orchestrator-vs-worker distinctions, delegation patterns, coordination flow — are **shape policy**, not framework-core. Per D19's existing wording: "Event-driven (preferred at framework level): specialists subscribe to other specialists' / adapters' / shape's emissions and react via their skills. RPC-style direct invocation between specialists is implementation-shape." This entry formalizes that wording as the canonical framework-level answer.

### Rejected alternative (named)

**Kore.ai's orchestrator-vs-worker pattern**: explicit orchestrator-role designation on specialists; framework-level routing-by-role; 300+ pre-built industry templates assuming this distinction. The pattern has commercial traction and scale evidence.

Why fresh-plan rejects at framework-core: per D4 inclusion test, legitimate shapes opt out of an orchestrator-vs-worker distinction (e.g., autonomous-business-shape with parallel specialists; financial-trading-shape with broadcast-then-aggregate semantics). Forcing the distinction into core fails the inclusion test the same way the VISION axes did.

### How shapes express orchestration

Shapes that need orchestrator-worker patterns declare them via existing D13 slots:

- **`roles[]`** — shape declares `orchestrator` + `worker` as shape-level role-tags.
- **`hooks[]`** — shape declares `pre-delegate`, `post-aggregate`, etc.
- **`authority-bindings[]`** — shape requires delegation events to be attested by the orchestrator role.

No framework-core changes needed; D19's existing mechanisms accommodate the full Kore.ai pattern at shape level.

**Cross-references**: D4 (inclusion test); D8 (routing is not a framework-core kind); D13 (shape policy slots); D19 (specialist cross-specialist coordination); D26 Phase E (multi-deployment validation as evidence-gathering for shape-neutrality).
