# review-draft — layered review workflow

Detailed Layer 1 / 2 / 3 procedure for the A/B/C-categorized review
pattern. Loaded by SKILL.md when this skill is active.

## Layer 1 — Structural (validate-checklist delegation)

### Entry condition

Compile_latex passed (Compile Gate 4.1). If not, refuse to review.

### What's checked

Delegated entirely to `validate-checklist` skill, which loads the
relevant doctype checklist:

- b-plan-begruendung.md — for Begründungen
- b-plan-festsetzungen.md — for Festsetzungen
- umweltbericht.md — for Umweltberichte
- gutachten-generic.md — fallback for Gutachten

Returns severity-rolled findings:

- `required_missing` — block-level
- `expected_missing` — warnings
- `optional_missing` — informational
- `unfilled_placeholders`
- `header_mismatch`
- `package_violations`

### Per-finding handling

For each finding, surface with spec reference and ask:

```
[REQUIRED] L42: Section "Geltungsbereich" not found
            (b-plan-begruendung.md §canonical-sections, item 4)

→ fix-now / defer / accept-with-reason / drop
```

Block layer transition until all `required_missing` resolved.

### Layer-1 verdict

```
Layer 1 result:
  N required-missing items → resolved (fixed | deferred)
  M expected-missing items → resolved
  K cross-check failures → resolved

PASS / BLOCK at level 1.
Proceeding to Layer 2 fachlich? [y/n]
```

## Layer 2 — Fachlich (manual + verify-citations delegation)

### Entry condition

Layer 1 passed (no `required_missing` outstanding).

### What's checked

Substantive content correctness. Per-section walk:

1. **Claims grounded in inputs** — every factual claim about the
   project (Geltungsbereich-Größe, Bestandsfunde, technische Daten)
   must trace to an input file or referenced past project. Surface
   ungrounded claims.

2. **Legal citations grounded in references** — delegate to
   `verify-citations` for every `§ X Y`, `Art. Z`, `BVerwG ...`,
   `EuGH ...` reference. Drift / missing → finding.

3. **Internal consistency** — Begründung argumentation must align
   with Festsetzungen rules (when both available). Contradictions
   surface.

4. **Section-content completeness vs context** — for each section,
   identify required elements per the doctype's typical scope:

   For Begründung sections:
   - Aufstellungsverfahren — references state.md.phase + bauleit-
     planung-phasen.md correctness
   - Geltungsbereich — references vermessung input + state.md.geltungs-
     bereich values
   - Planinhalte und Festsetzungen — narrative MUST mirror Festsetzungen
     content (cross-document)
   - Eingriffs-Kapitel — must show §44 BNatSchG-tatbestand-Prüfung
     wenn relevant
   - Alternativprüfung — must show actual alternatives considered, not
     just declarative "keine Alternative"
   - Stand des Aufstellungsverfahrens — must align with state.md.
     phase_history

5. **A/B/C taxonomy from transcript pattern**:
   - **A** — Fachlich-inhaltlich offene Punkte (substantive content
     gaps; the meat of fachlich review)
   - **B** — Formal-strukturelle (mostly Layer 1 already; redirect)
   - **C** — Juristisch kritische Kernstellen (e.g. §45-Ausnahme-
     argumentation, FFH-Vorprüfung-Erheblichkeit, Eingriffs-Bilanz)

6. **Deepening (mandatory)** — each finding traces implications:
   - "Missing FFH-Vorprüfung" → adjacent: does §44-Prüfung in Eingriffs-
     section reference FFH-impact correctly? Does Schutzgut Tiere/
     Pflanzen in Umweltbericht reflect FFH-relevance?
   - "Citation drift on BNatSchG" → adjacent: are other BNatSchG
     references in document also stale?

### Per-finding handling

```
[A2] L168: §45 Abs.7 Nr.5 argumentation uses Innenbereichssatzung
     alone. UNB Rostock previously rejected this pattern (see
     memory/universal/artenschutz/feedback/2026-04-28-...).
     Suggested fix: combine with §1a Abs.2 BauGB-Bezug.
     Implications: Festsetzungen rule on Folgenutzung may need
     §1a-reference too.

→ fix-now / defer / accept-with-reason / drop
```

For C-class findings (kritische Kernstellen), suggest extra
scrutiny: external review or Claude Opus pass on the specific
section.

### Layer-2 verdict

```
Layer 2 result:
  A. <N> substantive findings → <breakdown>
  C. <M> juristisch critical → <breakdown>

PASS / WARN at level 2 (no block; Layer 2 is judgmental).
Proceeding to Layer 3 formal? [y/n]
```

## Layer 3 — Formal (validate-latex-style + verify-citations + korrektur)

### Entry condition

Layer 2 acknowledged (findings handled or deferred with reason).

### What's checked

1. **Style-spec compliance** — delegate to validate-latex-style.
   Document class, packages, geometry, headers, fonts, number
   formatting all match spec.

2. **Korrektur-rules compliance** — manual sweep:
   - German quotes `\glqq...\grqq{}`
   - Non-breaking spaces `~` before units, `§`, currency, dates
   - German number format (comma decimal, dot thousands)
   - Long compound hyphenation
   - Source line wrap ~80 chars
   - Lists in itemize/enumerate environment

3. **Citation freshness** — delegate to verify-citations. All cited
   amendment dates must be current.

4. **Section-level edits**:
   - Findings batched by section.
   - Apply via Edit tool (NOT whole-document Write).
   - Per orchestrator Validation 7.3: produce explicit diff summary
     after edits.

5. **Final compile** — Layer 3 done compile_latex must pass with no
   new warnings introduced.

### Per-finding handling

```
[FORMAL] L267: BNatSchG i.d.F. ...08.12.2022 → DRIFT to 23.10.2024
[FORMAL] L142: "Regiosaatgut" → \glqq Regiosaatgut\grqq{}
[FORMAL] L155: 5 m → 5~m

Apply all formal fixes? [y/n] (typically batched fix without
per-item review)
```

### Layer-3 verdict

```
Layer 3 result:
  Style: 1 fix (header text)
  Citations: 1 drift fixed (BNatSchG 2024 amendment)
  Korrektur: 12 fixes batched (4 quotes, 6 nbsp, 2 numbers)

Final compile: PASS.
Section-level diff: changed 4 sections; 13 files unchanged.

Review complete.
```

## End-of-review handoff

When all three layers pass:

1. Final compile_latex passes.
2. Call `update_project_state(project, updates={"lifecycle": "ready-for-phase-C"}, body_append="- <YYYY-MM-DD> — Layered review passed; ready for Phase C.")`. Never write state.md directly (meta-rule 4).
3. Append `_ai/decisions.md` entries for:
   - Each Layer 2 A-finding fixed (with reasoning summary)
   - Each Layer 2 C-finding flagged for external scrutiny
   - Each deferred finding (with reason)
4. Hand to orchestrator for Phase C entry (send-gate, snapshots,
   draft-cover-mail).

## What not to do

- **Don't run all three layers as one pass**. Layers are sequential
  with user pause between each. Bundling them violates the framework.
- **Don't auto-apply A or C findings without user decision**. Only
  Layer 3 formal fixes (style, korrektur, citations) can be batched
  with user "yes apply all" approval.
- **Don't whole-document rewrite**. Section-level edits only
  (Validation 7.3 invariant).
- **Don't skip verify-citations** in Layer 2 or 3. Source-grounding
  guard requires it.
- **Don't claim "review complete" if any required_missing remains
  unresolved** from Layer 1. Block.
