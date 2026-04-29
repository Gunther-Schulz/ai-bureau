# Output conventions

How to structure the artifact + recommendations.

---

## Subsystem verdict types

Each subsystem reviewed gets exactly one verdict. The verdict
captures the subsystem-level judgment; recommendations capture the
specifics.

### Refined

Actual ≈ greenfield. The from-scratch design would look essentially
like the existing form. **No recommendations**.

This is a positive outcome, not a failure of the review. Some
subsystems ARE right-shape; saying so is the correct verdict.

### Rough but adequate

Actual diverges from greenfield, but the divergence doesn't pay
off enough to justify changing. Recommendations exist (Keep
bucket: documenting the divergence + the reasoning for not
changing) but no action items.

Use this verdict when the cost of change exceeds the benefit, even
under pre-launch freedom-to-rewrite. Examples:

- A naming convention that's slightly off but consistent
- A minor structural choice that has edge cases but works

### Rough and worth refining

Actual diverges from greenfield in ways that **do** pay off
changing. Recommendations are mostly Refactor-bucket; a Reshape or
two might also apply. The user should act on these.

Use this verdict when the divergence has visible cost (drift, bug
risk, friction for new contributors) and a bounded change closes
the gap.

### Wrong shape

Actual diverges from greenfield fundamentally. The bounded
refactor doesn't reach greenfield. Recommendations are mostly
Reshape-bucket — restructure abstractions, possibly delete entire
concepts.

This is the verdict that the anti-bias mechanism is designed to
make speakable. It will feel uncomfortable to assign, especially
for subsystems with significant existing investment. **Assign it
anyway when warranted.** The unique pre-launch window makes
Reshape recommendations cheap to act on; that window closes when
the system goes live.

---

## Recommendation buckets

Each recommendation gets exactly one bucket.

### Keep

Existing form is right OR cost-of-change exceeds benefit.

