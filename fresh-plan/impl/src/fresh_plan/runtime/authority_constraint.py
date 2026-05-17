"""Authority-constraint grammar parser per D56 §B.1.1 (minimal grammar).

The constraint string slot on each ``shape.authority-bindings[i]`` is
parsed at Shape ``__init__`` time per D56 §C; the parsed form is cached
parallel to the binding and consulted at per-event ``Shape.check_authority``
time.

Minimal grammar (D56 §B.1.1):

  constraint ::= { "equals": { "lhs": <path>, "rhs": <path> } }
              | { "in":     { "lhs": <path>, "rhs": [<literal>, ...] } }

  path       ::= "event.payload.<key>"
              | "event.actor.<key>"
              | "state.shape-config.<key>"
              | "literal:<string>"

Per CLAUDE.md no-silent-substitution: unknown top-level keys, malformed
path strings, unresolved path lookups at per-event time → fail closed.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional, Union


class AuthorityConstraintGrammarError(ValueError):
    """Raised on D56 §B.1.1 grammar violation at parse time.

    Caller (Shape.__init__) wraps into ``WorkspaceBootError(category=
    "authority-constraint-grammar")``.
    """


@dataclass(frozen=True)
class _ParsedConstraint:
    op: str  # "equals" or "in"
    lhs: str  # path string
    rhs: Union[str, tuple[str, ...]]  # path string for equals; literal tuple for in


def parse_authority_constraint(raw: Any) -> Optional[_ParsedConstraint]:
    """Parse a D56 §B.1.1 constraint slot value; return parsed form or None.

    Accepts either a JSON-encoded string (current shape.schema.json
    ``additional-constraints`` field is a string slot) or an already-parsed
    dict. Empty / None / empty-string → returns None (no constraint;
    back-compat with current decorative use).
    """
    if raw is None:
        return None
    if isinstance(raw, str):
        stripped = raw.strip()
        if not stripped:
            return None
        try:
            obj = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise AuthorityConstraintGrammarError(
                f"additional-constraints string is not valid JSON: {exc}"
            ) from exc
    elif isinstance(raw, dict):
        obj = raw
    else:
        raise AuthorityConstraintGrammarError(
            f"additional-constraints must be a string or object; got "
            f"{type(raw).__name__}"
        )

    if not isinstance(obj, dict):
        raise AuthorityConstraintGrammarError(
            f"additional-constraints must parse to an object; got {type(obj).__name__}"
        )
    if set(obj.keys()) - {"equals", "in"}:
        raise AuthorityConstraintGrammarError(
            f"additional-constraints admits only 'equals' or 'in' top-level keys; "
            f"got keys={sorted(obj.keys())!r}"
        )
    if len(obj) != 1:
        raise AuthorityConstraintGrammarError(
            f"additional-constraints requires exactly one top-level key; "
            f"got keys={sorted(obj.keys())!r}"
        )

    if "equals" in obj:
        body = obj["equals"]
        if not isinstance(body, dict) or set(body.keys()) != {"lhs", "rhs"}:
            raise AuthorityConstraintGrammarError(
                "'equals' body must be {'lhs': <path>, 'rhs': <path>}"
            )
        lhs = body["lhs"]
        rhs = body["rhs"]
        if not isinstance(lhs, str) or not isinstance(rhs, str):
            raise AuthorityConstraintGrammarError(
                "'equals' lhs and rhs must be path strings"
            )
        _validate_path(lhs)
        _validate_path(rhs)
        return _ParsedConstraint(op="equals", lhs=lhs, rhs=rhs)

    if "in" in obj:
        body = obj["in"]
        if not isinstance(body, dict) or set(body.keys()) != {"lhs", "rhs"}:
            raise AuthorityConstraintGrammarError(
                "'in' body must be {'lhs': <path>, 'rhs': [<literal>, ...]}"
            )
        lhs = body["lhs"]
        rhs = body["rhs"]
        if not isinstance(lhs, str):
            raise AuthorityConstraintGrammarError("'in' lhs must be a path string")
        if not isinstance(rhs, list) or not all(isinstance(x, str) for x in rhs):
            raise AuthorityConstraintGrammarError(
                "'in' rhs must be a non-empty list of literal strings"
            )
        _validate_path(lhs)
        return _ParsedConstraint(op="in", lhs=lhs, rhs=tuple(rhs))

    # Unreachable given the key-set check above; defensive.
    raise AuthorityConstraintGrammarError("unrecognized constraint form")


def _validate_path(path: str) -> None:
    """Validate a path string against the four allowed prefixes."""
    allowed_prefixes = (
        "event.payload.",
        "event.actor.",
        "state.shape-config.",
        "literal:",
    )
    if not any(path.startswith(p) for p in allowed_prefixes):
        raise AuthorityConstraintGrammarError(
            f"path {path!r} must start with one of "
            f"event.payload. / event.actor. / state.shape-config. / literal:"
        )


def _resolve_path(
    path: str,
    event: dict,
    matched_actor_record: Optional[dict],
    state: Any,
) -> Optional[Any]:
    """Resolve a path to a value. Returns None on missing-key (fail-closed)."""
    if path.startswith("literal:"):
        return path[len("literal:"):]
    if path.startswith("event.payload."):
        key = path[len("event.payload."):]
        payload = event.get("payload") or {}
        return payload.get(key)
    if path.startswith("event.actor."):
        key = path[len("event.actor."):]
        if matched_actor_record is None:
            return None
        return matched_actor_record.get(key)
    if path.startswith("state.shape-config."):
        key = path[len("state.shape-config."):]
        shape_config = getattr(state, "shape_config", None) or {}
        return shape_config.get(key)
    return None


def evaluate_constraint(
    parsed: _ParsedConstraint,
    event: dict,
    matched_actor_record: Optional[dict],
    state: Any,
) -> bool:
    """Evaluate parsed constraint against (event, actor-record, state).

    Per D56 §B.1.1 fail-closed: unresolved path lookups → False (the
    constraint is unsatisfied; caller surfaces as
    ``EventRejected(category="authority")``).
    """
    lhs_val = _resolve_path(parsed.lhs, event, matched_actor_record, state)
    if parsed.op == "equals":
        rhs_val = _resolve_path(parsed.rhs, event, matched_actor_record, state)
        # Fail-closed on either-side missing per CLAUDE.md.
        if lhs_val is None or rhs_val is None:
            return False
        return lhs_val == rhs_val
    if parsed.op == "in":
        if lhs_val is None:
            return False
        return lhs_val in parsed.rhs
    return False
