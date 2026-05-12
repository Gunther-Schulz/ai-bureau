# D49 — 2026-05-12 — Clarifies D47 §C + §D + D48 §B.2 — sharpen-surfaced corrections (step-count + missing handler-index defer + Recovery-row wording)

**Decision (clarifies D47 §C bullet 6 + D47 §D + D48 §B.2)**: Three sharpen-surfaced corrections to locked entries D47 + D48 land here per append-only ledger discipline (locked entry text stands; this clarification entry carries the corrections). 2026-05-12 sharpen sweep dispatched via sub-agent on D47 + D48 surfaced multiple findings; the three below are the load-bearing fixes (factual error + contract gap + cold-read ambiguity affecting contract clarity). Remaining wording-polish findings logged-and-accepted per cost/benefit (cumulative ledger-load not justified for cosmetic-tier corrections; original entries' bodies carry the load-bearing semantics correctly).

### A. D47 §C bullet 6 step-count correction (factual error)

D47 §C bullet 6 reads: "update `substrate.py append_event` docstring to enumerate the **7 ordered steps** including hook-firing positions." The actually-locked impl docstring (`substrate.py:165-179`) enumerates **9 ordered steps**:

1. per-event identity check (D30 §4 + D34 §A.5)
2. shape authority check (D13)
3. pre-event-emit hook fire (D47 §B.2)
4. event_chain.append (D10)
5. projection (D39)
6. enqueue for dispatch (D44 queued FIFO)
7. post-event-emit hook fire (D47 §B.2)
8. (outer call only) drain queue
9. (outer call only) raise aggregated SubscriberDispatchError + HookExecutionError

The entry's "7" was pattern-completed (likely from a draft before the impl docstring expanded to include drain + aggregated raise as explicit numbered steps); impl is canonical at 9.

**Correction**: D47 §C bullet 6's "**7 ordered steps**" → **9 ordered steps** per `substrate.py:165-179`. Future readers cross-referencing D47 against impl should expect 9 not 7. This is the failure-mode probing.md's investigation-before-claim discipline targets — the discipline was itself motivated by D47 §B.3 `HookRegistry.fire` confabulation; the §C step-count slipped through the same authoring window. Lesson: pre-lock probe (skipped per D45 §E precedent at D47 lock-time; would have fired per D48 §E refined skip rule) was the missing gate.

### B. D47 §D missing handler-index defer (contract gap)

D47 §D enumerates seven explicit deferrals. The impl at `substrate.py:240-246` post-emit hook handler capture uses sentinel `handler_index=-1` because `HookRegistry.fire` iterates handlers serially and only the first-raising handler's exception surfaces from the catch site. The impl comment (`substrate.py:243`) explicitly states: "Future probing audit may surface this as a gap; **acceptable for Phase B impl per D47 §D**." **But D47 §D does not actually carry this defer.** Discipline-cited-as-label-not-applied-as-check pattern — the impl points at §D as the disposition; §D is empty there.

**Correction (extends D47 §D)**: add the following defer to D47 §D's enumerated list:

- **No handler-index in `_post_emit_failures` capture**. `HookRegistry.fire` iterates handlers serially; on first handler raise, subsequent handlers in the same `fire()` call are not invoked, and the catch site does not know which handler index raised. Capture uses sentinel `handler_index=-1` (= first-raising in registration order). Future D-entry may lock per-handler isolation (re-fire from N+1 to capture downstream failures; or restructure `HookRegistry.fire` to iterate from catch site) if shape policy or audit-grade observability needs it; not in scope here.

Surfaced by post-hoc sub-agent sharpen pass on D47; D45 §E skip precedent followed in good faith at D47 lock-time; D48 §E refined skip rule (probing.md Procedure 3) postdates D47 and would have caught this gap pre-lock had D47 fired the probe.

### C. D48 §B.2 Recovery row wording (cold-read ambiguity affecting contract clarity)

D48 §B.2 Recovery row currently reads: "For Phase B stubs no failure mode exists; the wrapping is defensive for Phase C+." The phrase "no failure mode exists" reads as "no wrapping" — but the wrapping IS active (and verified by the `test_adapter_attach_failure_surfaces_as_workspace_boot_error` test in commit `ae4bb81`). Phase B stubs cannot TRIGGER the wrapping because attach is trivial assignment, but the wrapping itself is in place + exercised by a monkeypatched-subclass test.

**Correction**: D48 §B.2 Recovery row reads: "Phase B stub attach is trivial (cannot fail in normal operation); the wrapping is active + verified by monkeypatched-subclass test (`test_adapter_attach_failure_surfaces_as_workspace_boot_error`); Phase C+ real-wire attach work (connection-pool setup / auth handshake / pre-flight) inherits the surface. Boot is aborted per D46 §B.2 partial-and-discardable semantics: substrate object exists with partially-bound adapters (0..idx-1 attached; idx..N not attached); `Workspace` handle is NOT returned (the `WorkspaceBootError` raises before `return workspace` at `boot.py:365`). Phase C+ real-wire substrates SHALL define teardown semantics on partial-attach failure (e.g., closing connection pools of already-attached adapters)."

### What is NOT corrected (logged-and-accepted)

The 2026-05-12 sharpen sweep surfaced additional findings on D47 + D48 that are NOT corrected here per cost/benefit assessment (wording-polish doesn't justify cumulative ledger-load; corrections logged in sub-agent reports + commit messages + JOURNAL.md as discipline-effectiveness data points):

- **D47 F1** — §B.2 / §C "after subscriber-dispatch enqueue" cold-read ambiguity (reads as "after subscribers dispatched"; actual semantics "after queued, before drain"). §B.2 "Why synchronous at append" paragraph carries the explicit semantics; substance is correct.
- **D47 F3** — cluster cardinality "3 SUSPECTs" when honest count is "2 SUSPECTs + 1 derived gap (A.3 downstream of A.2)." §A.3 body itself acknowledges the downstream relationship; framing inflates by counting derived gap as third SUSPECT.
- **D47 F5** — §E pre-lock probe skip is rationale-after-the-fact given D48's later refined skip rule would have required probe. Ledger history; D45 §E precedent followed in good faith at D47 lock-time.
- **D48 F1** — opening paragraph "(adjacent cleanup; not in D45 §C ...)" contradicts §A.3 body's "D45 §C item 3 originally surfaced this case." §A.3 body carries the honest framing.
- **D48 F4** — §C bullet 4 documents both options + the lean ("leave bare"); impl chose "leave bare." Bullet stands as documented design decision (non-action with rationale rather than action item).

**Rationale**: append-only ledger discipline means locked entries stand. Sharpen-surfaced corrections warrant clarification entry only when load-bearing — factual errors (§A); contract gaps (§B); ambiguity affecting contract clarity (§C). Cosmetic-tier corrections accumulate ledger-load without commensurate benefit; the original entries' bodies carry the load-bearing semantics correctly; future readers cross-referencing the impl + the entries together get the canonical picture once D49's three corrections are applied.

The discipline-effectiveness lesson — pre-lock probe firing catches what skip misses — is the forward fix (probing.md Procedure 3 refined skip rule + D48 §E precedent); D49 doesn't try to retroactively re-author D47 or D48. The sharpen sweep itself (sub-agent dispatch on locked entries) is a post-hoc analogue to pre-lock probe — useful when applied to entries whose lock-time skipped probing, but no substitute for catching issues pre-lock.

**Cross-references**: D44 (queued FIFO dispatch — the 9-step ordering in `substrate.py:165-179` honors D44 + D47); D45 (canonical citation for cluster supersedes pattern; D47 + D48 are second + third cluster supersedes; §E pre-lock probe skip precedent); D46 (first cluster supersedes; structural template D47 + D48 followed); D47 §C bullet 6 (corrected here per §A); D47 §D (extended here per §B); D47 §E (skip precedent followed at lock-time; refined retrospectively by D48 §E); D48 §B.2 Recovery row (clarified here per §C); D48 §E (refined skip rule that would have caught D47 §C + §D gaps if D47 had run pre-lock probe); probing.md §"Investigation-before-claim discipline" + §"Pattern-completion over pattern-questioning" failure mode + Procedure 3 refined-skip rule (the discipline frame for these corrections); 2026-05-12 sharpen sweep on D47 + D48 (sub-agent reports surfaced these findings; logged in commit message ae4bb81-onwards + dotfiles JOURNAL.md as discipline-effectiveness data points).
