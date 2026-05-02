# Profile L5g: Medical practitioner — solo private practice

**Status: PRELIMINARY — skeleton (full content TBD)**

**Lifecycle stage**: L5 (practitioner-user)
**Shape variation**: practitioner-shape
**Archetype**: medical practitioner (clinical case work)
**Scale**: solo (single physician private practice)

## Identity + context

Solo physician at private practice. Clinical case work: patient encounters, diagnosis, treatment planning, case notes, prescriptions, referrals. Produces accountability-bearing clinical documentation under HIPAA (or jurisdictional equivalent), medical-board oversight, malpractice scrutiny.

Adds **privacy-as-architectural-constraint** dimension that other practitioner-shape profiles don't fully cover. PHI (protected health information) handling is a hard constraint at framework level.

## What this profile is intended to EXEMPLIFY

This profile stress-tests:
- **Privacy-as-architectural-constraint**: HIPAA / GDPR-medical / jurisdictional equivalent — patient data handling is non-negotiable architectural requirement
- **Per-claim defensibility under medical-board scrutiny**: diagnosis, treatment-justification, prognosis claims defensible
- **Case-note documentation discipline**: per-encounter audit-trail; legal-medical record requirements
- **Differential-diagnosis documentation**: claim-level reasoning capture (why this diagnosis vs alternatives considered)
- **Real-time clinical decision support** (vs after-the-fact drafting): AI engagement during encounter possibly relevant
- **Long-arc patient relationship**: same patient visits over years; cross-encounter context; longitudinal clinical record
- **Multi-practitioner data flow**: referrals + consultations; PHI sharing with consent; cross-provider coordination
- **Emergency-time pressure**: critical decisions; rubber-stamping risk under emergency
- **Litigation defensibility**: malpractice scenarios test six-months-later claim defensibility

## Packaging boundary section

n/a — L5 profile.

## TBD sections (full content)

- Day-in-the-life / usage flow (typical clinic day; encounter cycle)
- Hybrid moments (codified encounter workflow + ad-hoc differential-diagnosis exploration + emergency-decision)
- Capability composition (medical-practitioner-specialist + specialty-specific specialists + jurisdiction-specific Layer A)
- Multi-user moments (referrals; consults; office staff; mostly solo for clinical decisions)
- Edge cases (HIPAA breach scenarios; malpractice claim; medical-board investigation; emergency cases without time for engaged-authorship)

## Status

PRELIMINARY — skeleton. Full content drafted in subsequent session(s). Privacy-as-architectural-constraint surfaces concerns potentially affecting framework primitives (workspace privacy boundaries; per-entity privacy classification; cross-deployment data-flow rules).
