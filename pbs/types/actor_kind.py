"""ActorKind enum — framework-level actor typing for AuditEvent attribution.

Per `glossary/actor.md` + `glossary/authority-binding.md`: every AuditEvent
declares its emitting actor's kind. The enum lives at framework-mechanism
level; specific actor records live as workspace-scope managed entities at
Owner B (per `glossary/owner-b-scope.md`).

Three framework-baseline values (`glossary/actor.md` "What it is"):

- HUMAN — practitioners; legal/professional accountability moments
  (signature_applied; per-claim attestation events)
- AI_RUNTIME — substrate's running Instance; skill emissions; sparring
  rounds; production-phase engagement attribution. Deliberately NOT
  named `skill` per `glossary/actor.md` "Naming note" (avoids collision
  with `skill` primitive vocabulary).
- EXTERNAL — events arriving from outside the workspace (A2A peers;
  external system integrations; events that did not originate in the
  workspace's own substrate Instance).

Per-shape policy bundles MAY extend the enum surface (per `arch/audit.md`
§5 per-shape policy mechanics) — extension is reserved for evidence-driven
v1.x amendments per `MAINTENANCE.md` v1.x amendment cadence.
"""

from enum import StrEnum


class ActorKind(StrEnum):
    """Framework-level actor type per `glossary/actor.md`.

    Used as the `actor_kind` field on every AuditEvent (per `arch/audit.md`
    §2.A emission API + `glossary/authority-binding.md` per-event actor
    declaration).
    """

    HUMAN = "human"
    AI_RUNTIME = "ai_runtime"
    EXTERNAL = "external"
