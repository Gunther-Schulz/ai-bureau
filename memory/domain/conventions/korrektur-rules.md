# Korrektur rules — PBS LaTeX writing conventions

The legacy `korrektur-prompt.txt` in existing project repos lists 13+
rules that were prompt-engineered for older LLMs needing step-by-step
guidance. Most of those (basic spelling, grammar, UTF-8 verification,
math forms, citation/figure label correctness) are reflexive for current
models and don't need to be stated.

What follows is the **office-specific** subset that captures actual
PBS conventions a model would otherwise miss or get wrong.

## 1. German quotation marks

Always use `\glqq` and `\grqq` — never straight `"` or fancy `“ ”`.

```
"Regiosaatgut"           →  \glqq Regiosaatgut\grqq{}
"extensive Bewirtschaftung"  →  \glqq extensive Bewirtschaftung\grqq{}
```

Append `{}` after `\grqq` when followed immediately by text or
punctuation, to avoid space-eating.

## 2. Non-breaking spaces (~)

Use `~` (tilde) instead of regular space in these patterns to keep the
two parts on the same line:

| Before | Pattern | Example |
|---|---|---|
| Units | `<number>~<unit>` | `5~m`, `100~ha`, `30,37~ha` |
| Currency | `<number>~<symbol>` | `10~€`, `2.500~€` |
| Legal refs | `§~<num>` | `§~9 BauGB`, `§~44 Abs. 1 Nr. 1 BNatSchG` |
| Article refs | `Art.~<num>` | `Art.~16 FFH-RL` |
| Date day | `<day>.~<Monat>` | `1.~Juli`, `15.~März 2026` |
| Abbreviations | `i.~d.~F.`, `z.~B.` | (use sparingly; usually unhyphenated forms also acceptable) |

## 3. Numbers in tables vs prose

- **Tables:** use `siunitx` — `\num{30370}` renders as `30.370` (German
  thousands), `\num{30,37}` renders as `30{,}37`. The preamble already
  configures `output-decimal-marker={,}, group-separator={.},
  group-minimum-digits=4`.
- **Prose:** German format directly (decimal comma, thousands dot for
  ≥4 digits). Use `~` before units. Example: `30,37~ha`, `1.250~m²`.

For squared/cubed units in prose: `m$^2$`, `m$^3$`, `CO$_2$`. Inside
siunitx contexts these render automatically; outside, manual is fine.

## 4. Compound-word hyphenation (German)

LaTeX often breaks long compounds badly. Two ways to help:

- **Preamble hyphenation hints** for a closed list of words:
  ```latex
  \hyphenation{
    Na-tur-schutz-aus-füh-rungs-ge-setz
    Bun-des-na-tur-schutz-ge-setz
    Photo-vol-ta-ik-frei-flä-chen-an-la-ge
  }
  ```
- **In-source hints** with `\-` for one-off cases:
  `Photo\-voltaik\-frei\-flächen\-anlage`

Don't aggressively hyphenate everything. The Begründung preamble uses
relatively soft penalties (`\hyphenpenalty=50, \exhyphenpenalty=50`)
that allow LaTeX's natural breaking; only intervene when output looks
genuinely bad.

## 5. Source line wrapping (~80 chars)

Wrap LaTeX source at ~60–80 characters per line for diff-friendliness.
Break at natural punctuation/clause boundaries, not arbitrarily.

This is purely a source-readability preference. It does not affect
output (LaTeX collapses runs of whitespace).

```
% bad: one giant line
Die Zwischenmodulflächen sowie die von Modulen überschirmten Flächen werden mit autochthonem, kräuterreichem Saatgut eingesät. Bodenbearbeitung ist untersagt.

% good: clause-aligned breaks
Die Zwischenmodulflächen sowie die von Modulen überschirmten Flächen
werden mit autochthonem, kräuterreichem Saatgut eingesät.
Bodenbearbeitung ist untersagt.
```

## 6. Preserve as-is

Do not touch:
- Legal citations (BauGB, BNatSchG paragraphs as written, even if
  formatting looks off — they may be officially correct)
- Quoted text from external sources (even if quoting style differs from
  PBS conventions)
- LaTeX commands and their arguments
- Specialized technical terms (Hochspannungsfreileitung, Solartracker,
  Wechselrichterstation — leave intact even if hyphenation feels weird)

## 7. Lists from prose

When source has dash- or bullet-led list content as plain prose,
convert to `itemize`:

```
% before
Zulässig sind: - PV-Module, - Trafostationen, - Wechselrichter.

% after
Zulässig sind:
\begin{itemize}[leftmargin=*]
  \item PV-Module
  \item Trafostationen
  \item Wechselrichter
\end{itemize}
```

The Festsetzungen heavily nest `enumerate` for the binding-rules
structure; preserve that pattern when writing new rules.

---

## What's intentionally left out (vs legacy korrektur-prompt.txt)

The old prompt also instructed:
- Basic spelling/grammar correction → modern LLMs do this without being told
- UTF-8 encoding verification → not a writing rule, a build-environment concern
- Generic LaTeX form (math, headings, figures, citations, references) →
  general LaTeX literacy expected
- Heading consistency, label uniqueness → caught at compile-validation time

These weren't wrong, just verbose for the prompt-style they targeted.
Our orchestrator's review-draft skill assumes general LaTeX competence
and only enforces the office-specific points above.
