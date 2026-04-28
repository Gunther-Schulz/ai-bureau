---
name: draft-cover-mail
description: This skill should be used to draft a transmittal cover mail (Anschreiben) when sending project artifacts to authorities (UNB, Behörden, höhere Verwaltungsbehörde) or clients. Triggered as part of orchestrator's send gate (Checkpoint 4.3), or by direct user phrases like "Mail an UNB aufsetzen", "Anschreiben für die Stellungnahme", "draft cover mail", "Begleitmail", "transmittal letter".
version: 0.1.0
license: MIT
---

# draft-cover-mail

Specialist skill for drafting transmittal cover mails when artifacts
go out to authorities or clients. Phase-aware; tone calibrated by
prior correspondence.

## Load this now

Read `<repo>/memory/universal/verfahren/bauleitplanung-phasen.md` for
phase-appropriate language and the Verfahrensvermerke context.

Load `office_config` for office identity and signature: `office.name`,
`identity.address_lines`, `identity.signature_block`,
`identity.phone`, `identity.email`. The signature block is inserted
verbatim at the end of the mail; identity fields populate header
metadata if needed.

If the project has prior correspondence with the recipient, scan
`<project>/_ai/correspondence-log.md` for tone calibration —
established contacts use collegiate style, new contacts use formal.

## When invoked

By orchestrator's send gate, or by direct user request. Inputs:

- **Project** — project ID; loads state.md context.
- **Recipient** — authority/contact name. If `contact` field is set
  in correspondence-log → use collegiate. If not → formal.
- **Phase** — current Bauleitplanung-phase. Determines what's being
  sent and what mail content is appropriate.
- **Artifacts being attached** — list of files. The mail summarizes
  what's enclosed.
- **Specific points to flag** — anything the recipient should pay
  attention to (open questions, deviations, etc.).

## Behavior

1. **Detect tone**:
   - Established contact (prior correspondence ≥ 3 in log) →
     collegiate.
   - First contact → formal.
   - Override per user request.

2. **Detect language**:
   - Default from `office_config.office.language` (currently always
     `de_DE`). All German-deployment correspondence is in German.
   - English only on explicit user override (rare; only for non-
     German-speaking authorities).

3. **Compose by phase**:

   - **Phase 0-3 (frühzeitige Beteiligung)**: introduction of
     project, scope of frühzeitige Unterrichtung/Beteiligung, no
     formal request for a Stellungnahme but invitation to comment.

   - **Phase 4-5 (Auslegung + förmliche Beteiligung)**: formal
     Aufforderung zur Stellungnahme nach §3 Abs.2 / §4 Abs.2 BauGB
     with Frist (per §4 Abs.2: mind. 1 Monat / 30 Tage).
     Reference Auslegungs-Bekanntmachung if applicable.

   - **Phase 6-7 (Abwägung / erneute Auslegung)**: response to
     received Stellungnahme + Mitteilung des Abwägungsergebnisses,
     OR Aufforderung erneuter Stellungnahme im verkürzten Verfahren.

   - **Phase 9-10 (Satzungsbeschluss → Genehmigung)**: Antrag auf
     Genehmigung der Satzung an höhere Verwaltungsbehörde.

   - **Phase 12 (Bekanntmachung)**: rather Bekanntmachungstext;
     usually no separate cover mail.

4. **Structure**:
   - Subject line: `<Projekt-Kurzform> — <Phase-Anlass>`
     Example: "<BPlan-Name> — Stellungnahme §4 Abs.2 BauGB"
   - Salutation matched to tone.
   - Opening paragraph: project context (one sentence).
   - Body: what's being sent + why + key points + Frist (if applicable).
   - Specific items the recipient should pay attention to (from input).
   - Closing: anbieten Rückfragen / Telefonklärung / weiterer
     Austausch.
   - Signature: insert `office_config.identity.signature_block`
     verbatim. If the active practice has its own
     `practices[].signer` set, prepend the signer's name above the
     signature block.

5. **Reference attachments** in body and list at end.

6. **Do NOT actually send** — output the draft for user review. Send
   gate (orchestrator Checkpoint 4.3) handles the actual transmission
   only after user explicit confirm.

## Output

Plain text draft (mail format), ready to copy-paste into the office's
mail client. Headers as the start of the draft, body follows,
signature at end. No markdown formatting in the mail itself
(LaTeX-style markup not needed for mail).

## Edge cases

- **No prior correspondence with recipient AND no formal context**:
  default formal salutation. Note in output that tone may be
  adjustable.
- **Multi-practice project**: signature includes both practices' signers
  if appropriate (e.g. for joint Gutachten signed by multiple practices).
  Pull each signer from the relevant entry in `office_config.practices`.
- **Late response to received Stellungnahme**: tone needs explicit
  acknowledgment of late response; suggest user verify Frist
  passed before sending.
- **Recipient on personal vs office basis** (e.g. Bürgermeister
  privat vs amtlich): use amtlich form by default; flag if user
  explicitly wants Privatname tone.

## Tools used

- `Read` — project state, correspondence log.
- Office identity values come from `office_config` (in-memory),
  not from any markdown file.
- `Grep` — search prior mail for tone calibration.
- No MCP backend dependency for drafting (the send action itself is
  separate).
