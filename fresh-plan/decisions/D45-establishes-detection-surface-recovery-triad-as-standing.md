# D45 — 2026-05-12 — Establishes detection-surface-recovery triad as standing requirement for runtime decisions

**Decision (substantive; meta-foundation entry)**: Every locked decision affecting *runtime behavior* (boot, append, dispatch, projection, validation, query, lifecycle, or other moments where the impl behaves observably) MUST explicitly name a **detection-surface-recovery triad** in its FAILS framing — a named exception type or failure marker (detection), a user-visible diagnostic surface (not buried in logs), and a defined recovery path. Per D44 precedent — the only existing runtime decision honoring this discipline. Per the 2026-05-12 failure-mode + abandonment-path audit (the second probing.md non-original audit run; surfaced 33 SUSPECT runtime decisions lacking the triad). This entry promotes the D44 precedent from one-off implementation choice to standing requirement, applying forward to all new runtime decisions and backward (via cluster-level supersedes / extends entries) to existing ones. Bref deliverable per D42 — process-by-pattern revision of the original bounded-fill plan, codifying the discipline rather than processing 33 suspects in isolation.

### A. Scope — what counts as a runtime decision

A "runtime decision" is any locked decision whose subject matter is the impl's runtime behavior — code paths exercised when the workspace is operating, not configuration-only or process-only decisions. Concretely **in scope**:

