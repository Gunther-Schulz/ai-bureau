"""Specialist runtime — D19 + specialist.schema.json + D37 + D36 B6 brief.

Per D19, specialists are packaged role/skill bundles loaded into a
workspace's substrate via the `skills` capability (D17). `Specialist` is
the base class reading off D19; concrete specialist impls subclass it.

Per D37, cross-specialist coordination is event-driven at framework level
(declared-event-emissions / declared-event-subscriptions per D19); the
substrate's subscriber-dispatch infrastructure dispatches matching events
into `on_event`. RPC-style direct invocation is implementation-shape.

For Phase B, the shipped GenericSpecialist is a stub: `handle_skill`
emits one `action` event per invoke and returns a canned response;
`on_event` is a no-op (subclasses override for reactive policy).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

from fresh_plan.runtime.provision import load_provision_spec


class SkillExecutionError(Exception):
    """Specialist ``handle_skill`` runtime failure per D50 §B.1 (specialist cluster supersedes per D45 §C).

    Phase C+ real-wire forward-bar: real-wire specialist impls (subclasses
    of ``Specialist`` overriding ``handle_skill``) SHALL raise this on
    skill-body failures (domain-validation rejection, external-dependency
    unavailable, runtime invariant violation, etc.). Phase B stubs do not
    trigger this exception — Phase B pre-condition guards stay as Python
    idioms (bare ``RuntimeError`` / ``NotImplementedError``) per D50 §D D-1.

    Composes with D47 §B.1 SubscriberDispatchError aggregation: when a
    specialist's ``on_event`` delegates to ``handle_skill`` which raises
    SkillExecutionError, the exception is captured per D47 §B.1 into
    substrate's ``_subscriber_failures`` (substrate.py:310-320) and
    aggregated as SubscriberDispatchError after the outer drain. Direct
    ``handle_skill`` callers see the raw exception.

    Composes with D48 §B.1 AdapterCallError: when ``handle_skill`` body
    invokes ``adapter.call(...)`` which raises AdapterCallError,
    specialist-impl choice (per D50 §D D-5) — wrap as
    SkillExecutionError(category="external-dependency-error",
    original=AdapterCallError) for uniform skill-failure surface, OR
    propagate raw AdapterCallError. Caller MUST be prepared for either.

    Per D50 §D D-2: starter category vocabulary (domain-error /
    external-dependency-error / skill-execution / unknown) is
    practitioner-shape-flavored; non-practitioner shapes register
    additional categories per D29 namespacing.
    """

    def __init__(
        self,
        *,
        specialist_id: str,
        skill_id: str,
        category: str,
        detail: Optional[dict] = None,
    ) -> None:
        self.specialist_id = specialist_id
        self.skill_id = skill_id
        self.category = category
        self.detail = dict(detail) if detail else {}
        super().__init__(
            f"[{category}] specialist={specialist_id!r} skill={skill_id!r}: {self.detail}"
        )


def _parse_activation_scope(
    raw: Any,
) -> Optional[Callable[[dict], bool]]:
    """Parse D55 §B.1 minimal grammar; return predicate callable or None.

    Grammar:

      activation-scope ::= "always"                                       ; string literal
                         | { "when": { "payload-subtype": <string> } }    ; single-field predicate

    Returns ``None`` when ``raw`` is ``None`` or the literal ``"always"``
    (semantic equivalent of always-active). Returns a callable
    ``(event) -> bool`` otherwise. Raises ``ValueError`` on grammar
    violation. Caller (``attach_workspace``) wraps into
    ``WorkspaceBootError(category="activation-scope-grammar")``.
    """
    if raw is None:
        return None
    if isinstance(raw, str):
        if raw == "always":
            return None
        raise ValueError(
            f"activation-scope string literal must be 'always'; got {raw!r}"
        )
    if isinstance(raw, dict):
        if set(raw.keys()) != {"when"}:
            raise ValueError(
                f"activation-scope object must have exactly one top-level key 'when'; "
                f"got keys={sorted(raw.keys())!r}"
            )
        when = raw["when"]
        if not isinstance(when, dict):
            raise ValueError(
                f"activation-scope 'when' value must be an object; got {type(when).__name__}"
            )
        if set(when.keys()) != {"payload-subtype"}:
            raise ValueError(
                f"activation-scope 'when' object admits exactly one key 'payload-subtype'; "
                f"got keys={sorted(when.keys())!r}"
            )
        target_subtype = when["payload-subtype"]
        if not isinstance(target_subtype, str) or not target_subtype:
            raise ValueError(
                "activation-scope 'when.payload-subtype' must be a non-empty string; "
                f"got {target_subtype!r}"
            )

        def predicate(event: dict, _target: str = target_subtype) -> bool:
            return event.get("payload-subtype") == _target

        return predicate
    raise ValueError(
        f"activation-scope must be either a string or an object; got "
        f"{type(raw).__name__}"
    )


@dataclass
class Specialist:
    """Base class for specialist runtime impls per D19 + specialist.schema.json.

    Holds the loaded spec, exposes D19 slot accessors, manages workspace
    attachment + required-adapter resolution + skill-registration into
    the substrate's `skills` capability (D17). Subclasses override
    `handle_skill` to implement skill behavior and `on_event` to react
    to subscribed events (D37).
    """

    spec: dict
    # Per D57 §B.1: opaque pass-through configuration dict from
    # composition.specialist-bindings[i].configuration. None when omitted.
    configuration: Optional[dict] = None
    _emit_event: Optional[Callable[..., dict]] = field(default=None, repr=False)
    _workspace: Any = field(default=None, repr=False)
    _adapters: dict[str, "Adapter"] = field(default_factory=dict, repr=False)
    # Per D55 §B.1: parsed activation-scope predicate; None means always-active.
    # Populated by ``_parse_activation_scope`` at ``attach_workspace`` time.
    _activation_predicate: Optional[Callable[[dict], bool]] = field(
        default=None, repr=False
    )

    @property
    def id(self) -> str:
        return self.spec["id"]

    @property
    def version(self) -> str:
        return self.spec["version"]

    @property
    def roles(self) -> list[str]:
        return list(self.spec.get("roles", []) or [])

    @property
    def skills(self) -> list[dict]:
        return list(self.spec.get("skills", []) or [])

    @property
    def supported_work_unit_kinds(self) -> list[str]:
        return list(self.spec.get("supported-work-unit-kinds", []) or [])

    @property
    def required_adapter_bindings(self) -> list[str]:
        return list(self.spec.get("required-adapter-bindings", []) or [])

    @property
    def required_substrate_capabilities(self) -> list[str]:
        return list(self.spec.get("required-substrate-capabilities", []) or [])

    @property
    def declared_event_emissions(self) -> list[dict]:
        return list(self.spec.get("declared-event-emissions", []) or [])

    @property
    def declared_event_subscriptions(self) -> list[dict]:
        return list(self.spec.get("declared-event-subscriptions", []) or [])

    @property
    def activation_scope(self) -> Optional[str]:
        return self.spec.get("activation-scope")

    # ---------------------------------------------------------------
    # Workspace attachment (boot-ordering: post-Workspace + post-adapter-attach)
    # ---------------------------------------------------------------

    def attach_workspace(self, workspace: Any) -> None:
        """Wire workspace event-emit + resolve required adapter bindings.

        Per D30 cross-kind referential integrity: every entry in
        `required-adapter-bindings` must resolve to an adapter bound in
        the workspace. Per D48 §B.3 (adapter cluster supersedes per D45 §C):
        misses surface as structured `WorkspaceBootError(category=
        "adapter-binding-resolution", ...)` (replaces the prior bare
        RuntimeError; symmetric with D46's raise-at-failure-site pattern).

        Per D55 §B.1: parse the ``activation-scope`` slot at attach time
        and cache the predicate on ``self._activation_predicate``. Grammar
        parse-failures raise ``WorkspaceBootError(category=
        "activation-scope-grammar")``.
        """
        # Import locally to avoid a module-level circular dep: boot.py
        # imports specialist.py lazily (inside boot_workspace); this
        # reverse import is the symmetric lazy path.
        from fresh_plan.runtime.boot import WorkspaceBootError
        from fresh_plan.validator.types import ValidationFailure

        self._workspace = workspace
        substrate = workspace._substrate
        # Per D55 §B.1: parse activation-scope before adapter-binding-resolution.
        # Look up binding-id early so error path can name it.
        my_binding_id_for_scope: Optional[str] = next(
            (bid for bid, sp in substrate.specialist_instances.items() if sp is self),
            None,
        )
        # Per D64 §B.1: wrap workspace._emit_event as a closure pre-filling
        # emitting-specialist=<self-binding-id>. `setdefault` lets a
        # subclass override attribution (e.g., when delegating); default
        # is the bound specialist's own binding-id.
        _binding_id_for_emit = my_binding_id_for_scope
        _ws_emit = workspace._emit_event

        def _wrapped_emit(**kwargs: Any) -> dict:
            kwargs.setdefault("emitting_specialist", _binding_id_for_emit)
            return _ws_emit(**kwargs)

        self._emit_event = _wrapped_emit
        try:
            self._activation_predicate = _parse_activation_scope(
                self.spec.get("activation-scope")
            )
        except ValueError as exc:
            raise WorkspaceBootError(
                [
                    ValidationFailure(
                        category="activation-scope-grammar",
                        path=(
                            f"composition.specialist-bindings"
                            f"[binding-id={my_binding_id_for_scope!r}]"
                            f".activation-scope"
                        ),
                        value=self.spec.get("activation-scope"),
                        reason=(
                            f"specialist {self.id!r}: activation-scope grammar "
                            f"violation: {exc}"
                        ),
                    )
                ]
            ) from exc
        # Reuse the binding-id already looked up for activation-scope error path.
        my_binding_id: Optional[str] = my_binding_id_for_scope
        for required in self.required_adapter_bindings:
            matched_bid: Optional[str] = None
            for bid, binding_dict in substrate.adapter_bindings.items():
                if binding_dict.get("provision") == required:
                    matched_bid = bid
                    break
            if matched_bid is None:
                raise WorkspaceBootError(
                    [
                        ValidationFailure(
                            category="adapter-binding-resolution",
                            path=(
                                f"composition.specialist-bindings"
                                f"[binding-id={my_binding_id!r}]"
                                f".required-adapter-bindings"
                            ),
                            value=required,
                            reason=(
                                f"specialist {self.id!r}: required-adapter-binding "
                                f"{required!r} has no matching adapter-binding in workspace"
                            ),
                        )
                    ]
                )
            self._adapters[required] = workspace.adapter(matched_bid)

    def register_skills(self, skill_registry) -> None:
        """Register each declared skill as a handle_skill-dispatching callable."""
        for skill in self.skills:
            skill_id = skill if isinstance(skill, str) else skill.get("id")
            if not skill_id:
                continue
            skill_registry.register(
                skill_id,
                lambda params, _sid=skill_id: self.handle_skill(_sid, params),
            )

    # ---------------------------------------------------------------
    # Skill dispatch (abstract; subclass-owned)
    # ---------------------------------------------------------------

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        """Dispatch a skill invocation. Subclasses MUST override."""
        raise NotImplementedError("Specialist subclasses must implement handle_skill")

    def on_event(self, event: dict) -> None:
        """React to a subscribed event (D37). Default = no-op; override for policy."""
        return None


@dataclass
class GenericSpecialist(Specialist):
    """First concrete specialist impl per B6 / D26 — deliberately neutral, NOT
    practitioner-specialist; stub behavior emits one action event per skill
    invocation and returns a canned response.
    """

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "specialist not attached to a workspace; call attach_workspace first"
            )
        params = params or {}
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": skill_id,
                "parameters": params,
            },
        )
        return {"ok": True, "skill": skill_id, "stub": True, "parameters": params}


@dataclass
class RAGSpecialist(Specialist):
    """Retrieval specialist per D38 (knowledge composes via existing primitives).

    First concrete impl of a retrieval-shaped specialist. handle_skill('retrieve',
    {query, k?}) invokes the bound MCP retriever adapter and returns a stub
    retrieval-shaped response with `chunks`. Real-wire retrieval (real corpus +
    embedding model + vector DB) is Phase C / D.
    """

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "specialist not attached to a workspace; call attach_workspace first"
            )
        if skill_id != "retrieve":
            raise NotImplementedError(
                f"rag-specialist does not implement skill {skill_id!r}"
            )
        params = params or {}
        query = params.get("query", "")
        k = int(params.get("k", 3))
        adapter = self._adapters.get("rag-via-mcp-ext:rag-retriever-adapter")
        if adapter is None:
            raise RuntimeError(
                "rag-specialist: required adapter "
                "'rag-via-mcp-ext:rag-retriever-adapter' not bound"
            )
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": skill_id,
                "parameters": params,
            },
        )
        adapter_response = adapter.call("retrieve", {"query": query, "k": k})
        chunks = [
            {"id": f"chunk-{i + 1}", "content": f"stub chunk {i + 1} for query={query!r}"}
            for i in range(k)
        ]
        return {
            "ok": True,
            "skill": "retrieve",
            "query": query,
            "k": k,
            "chunks": chunks,
            "adapter-outcome-ref": adapter_response["outcome-reference"],
            "stub": True,
        }


@dataclass
class RealWireRAGSpecialist(Specialist):
    """Phase C real-wire RAG specialist per D75 §B.1 (closes C7).

    Per D68 §A C7 + §C closure items (c) + (f). REPLACES the B7 ``RAGSpecialist``
    stub (kept in place for back-reference) by invoking the c3
    ``RealWireMCPClientAdapter`` (D71) end-to-end through the bound
    ``mcp-server-ext:mcp-real-wire-adapter`` provision (the required-adapter-
    bindings entry resolves to that 0.2.0 adapter). Activates the D50 §B.1
    ``SkillExecutionError`` forward-bar under real-wire conditions per starter
    category vocabulary (``domain-error`` / ``external-dependency-error`` /
    ``skill-execution`` / ``unknown``).

    Per D50 §D D-5 (AdapterCallError-inside-handle_skill composition contract)
    — this is the FIRST concrete real-wire impl establishing precedent per
    the D-5 framing. **Composition choice: WRAP** AdapterCallError as
    ``SkillExecutionError(category="external-dependency-error", ...)`` with
    the original AdapterCallError chained via Python's ``__cause__`` (raise
    ... from exc). Rationale (per D75 §B.1):

      1. Uniform skill-failure surface for callers — a single exception type
         (SkillExecutionError) per specialist boundary instead of two
         (SkillExecutionError + AdapterCallError) cohabiting.
      2. Preserves AdapterCallError diagnostic detail via __cause__ chain;
         callers introspecting __cause__ see the wire-layer category +
         adapter_id + call_target + detail dict.
      3. No silent substitution: the original AdapterCallError isn't
         swallowed; it's wrapped + chained.
      4. First concrete D-5 precedent; future real-wire specialists MAY
         PROPAGATE raw if uniformity is less important than layer-error
         transparency for their use case (per D50 §D D-5 explicit choice).

    Per D64 §B.1 emit-attribution: INHERITED via ``Specialist.attach_workspace``
    closure-wrap (specialist.py:226-237 sets ``self._emit_event`` to a
    closure pre-filling ``emitting_specialist=<binding-id>``). The class
    overrides nothing on attach; the inherited wrapper auto-attributes the
    action event emitted at handle_skill entry. Per D71 §B.1 pre-wire convention
    the action event is emitted BEFORE the adapter call so intent is recorded
    in the chain regardless of call outcome.

    Per D45 detection-surface-recovery triad (D75 §B.1 + §B.2):

      - **domain-error** ← params validation rejection. Detection: non-string
        / empty query; non-int k; k < 1; k > 100 (sanity-bar). Surface:
        SkillExecutionError(category="domain-error", detail={...}).
        Recovery: caller corrects params + retries.
      - **external-dependency-error** ← AdapterCallError caught from
        ``adapter.call('retrieve', ...)`` + WRAPped per D-5 RESOLUTION.
        Detection: AdapterCallError raised inside the call body. Surface:
        SkillExecutionError(category="external-dependency-error",
        detail={'underlying': str(exc), 'category': exc.category,
        'adapter_id': exc.adapter_id, 'call_target': exc.call_target})
        with __cause__ = original AdapterCallError. Recovery: caller
        catches SkillExecutionError + introspects __cause__ for wire detail.
      - **skill-execution** ← unexpected runtime invariant violation inside
        handle_skill body AFTER adapter returns. Detection: malformed
        result shape — chunks missing / chunks not a list / chunk lacks
        ``id`` or ``content`` field. Surface: SkillExecutionError(
        category="skill-execution", detail={...}). Recovery: caller
        catches; misbehaving server requires per-server-impl debug.
      - **unknown** ← catch-all bare ``except Exception`` final branch.
        Detection: any exception class not pre-classified above + not a
        SkillExecutionError already (re-raise on instance check).
        Surface: SkillExecutionError(category="unknown", detail={...})
        with __cause__ = original exception. Recovery: caller observes;
        bug-report territory.
    """

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        # Import locally to avoid module-level circular dep with adapter.py.
        from fresh_plan.runtime.adapter import AdapterCallError

        if self._emit_event is None or self._workspace is None:
            # Pre-condition guard per D50 §D D-1 — Python idiom (not
            # SkillExecutionError) because the specialist is not yet
            # attached to a workspace.
            raise RuntimeError(
                "specialist not attached to a workspace; call attach_workspace first"
            )
        if skill_id != "retrieve":
            raise NotImplementedError(
                f"rag-realwire-specialist does not implement skill {skill_id!r}"
            )

        params = params or {}

        # --- domain-error path: params validation ---
        query = params.get("query")
        if not isinstance(query, str) or not query:
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="domain-error",
                detail={
                    "reason": "query must be a non-empty string",
                    "got": repr(query),
                },
            )
        k_raw = params.get("k", 3)
        try:
            k = int(k_raw)
        except (TypeError, ValueError):
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="domain-error",
                detail={
                    "reason": "k must be an int",
                    "got": repr(k_raw),
                },
            )
        if k < 1:
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="domain-error",
                detail={"reason": "k must be >= 1", "got": k},
            )
        # Sanity upper bound; per-shape extensions may relax via configuration.
        _K_MAX = 100
        if k > _K_MAX:
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="domain-error",
                detail={
                    "reason": f"k must be <= {_K_MAX}",
                    "got": k,
                },
            )

        adapter = self._adapters.get("mcp-server-ext:mcp-real-wire-adapter")
        if adapter is None:
            # Required-adapter-binding wasn't satisfied at attach time
            # (Specialist.attach_workspace would have raised
            # WorkspaceBootError already); reaching here means the spec
            # was constructed bypassing attach_workspace. Pre-condition
            # guard per D50 §D D-1 — Python idiom.
            raise RuntimeError(
                "rag-realwire-specialist: required adapter "
                "'mcp-server-ext:mcp-real-wire-adapter' not bound"
            )

        # Emit action event BEFORE adapter call per D71 §B.1 pre-wire
        # convention (intent recorded in chain regardless of outcome).
        # D64 §B.1 emit-attribution: inherited closure-wrap auto-fills
        # emitting_specialist=<binding-id>.
        actor_id = next(iter(self._workspace._substrate.state.actors), None)
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": skill_id,
                "parameters": {"query": query, "k": k},
            },
        )

        # --- external-dependency-error path: adapter.call + WRAP per D-5 ---
        try:
            adapter_response = adapter.call("retrieve", {"query": query, "k": k})
        except AdapterCallError as exc:
            # WRAP per D50 §D D-5 RESOLUTION (D75 §B.1). __cause__ chain
            # preserves the original AdapterCallError for caller
            # introspection.
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="external-dependency-error",
                detail={
                    "underlying": str(exc),
                    "adapter-category": exc.category,
                    "adapter-id": exc.adapter_id,
                    "call-target": exc.call_target,
                },
            ) from exc
        except SkillExecutionError:
            # Already classified upstream — re-raise rather than catch-all.
            raise
        except Exception as exc:
            # Unexpected exception class from adapter.call (NOT
            # AdapterCallError); catch-all per D75 §B.1 unknown vocabulary.
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="unknown",
                detail={
                    "reason": "unexpected exception from adapter.call",
                    "exception-type": type(exc).__name__,
                    "exception": str(exc),
                },
            ) from exc

        # --- skill-execution path: result parsing ---
        try:
            content = adapter_response.get("content", [])
            if not isinstance(content, list):
                raise SkillExecutionError(
                    specialist_id=self.id,
                    skill_id=skill_id,
                    category="skill-execution",
                    detail={
                        "reason": "adapter response 'content' is not a list",
                        "got-type": type(content).__name__,
                    },
                )
            # Parse content blocks into chunks. Each TextContent block's
            # text is treated as the chunk content; chunk id is synthesized
            # from positional index per the starter retrieval-task shape.
            # Phase D+ pioneer-instance may register a richer chunk-content
            # schema per D29 namespacing.
            chunks: list[dict] = []
            for i, block in enumerate(content):
                if not isinstance(block, dict):
                    raise SkillExecutionError(
                        specialist_id=self.id,
                        skill_id=skill_id,
                        category="skill-execution",
                        detail={
                            "reason": "content block is not a dict",
                            "index": i,
                            "got-type": type(block).__name__,
                        },
                    )
                text = block.get("text")
                if text is None:
                    raise SkillExecutionError(
                        specialist_id=self.id,
                        skill_id=skill_id,
                        category="skill-execution",
                        detail={
                            "reason": "content block missing 'text'",
                            "index": i,
                            "block-keys": sorted(block.keys()),
                        },
                    )
                chunks.append({"id": f"chunk-{i + 1}", "content": text})
        except SkillExecutionError:
            raise
        except Exception as exc:
            # Unexpected exception class during result parsing → unknown.
            raise SkillExecutionError(
                specialist_id=self.id,
                skill_id=skill_id,
                category="unknown",
                detail={
                    "reason": "unexpected exception parsing adapter result",
                    "exception-type": type(exc).__name__,
                    "exception": str(exc),
                },
            ) from exc

        return {
            "ok": True,
            "skill": "retrieve",
            "query": query,
            "k": k,
            "chunks": chunks,
            "adapter-outcome-ref": adapter_response.get("outcome-reference"),
        }


# Module-level registry of (specialist.id → runtime class). Populated as new
# specialist impls land. For Phase B there's only GenericSpecialist; future
# practitioner-specialist (Phase D) registers here.
_SPECIALIST_CLASSES: dict[str, type[Specialist]] = {
    "generic-specialist": GenericSpecialist,
    "rag-specialist": RAGSpecialist,
    "rag-realwire-specialist": RealWireRAGSpecialist,
}


def load_specialist_from_provision(
    provision_ref: str,
    extensions_dir: Path,
    *,
    configuration: Optional[dict] = None,
) -> Specialist:
    """Load a specialist spec from a `<ext-id>:<provision-id>` ref + instantiate.

    Dispatches by `spec.id` to the registered runtime class. Raises
    ValueError if the spec's id has no registered runtime class (boot.py
    wraps as ``category="resolution"``). Constructor-raises are caught
    at boot.py and wrapped as ``category="configuration-rejected"`` per
    D57 §B.1.
    """
    from fresh_plan.runtime.provision import ProvisionResolutionError

    spec = load_provision_spec(provision_ref, extensions_dir)
    specialist_id = spec.get("id")
    cls = _SPECIALIST_CLASSES.get(specialist_id)
    if cls is None:
        raise ProvisionResolutionError(
            f"specialist provision {provision_ref!r}: spec id {specialist_id!r} "
            f"has no registered Specialist runtime class"
        )
    return cls(spec=spec, configuration=configuration)
