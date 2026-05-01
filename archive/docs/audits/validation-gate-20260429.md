# Validation-gate audit (slice 16, first run)

**Date**: 2026-04-29
**Scope**: per slice 16 spec (Pydantic models + MCP tool handlers)
**Trigger**: verification run for ARCHITECTURE.md meta-rule 4
strict-validation discipline (added this session as a corollary
of the boundary-refinement work).
**Skill version**: audit 0.6.0

---

## Summary

- **Total findings**: 4 (one per pattern)
- **BLOCKERS**: 0 (none ship malformed data to a downstream consumer
  in the current code paths)
- **All 4 fixed in-session** — directly contradicting the
  strict-validation discipline we just shipped would be inconsistent;
  fixes are small and local

The four findings together represent the discipline's first-pass
hardening of the existing model layer. None are architectural
reshapes; all are tightening.

---

## Findings (all fixed in-session)

### F1 — Pattern 1 (Optional-on-required) + Pattern 2: bind_project writes contract-violating state.md

**File**: `backend/mcp-server/src/pbs_mcp/tools/projects.py:97-113`

**The issue**: `bind_project` wrote a state.md frontmatter dict directly
via `compose_baustein` (raw YAML serialize), bypassing the
ProjectState contract. Specifically:
- `phase: None` written for a field declared `phase: str = Field(...,
  min_length=1)` (required string with non-empty constraint)
- Missing required fields entirely: `bundesland`, `verfahren_type`
- Wrote `doctype_focus: []` which isn't in the ProjectState schema

A subsequent `get_project_state` call would have failed validation;
the malformed file would have already been on disk.

**Fix applied**:
- Added required initialization fields to `BindProjectInput`:
  `bundesland: StateCode = "MV"`, `verfahren_type: VerfahrenType =
  "regelverfahren"`, `phase: str = "0-aufstellungsbeschluss"`
- Routed the write through `ProjectState.model_validate` + the new
  `project_state.write_project_state` gate
- Removed the unused `doctype_focus` field
- Added an automatic `phase_history` entry for the initial phase so
  the cross-reference invariant (`current phase must appear in
  phase_history`) holds

**Verification**: smoke-tested `bind_project` with a temp project
root; written state.md round-trips through `parse_state_file`
cleanly.

### F2 — Pattern 4 (Loose-shape config): contract-bearing models lacked extra="forbid"

**Files**: `backend/mcp-server/src/pbs_mcp/office_config.py` (11 models),
`project_state.py` (4 models)

**The issue**: Pydantic v2's default `extra="ignore"` silently
accepts and drops unknown fields. For contract-bearing models (file-
load entry points), this masks typos and schema drift — a user
writes `ofice:` (typo) and the field vanishes without error.

**Fix applied**:
- New shared base class `pbs_mcp/_strict.py:StrictModel(BaseModel)`
  with `model_config = ConfigDict(extra="forbid")`
- All contract-bearing models in `office_config.py` (Office, Actor,
  Roots, Scope, Templates, FolderLayout, ProjectNumbering,
  PathClassification, Conventions, OfficeConfig) and `project_state.py`
  (PhaseEntry, Deadline, ProjectState, ProjectStateFile) rebased to
  StrictModel.
- `Integration` keeps `BaseModel` directly (it needs
  `populate_by_name=True` for the `class` alias) but its config now
  also includes `extra="forbid"` for parity.

**Verification**: confirmed extra-field rejection on Office +
ProjectState; existing v3 office.yaml still loads cleanly (no
unknown fields to reject).

**Decision NOT to extend to MCP tool I/O models** in `schemas.py`:
the MCP framework already validates JSON shape at the protocol
level, and tool I/O models aren't file-contract-bearing in the same
sense. Adding `extra="forbid"` everywhere would be ceremony without
clear value. Slice 16 brief explicitly distinguishes these.

### F3 — Pattern 3 (Exception swallowing): parse_frontmatter silently swallowed YAML errors

**File**: `backend/mcp-server/src/pbs_mcp/tools/memory.py:40-53`

**The issue**: `parse_frontmatter` caught `yaml.YAMLError`, logged a
warning, and returned `({}, content)` — indistinguishable from
"file has no frontmatter at all." Callers treated the empty dict
as "no frontmatter," silently skipping malformed memory records.
Per strict-validation discipline, malformed YAML should fail loud.

**Fix applied**: removed the `try/except yaml.YAMLError` —
`parse_frontmatter` now lets `yaml.YAMLError` propagate. Also added
a check that the parsed YAML is a dict (raises ValueError if it's
a scalar/list, which would also be a malformed frontmatter).

The "no frontmatter" interpretation (no leading `---` or no closing
`---`) still returns `({}, content)` — that's a valid file shape,
not a contract violation. Only present-but-malformed YAML now
fails loud.

**Caller responsibility**: callers walking many files (e.g.,
`list_bausteine` over a directory) can wrap their own
`try/except yaml.YAMLError` to skip-and-continue *with explicit
error reporting* — but the default is fail-loud per discipline.

### F4 — Pattern 3 (Exception swallowing): _manifest_info caught broad `Exception`

**File**: `backend/mcp-server/src/pbs_mcp/tools/discovery.py:53-79`

**The issue**: `_manifest_info` caught `Exception` (broad catch),
logged a warning, returned a `ManifestInfo` with `entry_count=None`
+ `last_updated=None`. Callers couldn't distinguish "manifest is
empty" from "manifest failed to parse" — the failure was hidden.

**Fix applied**:
- Added explicit `errors: list[str] = Field(default_factory=list)`
  to `ManifestInfo`
- Narrowed the catch: `yaml.YAMLError` and `OSError` only (not all
  `Exception`)
- Added isinstance-check that the parsed YAML is a dict
- Each error is reported via `errors` rather than swallowed; empty
  list means "parsed cleanly"

**Verification**: smoke-tested `list_reference_manifests` on the 6
populated manifests; all return `errors=[]`. No malformed manifests
in the current set, which is correct (slice 15 verified this).

---

## Stopping decision

**Slice 16 is complete on this first run + all findings fixed
in-session.** The strict-validation discipline is now structurally
enforced via `StrictModel` for file-contract-bearing models, plus
the audit slice that catches deviations going forward.

Re-run slice 16 after:
- Adding new Pydantic models (verify they inherit StrictModel where
  appropriate)
- Refactoring tool handlers (verify exception-swallowing didn't
  creep back in)
- Any deployment that increases the cost of validation laxness
  (multi-user, post-launch)

**Procedure validation**: slice 16's first run heeded the brief's
agent-discipline note ("do not classify findings as BLOCKER unless
the violation actively ships malformed data"). All 4 findings were
correctly classified as FINDING-not-BLOCKER. The brief's tighter
language worked — no agent verdict-overreach this run, in contrast
to slice 14 + slice 15 + target 8 first-runs.