- **Boot procedure** (D7 §workspace boot, D32 boot-time resolution, D29 §validation flow at boot)
- **Event-chain operations** (D10 append + integrity, D23 work-unit-id, D39 state derivation, D40 §A query interface, D44 subscriber dispatch)
- **Per-event runtime checks** (D30 §4, D34 §A.5)
- **Substrate runtime behaviors** (D12 + D17 + D43 capability vocabulary as runtime contract; substrate's `append_event` + `_dispatch_event_to_subscribers` + `_apply_runtime_side_effects`)
- **Shape policy enforcement** (D13 authority-bindings + hooks at runtime)
- **Adapter runtime** (D16 adapter call + binding resolution at runtime)
- **Specialist runtime** (D19 handle_skill + on_event + activation; D37 event-driven coordination)
- **Work-unit lifecycle** (D20 transitions; create / status changes / abandonment)
- **Workspace lifecycle** (D7 §lifecycle; boot / shutdown events)

**Out of scope** (these decisions don't have failure paths beyond schema/validator-level, OR they describe process not runtime):

- Purely structural decisions (kind contracts as identity claims, layer commitments, identity-axis claims like D5 I1/I2/I3)
- Purely procedural decisions (working patterns, ledger conventions, probing discipline meta-rules)
- Configuration / scope-setting decisions (D26 roadmap, D27 / D36 phase enumeration, D42 Bref formalization)

When in doubt, default to in-scope. The audit found "implicit" failure modes were where most SUSPECTs hid; treating decisions as in-scope by default matches the discipline's bias toward catching gaps.

### B. The triad — what each element requires

For each runtime decision in scope, the FAILS framing must name all three elements:

- **Detection** — *how* is the failure detected? Specific shape: typed exception raised; structured failure record returned; sentinel value; explicit error code; named state marker. Ambiguous "the operation fails" without naming the detection mechanism does not satisfy.
- **Surface** — *how* does the failure become observable? Bar: user-visible (where "user" includes operator, monitoring, and downstream code that needs to handle it). The user must be able to know "this thing failed" without reading server logs. Specific shapes: typed exception carrying a structured diagnostic message; named return-value shape with failure context; named log-with-alerting hook that's wired through to a user-visible channel. "Logged to stdout" without alerting does not satisfy. "Should never happen" without alerting does not satisfy.
- **Recovery** — *what* is the defined path after detection + surface? Specific shapes: caller catches and retries (idempotent path); caller catches and reports (escalation path); system aborts cleanly with state defined (abort-and-restart path); user is prompted to fix the cause (user-action path). "The system continues with undefined state" does not satisfy. "Restart the workspace" CAN satisfy if the entry is explicit that this is the recovery and what state survives.

D44 is the canonical concrete example:
- Detection: `n_dispatched > self.max_events_per_drain` counter exceeded.
- Surface: `RuntimeError` raised with structured diagnostic naming the offending event in flight (id + payload-subtype).
- Recovery: `self._dispatch_queue.clear()` leaves substrate in clean state; caller catches and handles or terminates the workspace.

Future runtime decisions should match D44's clarity.

### C. Application — forward + backward

**Forward (gating new entries)**: every new runtime decision must include the triad in its FAILS field per probing.md Procedure 1 (decision-shape template). The amended FAILS field (per probing.md amendment 1) explicitly cites this entry as the standing requirement. Pre-lock probe (probing.md Procedure 3 brief: *"what's the failure path?"*) tests whether the answer is real, not just present. Detection-surface-recovery audit (probing.md Procedure 2 amendment 2) catches at workstream-completion + phase-boundary checkpoints any gaps that slip past pre-lock.

**Backward (the audit-driven cleanup)**: existing runtime decisions lacking the triad need supersedes / extends entries to add it. Per the 2026-05-12 audit's 33 SUSPECT findings, the gaps cluster into ~5-6 runtime paths where one supersedes / extends entry can apply the triad across multiple SUSPECTs:

1. **Boot-procedure cluster** — D7 §workspace boot + D32 §boot-time resolution: silent ValueError swallowing in boot steps 6/7/8 (manifest-declared shape/adapter/specialist with unknown id); manifest-actor seeding mid-cascade rejection (no rollback; introduced in D39 closure work); capability-only substrate-binding error path post-B1.
2. **Subscriber-dispatch cluster** — D37 + D44: on_event exception silently swallowed (`substrate.py:193-197 except Exception: pass`); HookRegistry.fire integration site (hooks registered but never invoked anywhere in `impl/src/` — D13 hook contract is decorative until firing-sites land).
3. **Adapter cluster** — D16: adapter `call()` failure shape unspecified at framework level (Phase C real-wire = network / auth / timeout); adapter binding failure mid-boot (root cause lost, mis-attributed downstream).
4. **Specialist cluster** — D19: handle_skill failure shape unspecified; on_event exception path (composes with cluster 2).
5. **Validation cluster** — D29 + D30 §4: per-work-unit identity checks named in spec, never implemented in `per_event_checks.py`; B1 collect-all skipping when extensions empty (silent skip of capability + vocabulary + binding checks).
6. **Composition-change cluster** — D10 + D13 + D39: post-projection state validity unchecked (e.g., adding actor whose subtype contradicts shape's authority-binding requirements; composition-change passes per-event check but resulting state violates shape policy with no detection).

Each cluster gets one supersedes / extends entry establishing the triad for that runtime path. Estimated 5-6 entries → casts net over ~25-28 of the 33 SUSPECT findings. Remaining 5-8 SUSPECTs likely fold into the slot-pass (some overlap with slot-interpretation findings; not all 33 are pure-runtime-failure shaped). Tracked as Bref deliverables; logged in `roadmap.md`.

### D. Relation to D44 (precedent) and probing.md (discipline)

D44 (queued subscriber-dispatch + loop backstop) is the canonical precedent. Its structure becomes the template:

| Triad element | D44 instance |
|---|---|
| Detection | `n_dispatched > self.max_events_per_drain` counter |
| Surface | typed `RuntimeError` with diagnostic naming offending event |
| Recovery | `_dispatch_queue.clear()` + clean state for caller |

D44 also explicitly cited "Failure-modes-are-first-class" as rationale (per global CLAUDE.md). The 2026-05-12 audit found this citation was the *only* place the discipline was both cited and applied. Other entries cited but did not apply. This entry locks the requirement so the discipline is structurally enforced (via probing.md Procedure 1's amended FAILS field), not relied upon as authorial habit.

probing.md (the discipline) was amended 2026-05-12 with five edits responding to the audit; one edit specifically strengthened the FAILS field in Procedure 1 to require the D44 triad pattern. This entry (D45) is the substantive ledger lock that the probing.md amendment references — discipline + ledger lock together complete the loop.

### E. Pre-lock probe self-referentiality (skip with documented reason)

probing.md Procedure 3 mandates pre-lock adversarial probe for Tier-3 substantive D-entries. This entry IS the result of an adversarial probe (the 2026-05-12 audit). Running another probe pre-lock would be circular — the audit motivated the entry; the entry codifies the audit's recommendation; a pre-lock probe would re-derive what we already have.

**Pre-lock probe SKIPPED for D45.** Reason documented here; precedent established for future audit-driven entries: when the entry's content is already grounded in fresh-context audit findings, the pre-lock probe is redundant. The pre-lock probe's purpose is to test whether the author's reasoning has unsurfaced gaps; if the entry was *generated by* a fresh-context probe, that test has already happened. Future entries should cite this precedent + the audit they're grounded in when invoking the skip.

### What is NOT in this decision

- **No specific exception-type vocabulary** — each runtime decision picks its own exception type appropriate to its concern (`WorkspaceBootError`, `EventRejected`, `MalformedEventError`, `RuntimeError`, etc.). This entry does not enumerate or constrain.
- **No specific log/alerting mechanism** — substrate-impl concern; the framework specifies the requirement (user-visible), not the technology (stderr / structured logging library / OpenTelemetry / Sentry / etc.).
- **No specific recovery semantics for individual failure modes** — recovery is case-by-case per supersedes/extends entry. This entry establishes the requirement to define recovery, not what recovery should be.
- **No batch processing schedule for the 33 SUSPECT findings** — cluster-by-cluster (5-6 entries) is the recommended approach; future supersedes entries can choose granularity.
- **No performance or observability metrics requirements** — adjacent concern; not addressed here. Detection-surface-recovery is about *failure-mode discipline*, not telemetry coverage.
- **No retroactive rewriting of D44** — D44 already honors the triad implicitly; this entry doesn't supersede it. D44 stands as the precedent.
- **No automatic application to non-runtime decisions** — purely structural, procedural, or configuration-only decisions are out of scope per §A. If a decision's subject matter is contested (runtime vs configuration), default to in-scope.

### Decision-shape template self-application (per probing.md Procedure 1)

Eating own dog food — D45 honors the discipline it establishes:

- **WHAT**: standing requirement that runtime decisions name detection + surface + recovery in their FAILS framing.
- **WHO**: enforced by *framework-validator (probing.md decision-shape template at write-time)* + *deferred (Phase B closure of cluster supersedes entries) for backward cleanup*. New entries: pre-lock probe + decision-shape template gate. Existing entries: cluster supersedes entries process the SUSPECT findings.
- **FAILS**: when a future runtime decision is locked WITHOUT the triad — *Detection*: pre-lock probe surfaces (probing.md Procedure 3 brief: "what's the failure path?"); detection-surface-recovery audit catches at next workstream-completion or phase-boundary checkpoint (probing.md Procedure 2 menu). *Surface*: probe report cites the missing triad element; audit findings list the offending entry. *Recovery*: supersedes/extends entry adds the triad before phase closure.
- **CROSS**: D44 §full entry (precedent; structure template); probing.md Procedure 1 §FAILS field amendment (write-time enforcement); probing.md Procedure 2 §detection-surface-recovery audit shape (audit-time enforcement); probing.md Procedure 3 §rotating brief menu ("what's the failure path?" brief tests answers); D5 §I3 (accountability anchor — detection-surface-recovery is what makes accountability operational, not just declared); the 33 SUSPECT findings from 2026-05-12 audit (motivating evidence; targets of cluster supersedes entries).
- **DEFERS**: per-cluster supersedes entries (5-6 entries; future Bref deliverables); specific exception vocabulary per decision (per-decision choice); recovery semantics for each failure mode (case-by-case); telemetry / observability standards (adjacent; future Phase C+ concern).

**Rationale**: The 2026-05-12 audit found D44 was the only runtime decision honoring the failure-mode-as-first-class discipline cited throughout the corpus. The discipline was named in entries' rationales but not consistently applied as a check. This is the canonical pattern of *discipline-cited-as-label-not-applied-as-check* that the audit explicitly named. Pattern-level lock (this entry) addresses the pattern; cluster supersedes entries clean up existing instances. Process-by-pattern (this approach) over process-by-suspect (handle 33 items individually) per the bounded-fill plan revision: pattern-level processing prevents repeating the local-over-global failure mode at scale (which is precisely the failure pattern that produced the gaps).

Per the durability bet (CONCEPTS "What is durable vs scaffolding"): the framework's primary deliverable is a *specification*. Specifications that define the happy path without naming failure modes produce reference impls that work-until-they-don't, and the don't-work moments require operators to read server logs. This is the bar EU AI Act Article 12 (effective 2026-08-02) makes legally explicit: failure paths must be reconstructable + observable. D45 makes that bar a structural requirement of fresh-plan's spec, not a discipline-honored-by-habit.

D45 is a **meta-foundation entry** — it doesn't itself fix concrete impl. The 5-6 cluster supersedes entries + their impl follow-throughs do the cleanup. D45 is the precondition that makes those entries lockable as standing-pattern applications rather than ad-hoc fixes.

**Cross-references**: D5 (I3 accountability anchor — operationalized by this requirement); D7 (workspace runtime — boot-procedure cluster target); D9 (actor runtime — registration; composes with boot cluster); D10 (event chain runtime — append + integrity; canonical runtime path); D12 + D17 + D43 (substrate runtime — capability vocabulary as runtime contract); D13 (shape runtime — authority check + hooks; subscriber-dispatch cluster + composition-change cluster targets); D16 (adapter runtime — adapter cluster target); D19 (specialist runtime — specialist cluster + subscriber-dispatch cluster targets); D20 (work-unit lifecycle runtime); D29 (extension manifest validation flow — validation cluster target); D30 §4 (per-event runtime checks — validation cluster target); D32 (boot-time resolution — boot cluster target); D34 §A.5 (current-state resolution); D37 (event-driven cross-specialist coordination — subscriber-dispatch cluster target); D39 (state derivation runtime — composition-change cluster); D40 §A (query interface runtime; §B integrity-mechanism extension point); D42 (Bref — this is a Bref deliverable; process-by-pattern revision of the bounded-fill plan); D44 (canonical precedent; sole existing runtime decision honoring the triad; structure template); probing.md (discipline that enforces this requirement; FAILS field amendment + detection-surface-recovery audit shape); 2026-05-12 failure-mode + abandonment-path audit (motivating evidence; 33 SUSPECT findings drive cluster supersedes entries).
