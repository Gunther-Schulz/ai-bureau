# D11 — 2026-05-08 — Layering clarification: formal schema is layer 3, format is implementation

**Decision**: The mental model of framework levels is sharpened to distinguish three things that earlier entries (D7, D9, D10) referred to loosely as "schema":

| Level | Content |
|---|---|
| **Layer 1** (identity) | What the framework IS, structurally (D5). |
| **Layer 2** (kinds) | **Semantic contracts**: slot lists, cardinalities, relationships, invariants. What we're producing now (D7, D9, D10, ongoing kinds). |
| **Layer 3** (extension protocol) | **Formal schemas** for each kind (concrete enough to validate, format-neutral) + extension declaration mechanism + conformance validation + composition rules + promotion / demotion rules. |
| **(Below layer 3) Implementation** | **Format / serialization choices** (JSON / YAML / Pydantic / Protobuf / etc.), **storage / wire / protocol** (files, DB, streams, etc.), specific extension impls. |

**The bridging element**: an extension impl cannot be written from layer 2 alone. It needs **layer 3's formal schemas** to know what conformance looks like. Layer 2 says "events form an ordered chain"; layer 3 says "id is a non-empty UTF-8 string ≤ 256 chars; prev-event is a nullable string reference matching `^evt-[a-zA-Z0-9-]+$`; timestamp is ISO-8601 UTC"; implementation says "encoded as JSON in append-only file."

**Format and serialization choices remain implementation-level** (below layer 3); they are not framework-core decisions. Multiple impls may serialize differently and still conform, as long as each impl's serialization round-trips through the formal schema.

**Where prior entries used "schema" loosely**: D7 ("Concrete schema of the manifest (Pydantic, markdown, both, other) — implementation choice; layer-3 territory"), D9 (similar wording), D10 (similar wording). The intended meaning was **formal schema = layer 3**; **format / serialization = implementation**. The prior entries' "schema" referred to formal schemas (correctly placed at layer 3); examples like "Pydantic, markdown" are serialization choices (implementation).

**Rationale**: without this distinction, "implementation choice; layer-3 territory" was ambiguous. Locking the distinction prevents drift in subsequent kind definitions and makes clear what each layer must produce before impl work can begin.

**Procedural implication**: layer 2 enumeration can finish (per D6 closure) before layer 3 begins; but **layer 3 is non-optional** for any impl work to follow. It is a later phase of framework-core work, not an afterthought or implementation concern.
