# Decision record: skill trigger convention — concept labels, semantic match

**Status**: ACCEPTED (session 7, 2026-04-29)
**Owner**: `docs/plugin-conventions.md` triggers section; per-skill SKILL.md frontmatter

## Context

Today's `triggers:` field uses a structured form with explicit
language tags:

```yaml
triggers:
  - {phrase: "Mail an UNB aufsetzen", lang: de}
  - {phrase: "Anschreiben für die Stellungnahme", lang: de}
  - {phrase: "draft cover mail", lang: en}
  - {phrase: "Begleitmail", lang: de}
  - {phrase: "transmittal letter", lang: en}
```

Across 19 skills this produces ~3-5 entries per skill, half German
half English, often expressing the same concept. The structured
form suggests deterministic matching against user input, but in
practice triggers feed the LLM's skill-routing decision. The LLM
matches semantically — "Begleitmail" / "transmittal letter" /
"Anschreiben für die Stellungnahme" all map to the same concept
*regardless* of whether all three are listed.

Problems with the current form:

1. **Redundancy** — listing every German+English variant doubles
   the field length without adding routing accuracy. The LLM
   doesn't need exhaustive enumeration to map "Begleitmail" to
   the cover-mail skill.
2. **Bookkeeping debt** — skill authors maintain language-tagged
   pairs by hand; missing pairs feel like coverage gaps when
   they aren't.
3. **False suggestion of determinism** — the structured form
   implies machine-readable routing logic. No such consumer
   exists today; the field is purely LLM-facing.
4. **Wrong abstraction** — the field captures *concepts the skill
   handles*, not *exact phrases users will type*. The current
   form encodes the latter when the former is what matters.

## Decision

**Triggers are concept labels. The LLM matches semantically across
languages. Drop the `{phrase, lang}` structure for a flat list.**

```yaml
triggers:
  - draft cover mail
  - send transmittal
  - Anschreiben aufsetzen     # German technical anchor — kept
```

Rules:

1. **One concept label per concept**, not per language. "draft
   cover mail" covers Begleitmail, transmittal letter,
   Anschreiben für die Stellungnahme — semantically equivalent.
2. **Prefer English for concept labels.** English is the working
   language of skill metadata, ARCHITECTURE.md, decision records.
   Concept labels match that layer.
3. **Keep German technical terms when they're domain-anchors,
   not translations.** UNB, Stellungnahme, Bauleitplanung,
   Aufstellungsbeschluss, Festsetzungen — these aren't
   "the German word for X"; they're domain-specific terminology
   without clean English equivalents in planning law. Listing
   them helps disambiguation.
4. **Don't list every conjugation/inflection.** "Anschreiben"
   covers "Anschreiben aufsetzen", "ein Anschreiben erstellen",
   etc. The LLM handles morphology.

Top of `docs/plugin-conventions.md` triggers section gets a meta-
note:

> Trigger phrases are *concept labels*, not exact-string match
> targets. The orchestrator's skill-routing is LLM-mediated — a
> user typing "schreib mal die Begleitmail an die UNB" routes to
> the skill listing "draft cover mail" without that exact phrase
> appearing in triggers. Add an entry only when the concept itself
> is new or when a German technical term is a domain-anchor (UNB,
> Stellungnahme, Bauleitplan) rather than a translation.

## Rationale

1. **DRY** — typical skill goes from 4-6 triggers to 2-3 concept
   labels. Easier to read, maintain, audit.
2. **Honest abstraction** — the field now describes what it is
   (LLM-routing hints) rather than implying deterministic matching.
3. **Plugin-wide consistency** — same shape across 19 skills.
4. **No regression** — LLM routing accuracy doesn't drop. The
   per-language pairs were redundant anchors for a model that
   already does semantic matching.
5. **Domain technical terms preserved** — German planning-law
   terms stay because they're load-bearing vocabulary, not
   bookkeeping artifacts.

## Alternatives considered

**A. Keep structured form, mandate full bilingual coverage** —
rejected. Doubles the maintenance burden for zero routing benefit.
The LLM matches semantically with or without the explicit pairs.

**B. Drop the field entirely; rely on `description:`** —
rejected. The description field is full-prose explanation; triggers
are scannable concept labels that orchestrator + skill-author can
review at a glance. They serve a different purpose.

**C. Tag German technical terms with `lang: de` to keep
disambiguation signal** — rejected. The flat list is enough; if a
trigger is a German technical term, it reads as such (e.g. UNB,
Stellungnahme). The lang tag is redundant noise.

**D. Programmatic lint that flags missing translations** —
rejected. Would lock in the wrong abstraction; no value for the
LLM-routing consumer.

## Implementation plan

1. **Plugin-wide sweep** (session 7): rewrite all 19 skills'
   `triggers:` lists. Collapse `{phrase, lang}` pairs into concept
   labels. Drop redundant translations. Keep German technical
   anchors.
2. **`docs/plugin-conventions.md`**: add the triggers convention
   section + meta-note above.
3. **Audit consideration**: not a slice. The convention is
   review-driven (skill author follows the conventions doc); not
   automatically detectable as drift since the LLM tolerates the
   old form fine. Future: if drift detection is needed, add as a
   slice 2 sub-check (skill-author convention adherence).

## Revisit triggers

- The orchestrator's `list_skills()` MCP tool grows a deterministic
  matcher consumer (e.g. fuzzy-match user input against trigger
  phrases for routing speed) — at that point, the structured form
  may pay back. Today no such consumer exists.
- A skill's routing accuracy drops in measurable ways after the
  sweep (false negatives where the orchestrator routes wrong).
  Expected to be near-zero given semantic matching.
- A non-LLM-mediated workflow needs to read trigger phrases
  (e.g. CLI help generation, IDE plugin). Different consumer →
  may motivate richer structure.

## Files touched

- `plugin/skills/*/SKILL.md` — all 19 `triggers:` lists
- `docs/plugin-conventions.md` — new triggers section

---

## Session-11 retroactive review note (v0.21 — make wrong shapes impossible discipline)

This decision is a worked example of the discriminator working
in the **opposite direction** from typical applications: triggers
are AI-applied (LLM-mediated routing decisions), NOT
gate-dispatched. Per the discriminator: prose convention is
correct; structural enforcement (the prior `{phrase, lang}` form)
would be SQL-DB-trap-style over-structuring for an AI-applied
concern.

When v0.21 was named (session 11), this decision was already
in place; the discipline retroactively validates the concept-
labels-as-prose direction.

This pairs with `mcp-fallback-policy.md` (same-day session-7
decision) which goes the OTHER direction — fail-closed structural
enforcement for gate-dispatched concerns. Together they cover
both halves of the discriminator: prose convention where AI
applies; structural enforcement where gate dispatches.
