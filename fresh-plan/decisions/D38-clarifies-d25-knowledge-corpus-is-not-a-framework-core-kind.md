# D38 — 2026-05-11 — Clarifies D25 — knowledge / corpus is not a framework-core kind

**Decision (clarifies D25)**: "Knowledge" or "corpus" is **not** a framework-core kind. The 8 layer-2 kinds (D25) remain final. Knowledge as a deployment concern is supported via existing primitives:

- **Retrieval-shaped adapters** (per D16; canonical example: RAG-via-MCP per D26 Phase B B7).
- **Workspace state event projections** (claim payloads per D10 carry assertional content; per D40 events are queryable; per D39 state is fully derived from chain).
- **Shape policy** declaring knowledge-related hooks / roles / authority-bindings (e.g., a knowledge-centric shape declares roles like `curator` / `consumer` and hooks like `pre-citation`).

### Rejected alternative (named)

**Sana AI's "knowledge platform + agents" thesis**: knowledge is the central artifact; agents are tools over knowledge. Sana was acquired by Workday in 2025; the thesis has commercial traction.

Why fresh-plan rejects at framework-core: per D4 inclusion test, legitimate shapes have no knowledge corpus (e.g., financial-trading using real-time data feeds; process-automation orchestrating workflows; autonomous-business with proprietary internal state). Forcing knowledge as a core primitive fails the inclusion test the same way the VISION axes did.

Per fresh-plan's I3 (accountability-bearing AI-human work, per D5): *work* is the central organizing primitive; knowledge is supporting infrastructure. Different deployments have different relationships to knowledge — some are knowledge-centric (Sana-shape candidate); some treat knowledge as ambient context; some don't engage with knowledge at all.

### Precedent

Same shape as D8 ("no `discipline` kind at framework-core layer 2"): mechanisms-formerly-called-disciplines decompose across existing kinds. Same principle: knowledge-related mechanisms decompose across adapters, events, and shape policy. No new kind.

**Cross-references**: D4 (inclusion test); D5 I3 (accountability-bearing work as central primitive); D8 (precedent — "no discipline kind"); D10 (claim payload carries assertional content); D16 (retrieval-shaped adapters); D25 (layer 2 closure; this entry defends the kind set against the knowledge-thesis alternative); D26 Phase B B7 (RAG-via-MCP); D40 (projection / query contract enabling knowledge-related projections).
