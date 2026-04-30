# What PBS-bureau is, in plain terms

PBS-bureau is an experiment: build an "AI office" — a coherent
infrastructure where AI is a co-worker in the actual production
of expert knowledge work, not a feature bolted onto unchanged
workflow. The pioneer instance is a German planning bureau
(Planungsbüro), but the architecture is meant to generalize to
any expert-practitioner domain — law, research, accounting,
healthcare, consulting, and so on.

## What we want

The infrastructure should be:

- **Portable across industries** — same architecture, different
  domain prose; not locked to one industry shape.
- **Customizable by domain experts** — not requiring engineers
  for every deviation.
- **Simple enough to maintain** — not a low-code platform where
  every customization becomes config archaeology.

## What existing approaches do

Most existing infrastructure for office work makes one of a few
trade-offs. A rough survey:

| Product | Portable across industries | Customizable | Simple |
|---|---|---|---|
| Salesforce / SAP | partial (industry modules each separate) | yes (within domain) | no (certifications exist) |
| BPMN engines (Camunda) | yes | yes | no (specialists required) |
| Low-code (Mendix, Retool) | claim yes; real for narrow problem shapes | yes | yes for toys, no at scale |
| Django / Rails | yes | yes (for developers) | yes (for developers) |
| Notion / Airtable | yes | yes | yes at small scale; hits ceiling |
| Excel + macros | yes | yes | yes at small scale; breaks at office-coordination scale |

Each succeeded in its niche by making a specific trade-off (the
table makes the trade-off concrete per category). None hits all
three of what we want at once, at office scale, by domain
experts. Whether all three are achievable together is an open
empirical question, not a settled one.

## What LLMs change

LLMs introduce a new option that wasn't available when the
existing categories were built: **prose can be a viable config
language**. Not "AI-assisted config editing." Not "AI generates
code." Something more direct: write the rules of your domain in
prose, store them alongside the data, and let the AI read them
at runtime when it needs to act.

This suggests a different layering:

- **Structured layer** (small, stable, type-checked): identity,
  persistence, machine contracts, interfaces. The deterministic
  part. Things code needs to do reliably.
- **Prose layer** (larger, evolving, AI-read): domain semantics,
  conditional rules, process descriptions, the texture of how
  this office actually works. The non-deterministic part —
  interpreted by a runtime (the AI) that handles ambiguity
  natively.

The AI is the **runtime that fuses the two at use-time**, not a
translation layer between them. No translation layer means no
config-DSL to maintain — but prose interpretation depends on the
AI runtime, so model-version stability and consistency become
their own maintenance concerns. Different cost shape, not zero
cost.

This is the architectural bet. If it holds, the trade-off shape
of the three-way changes: structured stays small (simple), prose
carries domain shape (portable), AI runtime makes prose
actionable (customizable by non-engineers). Same framework,
many domains — with the per-domain customization happening in
markdown rather than YAML or code. Whether that combination is
maintainable at office scale is the empirical question.

## What integrating this looks like for a company

The shift, concretely:

- **Existing infrastructure stays.** Lexware for invoicing,
  Harvest for time-tracking, Salesforce for CRM, whatever's
  already in place. AI becomes the connective tissue across
  them, not a replacement for them.
- **The texture of how YOUR office actually works — rules,
  exceptions, conventions, the things that make you different —
  lives in prose alongside the data.** Domain experts edit it
  directly. Engineers aren't gatekeepers for every customization.
- **AI participates in actual work production** — drafts,
  reviews, decisions, with audit trail for accountability —
  rather than as discrete bolt-on features ("summarize this
  email," "generate that section").

Different addressable space than vertical-SaaS plays. Not "switch
to our system." Coordination layer, with AI as connective tissue
shaped by the prose your domain experts already think and write
in.

If the bet holds, the same architecture transfers across domains:
same shape, different prose. That's where this stops being one
bureau's tool and becomes a pattern other companies can adopt.
