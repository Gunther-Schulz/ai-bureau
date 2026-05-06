# Findings from PBS deployment

Aggregator for PBS-deployment findings that touch framework concerns. Lock context: see `LOCKED-STATE.md`.

## Purpose

This file is the evidence pool that reopen criteria fire against (per `LOCKED-STATE.md` reopen criteria). Every PBS deployment finding that touches framework gets logged. Even findings we do not act on (we will not, during lock). The log IS the evidence.

## Per-finding format

Per finding, add an entry below using this template. Either author the entry directly here OR author it in the PBS-deployment repo and add a pointer entry here.

```yaml
---
date: YYYY-MM-DD
short_name: kebab-case-summary
framework_area: shape | specialist | workspace | adapter | audit | substrate | sparring | quality-gate | authority-binding | claim | scope-model | practitioner | other
severity: blocking | workaround-acceptable | annoyance | observation
related_questionable_point: LOCKED-STATE.md §N | none
deployment_repo_link: <link to PBS-deployment repo file if applicable>
---

## Finding

[Plain-language description of what surfaced during PBS deployment.]

## Why it touches framework

[Which framework area + why current architecture does not handle this cleanly.]

## Current workaround

[What we did in PBS-deployment to ship around it; or "no workaround possible — blocking".]

## Reopen-trigger relevance

[Does this contribute to a reopen trigger? Which one (A/B/C/D per LOCKED-STATE.md)?]
```

## Severity definitions

- **blocking**: PBS deployment cannot proceed without framework change. Triggers reopen consideration on accumulation (per Trigger B threshold below).
- **workaround-acceptable**: PBS works around it; framework gap noted for later. Common case during lock.
- **annoyance**: minor friction; framework gap noted; low priority.
- **observation**: pattern observed; not yet a gap; might become one later.

## Trigger B threshold

Per `LOCKED-STATE.md` Trigger B: **≥5 findings of severity `blocking`** triggers reopen consideration. Counts only blocking-severity findings, not all findings. Workaround-acceptable + annoyance + observation findings do NOT count toward threshold but are tracked for pattern analysis at reopen review.

## Findings (chronological)

### 2026-05-06 — m1-api-friction (workaround-acceptable)

**Framework areas**: audit, substrate.
**Repo link**: `pbs-dep-1/findings/2026-05-06-m1-api-friction.md`
**Summary**: Three small API friction points surfaced wiring up Hello PBS: (1) `AuditShapePolicy` exported from impl module, not Surface module; (2) `audit.audit_storage_ready` vs substrate's `is_ready` inconsistency; (3) `audit.emit()` sync surprise vs surrounding async wiring. All workaround-acceptable; M1 ran cleanly after adjustments. Worth bundling with future API-cleanup findings.
**Reopen relevance**: none directly.

## Severity tally (auto-tracked at reopen review; manually-updated for now)

- blocking: 0 / 5 (Trigger B threshold)
- workaround-acceptable: 1
- annoyance: 0
- observation: 0
