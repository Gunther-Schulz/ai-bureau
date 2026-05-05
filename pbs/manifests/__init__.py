"""Mode 3 spec-layer manifests — Pydantic descriptor schemas.

Per `ARCHITECTURE.md` §6 Logic placement modes Mode 3: typed contracts that
the framework + reference impls validate against. Per `MAINTENANCE.md`
TOP-LEVEL SCOPE: instance-content authoring (per-deployment specialist /
practitioner / workspace / workflow / work-unit / claim entity-md files)
NEVER lives in this repo — these schemas describe the SHAPE of those
manifests, not the manifests themselves.

Phase 6.1 batch 6 covers all four primitive-cluster ARCH topics + scope-
model workspace.md schema:

- `specialist` — SpecialistDescriptor + SkillDescriptor per `arch/
  specialist-skill.md` §2.3 + §7
- `practitioner` — PractitionerRecord per `arch/practitioner.md` §2.2 + §7
- `workflow` — WorkflowDescriptor + WorkflowInstance per `arch/workflow-
  work-unit.md` §2.1 + §2.2 + §7 + §13
- `work_unit` — WorkUnitKindDescriptor + WorkUnitInstance per `arch/
  workflow-work-unit.md` §2.3 + §2.4 + §7 + §13
- `workspace` — WorkspaceManifest per `arch/scope-model.md` §3 workspace
  integration + §8 cross-shape policy variation
- `claim` — Claim + ClaimAttestation + 6-event-kind catalog per `arch/
  claim-defensibility.md` §13

Foundation-up: imports only from `pbs.types` (AuditEventBase + ActorKind);
NO imports from `pbs.<surface>` modules to preserve layering.
"""
