# Self-application — when and how the kit updates itself

The kit's own update mechanism is itself an application of the kit's derivation procedure. There is no separate, privileged update procedure. The kit commits to the same discipline it prescribes.

If the kit's own derivation method cannot produce the kit, that is evidence the kit is wrong.

## Triggers for updating the kit

The kit should be re-derived when one or more of the following holds:

1. **Fundamental new research on AI failure modes** — published research that contradicts or extends a structural invariant. Treat invariants 1-10 in `structural-invariants.md` as falsifiable: each names a failure mode and a basis. New research that nullifies the failure mode (e.g., the failure no longer occurs in current models) or invalidates the basis (e.g., the cited research was misread or has been retracted or superseded) is a trigger
2. **New frontier model release** — major capability shifts may obsolete some invariants (failure modes the model no longer exhibits) or surface new ones (capabilities introduce failure modes the kit doesn't address). Re-evaluate within a reasonable window after release
3. **Cross-project recurring failure not covered by current invariants** — when projects running the kit repeatedly hit a failure mode the invariants don't address, that is evidence the kit is incomplete. Threshold: the same failure mode observed across multiple independent projects (cross-project, not within-project — within-project recurrence is handled by the derived procedure's own adoption criteria)
4. **Citation staleness** — any cited external source older than ~12-18 months should be re-verified periodically. Research moves; positions evolve; what was canonical guidance may have been refined or retracted

Triggers are observable — anyone with access to the inputs (research, model releases, cross-project failure logs) can detect them. The kit does not depend on a single privileged maintainer for its updates.

## Self-application protocol

When a trigger fires:

1. **Treat "build an AI-collaboration kit" as a project domain** — its artifacts are this kit's documents (`README.md`, `structural-invariants.md`, `derivation-procedure.md`, `self-application.md`, `meta-rules.md`). Its goal is robust AI-partnered work across projects
2. **Run the derivation procedure** (`derivation-procedure.md`) against this domain — what would Step 1 (apply structural invariants verbatim), Step 2 (identify protected artifacts), Step 3 (derive hooks), Step 4 (derive named skills), etc. produce for this kit, given current research and current observed failure data?
3. **Compare the derived result to the current kit** — divergence points are where the kit has drifted past current reality
4. **Refine where the comparison shows divergence** — replace, extend, or retire kit content per the comparison. Add new invariants if the derivation surfaces failure modes not addressed; retire invariants if the derivation no longer needs them
5. **Update the kit's own provenance and citation dates** — record when the update happened, what changed, what evidence drove the change
6. **Re-tag evidence tier per claim** (per `meta-rules.md`) — some invariants will be more strongly evidenced after re-derivation; some weaker; some new

This is the strong form of dogfooding. The recursion is honest because the kit doesn't claim a privileged update path — it submits to its own discipline.

## Falsifier role

Under this self-application discipline, the kit's falsifier is not a designated human role. It is **external research** plus **cross-project failure data**. Both are observable inputs. Anyone with access can run the falsification.

This differs from frameworks where the falsifier is a privileged maintainer. The advantage is decentralization: any adopter can challenge the kit by pointing to research or failure data. The cost is that no one is institutionally responsible for periodic re-derivation. Adopters who want assurance of ongoing maintenance should designate that responsibility within their own organization, not assume the kit is centrally maintained.

## What the kit does NOT auto-update

Per-project procedures (the artifacts derived from this kit) are NOT updated when the kit updates. They have their own maintenance protocols, scoped to their projects and calibrated to their own cost-of-error and failure cadence.

A kit update may *invite* re-derivation in adopter projects (especially when an invariant changes), but adopters decide whether and when to act based on their own circumstances.

The kit's update is a notification to adopters, not a forced cascade.

## Versioning discipline (recommended)

When the kit updates, increment a version marker (date or semantic version) and record:

- What changed (which files, which sections)
- Which trigger fired
- What evidence drove the change
- Whether the change invalidates per-project procedures derived from prior versions (most changes will not; structural invariant changes might)

This lets adopters decide whether their derived procedure needs revisiting after a kit update.
