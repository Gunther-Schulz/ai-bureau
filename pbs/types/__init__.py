"""Foundation types — actor_kind enum, AuditEvent base, common Pydantic bases.

Read by every protocol Surface + every reference impl. Foundation-up: no
imports from `pbs.<surface>` modules; only stdlib + pydantic + this
package's own types submodules.
"""
