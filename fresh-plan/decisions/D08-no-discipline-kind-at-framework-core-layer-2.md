# D8 — 2026-05-08 — No "discipline" kind at framework-core layer 2

**Decision**: There is no unified `discipline` kind in framework-core. The mechanisms-formerly-called-disciplines from the prior corpus (audit, sparring, gate, authority-binding, etc.) decompose across the existing kinds and the shape layer:

- **Audit** → built into the workspace kind's state facet by construction (per D7 §3 + I3: every state mutation is an event; audit-trail is automatic). Not a kind.
- **Sparring** → shape policy bundle (per D4). The shape kind defines how policy is declared; specific sparring configurations live in specific shapes (e.g., practitioner-shape).
- **Gate / HITL checkpoints** → likely specialist capability and/or shape policy ("when does approval fire"). Not a kind.
- **Authority-binding** → shape policy ("which actor must attest which event-subtypes"). Not a kind.

**Rationale**: The prior corpus's "Mechanism Surface" pattern abstracted these mechanisms as if they shared a contract. They don't — audit is logging-by-construction, sparring is engagement, gate is a checkpoint, authority-binding is attestation. Each carries different semantics. A unified `discipline` kind would be over-abstraction (a shared base with no actually-shared contract). Per D2, kinds at framework-core are abstractions of distinct kinds-of-things; they should not be invented for symmetry.

**Supersedes**: prior corpus's "Mechanism Surface (Pattern A)" framing at framework-kind level. The Pattern A discriminator concept (≥2 conformant impls per kind) survives as a property of *each* kind that has it (likely substrate); it is not itself a unified meta-pattern at the kind layer.

**Note**: shape-level mechanisms (sparring, gate, authority-binding configurations carried by specific shapes) may share patterns *within a shape's policy bundle structure*. Whether shapes formalize that structurally is a shape-kind concern (defined when we get to the `shape` kind), not a discipline-kind concern.