Default for **Refined** subsystems (where the recommendation might
be "document the rationale for the existing choice so future
review doesn't re-discover it"). Sometimes appears in **Rough but
adequate** subsystems too, alongside the divergence-acknowledgment.

### Refactor

Existing concept is right; implementation needs work; bounded.

Examples:
- Extract a helper function
- Split a long file
- Consolidate a few similar functions into one
- Rename for clarity

The concept doesn't change. The shape doesn't change. The
implementation gets cleaner.

### Reshape

The concept is wrong-shape — restructure abstractions, possibly
delete entirely.

Examples:
- Replace a 3-axis decomposition with a 2-axis one
- Delete a concept that doesn't earn its keep
- Reverse a layering (X depends on Y → Y depends on X)
- Re-decompose a subsystem along a different axis

Reshape recommendations are the highest-leverage outputs of
design-review. Unlike Refactor, they affect downstream callers /
consumers. But under pre-launch freedom, they're still cost-cheap.

---

## Required output fields per recommendation

Every recommendation must include:

1. **Bucket** (Keep / Refactor / Reshape)
2. **Title** — short imperative phrase ("Extract chunker
   dispatcher to a registry" / "Delete the X concept")
3. **Greenfield grounding** — explicit reference to the
   from-scratch sketch. This is the load-bearing connection that
   keeps the recommendation tied to the anti-bias mechanism.
   Without it, the recommendation is just opinion.
4. **What it unlocks** — concrete benefit if acted on
5. **What breaks** — concrete cost / migration / breaking change
6. **Cost** — Small / Medium / Large (relative bucket, not hours)

Example:

```markdown
**Reshape: Extract the chunker dispatcher to a capability registry**

- **Greenfield grounding**: a from-scratch design wouldn't
  hardcode path heuristics in `select_chunker`; it would dispatch
  through a capability registry where chunkers self-declare what
  they handle.
- **What it unlocks**: third-party chunker plugins; cleaner
  testing; chunker selection becomes data, not code.
- **What breaks**: 9 chunker modules need a constructor signature
  change; `select_chunker` becomes a registry lookup; in-flight
  ingest paths might need migration.
- **Cost**: M
```

The greenfield grounding is the load-bearing line. If the
recommendation can't be grounded — if there's no specific
from-scratch difference being cited — the recommendation isn't
ready to ship. Drop or defer.

---

## Cross-cutting recommendations section

Some reshapes affect multiple subsystems simultaneously. Examples:

- "Restructure the meta-rule numbering" affects every entity that
  references a meta-rule
- "Replace scope orthogonality with a different decomposition"
  ripples through manifests + skills + bausteine + office-config
- "Unify audit + design-review under a single review framework"
  affects both skills + their downstream consumers

These don't fit cleanly in any one subsystem's recommendations.
The artifact has a dedicated **Cross-cutting** section after the
per-subsystem sections.

Cross-cutting recommendation has the same fields as per-subsystem
recommendations, plus:

- **Affected subsystems**: list of the subsystems that would be
  touched by this change

Cross-cutting threshold: the recommendation must affect **3 or
more** subsystems to belong in this section. 2-subsystem reshapes
go in one of the affected subsystems with a note ("this also
affects subsystem Y").

If the cross-cutting section is accumulating everything (every
recommendation gets lifted there), tighten the threshold. The
per-subsystem view shouldn't become empty.

---

## Artifact format

```markdown
# Design review — <scope> — <YYYY-MM-DD>

**Trigger**: <which trigger fired (full / focused / phrase)>
**Scope**: <subsystem(s) reviewed>
**Mode**: full | focused

## Verdict summary

| Subsystem | Verdict |
|---|---|
| Architecture meta-rules | Rough but adequate |
| Entity types + decision rules | Rough and worth refining |
| ... | ... |

## Per-subsystem reviews

### <Subsystem 1>

**Verdict**: <one of 4>

**Greenfield sketch** (one paragraph; what would we build today?):

<paragraph>

**Recommendations**:

[grouped by bucket; each with required fields]

### <Subsystem 2>

...

## Cross-cutting recommendations

[only if 3+-subsystem reshapes exist; else "none surfaced"]

## Recommended next action

[concrete: which Reshape to act on first, which to surface for
discussion, which to log as follow-up reviews]
```

The greenfield sketch IS produced as output (one paragraph per
subsystem) — this is different from the agent's private greenfield
reasoning. The output sketch is the user-facing summary of "what
would the from-scratch alternative look like" so the user can
assess whether the recommendations are grounded sensibly.

(This refines the "private to agent reasoning, not output" rule
slightly: the agent's full greenfield reasoning stays private, but
a short summary version surfaces in the artifact for transparency.
Without it, the user has no way to assess whether the
recommendations are well-grounded.)

---

## Closure tracking

Artifact is **frozen** at write-time. Don't edit recommendations
after the fact (muddies historical record).

**Closures live in two places**:

1. **Closure banner** — one-liner appended above the artifact
   title after acting:
   ```
   > **Closure status (post-<event>):** <N> recommendations acted
   > on in commits <sha>; <M> deferred to <when>; <K> rejected
   > with reasoning in HANDOFF.
   ```

2. **HANDOFF.md** — the active session-state doc. Captures
   verdicts per subsystem + which recommendations the user acted
   on / deferred / rejected.

This keeps the artifact a snapshot while the closure trail is
discoverable.

---

## File naming + location

Artifacts live in `docs/design-reviews/`:

```
docs/design-reviews/<scope>-<YYYYMMDD>.md
```

Examples:
- `docs/design-reviews/foundations-20260429.md` (full first-run
  on load-bearing foundations)
- `docs/design-reviews/chunkers-20260615.md` (focused review
  before Phase 2a)
- `docs/design-reviews/orchestrator-20261201.md` (focused review
  triggered by orchestrator behavior surprising the user)
