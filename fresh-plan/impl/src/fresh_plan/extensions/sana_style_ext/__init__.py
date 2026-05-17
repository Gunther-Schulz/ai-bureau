"""Sana-style extension stubs per D53 §C (Sana-style worked-example fixture).

Provides:
  - ``SanaKnowledgeShape`` (subclass of ``runtime.shape.Shape``) — installs
    pre-citation-impl as a ``pre-event-emit`` handler and
    post-corpus-write-impl as a ``post-event-emit`` handler; tracks known
    action outcome-references on the shape instance for evidence-reference
    resolution.
  - ``KnowledgeAgentSpecialist`` (subclass of ``runtime.specialist.Specialist``)
    — implements ``retrieve`` (delegates to knowledge-retriever adapter) and
    ``synthesize`` (emits an evidence-bearing claim whose evidence-references
    list outcome-references from prior retrieve action events).

Adapters reuse the already-registered ``MCPToolAdapter`` (mcp-server-ext:
mcp-client protocol — registered in ``runtime.adapter._ADAPTER_CLASSES``),
so no new adapter runtime class is introduced here.

Registration into framework runtime registries happens via the
:func:`register` helper, invoked from the test-fixture setup (not at
module import) to keep the registration explicit and scoped.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from fresh_plan.runtime.shape import Shape, _stub_handler
from fresh_plan.runtime.specialist import Specialist


@dataclass
class SanaKnowledgeShape(Shape):
    """Knowledge-shape per D53 §B Sana-style instantiation.

    The pre-citation policy (D53 §B + D38 §3) is implemented as a
    ``pre-event-emit`` hook handler that fires before substrate appends
    each event (substrate.py:219). For claim events whose first actor
    carries role='author' (the agent's role for synthesis output), the
    handler requires ``payload.evidence-references`` to be present,
    non-empty, AND every reference must resolve to a known prior action
    outcome-reference observed via the companion ``post-event-emit``
    handler. Raising from a ``pre-event-emit`` handler surfaces as
    ``EventRejected(category="hook-handler")`` per D47 §B.2 (substrate.py:
    223-235).

    Per D52 §B.1 + D52 §D D-7 forward-bar: this is the first fixture
    shape to use a non-"none" ``actor-requirements`` slot; the spec
    declares ``{human-actor: {min: 1}}`` so D52 step 2.5 fires during
    boot's actor-seeding loop (boot.py:315-368). Manifest actor order
    must place a human-actor FIRST so the constraint is satisfied
    after the first add (resulting state count = 1, satisfying min=1).
    """

    _known_outcome_refs: set[str] = field(default_factory=set, init=False, repr=False)

    def register_handlers(self, hook_registry: Any) -> None:
        """Install pre-citation (as pre-event-emit) + post-corpus-write (as
        post-event-emit) handlers; no-op stubs for any other declared hook
        names (parallel to GenericShape's stub-handler discipline).
        """
        for hook in self.hooks:
            name = hook.get("name")
            if name == "pre-event-emit":
                hook_registry.register(name, self._pre_event_emit_handler)
            elif name == "post-event-emit":
                hook_registry.register(name, self._post_event_emit_handler)
            elif name:
                # Semantic-declaration hooks (pre-citation, post-corpus-write)
                # carry a no-op handler per GenericShape pattern; their
                # actual policy lives inside pre/post-event-emit handlers
                # above. Registering a stub keeps `registered_names()`
                # reporting them as observable.
                hook_registry.register(name, _stub_handler)

    # ------------------------------------------------------------------
    # pre-citation policy (runs at substrate's pre-event-emit lifecycle).
    # ------------------------------------------------------------------

    def _pre_event_emit_handler(self, context: dict) -> None:
        """For agent-emitted (role=author) claims: require non-empty
        ``evidence-references`` and require every reference to resolve to
        a known prior action ``outcome-reference``. Raise → EventRejected.

        All other events pass through unchecked.
        """
        event = context.get("event") or {}
        if event.get("payload-subtype") != "claim":
            return
        actors = event.get("actors") or []
        if not actors:
            return
        # Discriminate by the first attributing actor's role. The Sana
        # convention: agent-actor emitting role='author' = synthesis-claim
        # subject to citation gate. Curator/consumer claims (role=curator
        # or role=consumer) bypass the citation gate.
        first_role = actors[0].get("role")
        if first_role != "author":
            return

        payload = event.get("payload") or {}
        refs = payload.get("evidence-references")
        if not refs:
            raise RuntimeError(
                f"sana-knowledge-shape pre-citation: synthesis-claim (role='author') "
                f"requires non-empty evidence-references; payload had "
                f"evidence-references={refs!r}"
            )
        missing = [r for r in refs if r not in self._known_outcome_refs]
        if missing:
            raise RuntimeError(
                f"sana-knowledge-shape pre-citation: synthesis-claim evidence-references "
                f"{missing!r} do not resolve to any prior action outcome-reference "
                f"(known={sorted(self._known_outcome_refs)!r})"
            )

    # ------------------------------------------------------------------
    # post-corpus-write projection (runs at substrate's post-event-emit
    # lifecycle). Captures outcome-references from action events so
    # subsequent pre-citation checks have data to validate against.
    # ------------------------------------------------------------------

    def _post_event_emit_handler(self, context: dict) -> None:
        event = context.get("event") or {}
        if event.get("payload-subtype") != "action":
            return
        payload = event.get("payload") or {}
        outcome_ref = payload.get("outcome-reference")
        if outcome_ref:
            self._known_outcome_refs.add(outcome_ref)


@dataclass
class KnowledgeAgentSpecialist(Specialist):
    """Knowledge-agent specialist per D53 §B.

    Implements two skills:

      - ``retrieve`` — delegates to the knowledge-retriever adapter; the
        adapter's ``call`` emits one action event with outcome-reference.
        The specialist itself ALSO emits one action event (mirroring
        RAGSpecialist's pattern) so the chain shows both the
        specialist-level intent + the adapter-level invocation.

      - ``synthesize`` — emits one action event (the synthesis act) then
        one claim event with ``evidence-references`` listing the
        outcome-references of prior retrieve action events observed in
        the substrate event chain. Subject to the sana-knowledge-shape
        pre-citation hook (registered via pre-event-emit). When
        ``params['evidence-references']`` is explicitly supplied (incl.
        empty list), it overrides the chain-derived references — used by
        Test 5 to exercise the missing-refs rejection path.
    """

    def handle_skill(self, skill_id: str, params: dict) -> Any:
        if self._emit_event is None or self._workspace is None:
            raise RuntimeError(
                "knowledge-agent-specialist not attached to a workspace; "
                "call attach_workspace first"
            )
        params = params or {}

        if skill_id == "retrieve":
            return self._handle_retrieve(params)
        if skill_id == "synthesize":
            return self._handle_synthesize(params)
        raise NotImplementedError(
            f"knowledge-agent-specialist does not implement skill {skill_id!r}"
        )

    def _agent_actor_id(self) -> Optional[str]:
        """First agent-actor in the workspace; used for event attribution."""
        substrate = self._workspace._substrate
        for aid, rec in substrate.state.actors.items():
            if rec.get("subtype") == "agent-actor":
                return aid
        # Defensive: fall back to first actor if no agent-actor present
        return next(iter(substrate.state.actors), None)

    def _handle_retrieve(self, params: dict) -> dict:
        query = params.get("query", "")
        k = int(params.get("k", 3))
        adapter = self._adapters.get("sana-style-ext:knowledge-retriever-adapter")
        if adapter is None:
            raise RuntimeError(
                "knowledge-agent-specialist: required adapter "
                "'sana-style-ext:knowledge-retriever-adapter' not bound"
            )
        actor_id = self._agent_actor_id()
        # Specialist-level action emission (intent).
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": "retrieve",
                "parameters": params,
            },
            role="author",
        )
        # Adapter-level action emission (wire-call) — adapter.call emits.
        # Pass attributing_actor_id so adapter attributes to the agent (not
        # the first manifest actor, which is curator-1 for the Sana fixture).
        adapter_response = adapter.call(
            "retrieve",
            {"query": query, "k": k},
            attributing_actor_id=actor_id,
        )
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

    def _handle_synthesize(self, params: dict) -> dict:
        """Emit a synthesis action event and a synthesis claim event.

        The claim's ``evidence-references`` come from explicit
        ``params['evidence-references']`` (when supplied — including an
        empty list for the negative-path test) or are derived by reading
        outcome-references of prior retrieve action events from the
        substrate event chain.
        """
        actor_id = self._agent_actor_id()
        # Synthesis action emission.
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="action",
            payload={
                "action-name": "synthesize",
                "parameters": {
                    k: v for k, v in params.items() if k != "evidence-references"
                },
            },
            role="author",
        )

        # Derive evidence-references: explicit (incl. empty) wins; else
        # gather all retrieve-action outcome-references from the chain.
        if "evidence-references" in params:
            refs = list(params["evidence-references"])
        else:
            refs = self._collect_retrieve_outcome_refs()

        synthesis_text = params.get(
            "synthesis", "synthesized statement (stub)"
        )
        claim_payload: dict = {"assertion": synthesis_text}
        # Always include evidence-references in the payload when the
        # specialist has them (even an empty list — sana-knowledge-shape
        # pre-citation treats empty as "missing"). The schema admits an
        # array; framework does not enforce non-empty (that's shape
        # policy's job per D53 §B + D38 §3).
        claim_payload["evidence-references"] = refs
        # Emit synthesis claim (subject to pre-citation gate).
        self._emit_event(
            actor_id=actor_id,
            payload_subtype="claim",
            payload=claim_payload,
            role="author",
        )
        return {
            "ok": True,
            "skill": "synthesize",
            "synthesis": synthesis_text,
            "evidence-references": refs,
            "stub": True,
        }

    def _collect_retrieve_outcome_refs(self) -> list[str]:
        """Pull outcome-references from prior retrieve-action events."""
        ws = self._workspace
        refs: list[str] = []
        for evt in ws.event_chain.by_payload_subtype("action"):
            payload = evt.get("payload") or {}
            if payload.get("action-name") == "retrieve":
                ref = payload.get("outcome-reference")
                if ref:
                    refs.append(ref)
        return refs


# ----------------------------------------------------------------------
# Registration helper — called from the test-fixture setup so this
# module does NOT side-effect import time. Idempotent.
# ----------------------------------------------------------------------


def register() -> None:
    """Register Sana-style runtime classes into framework registries.

    Idempotent. Adapters reuse ``MCPToolAdapter`` (already registered for
    ``mcp-server-ext:mcp-client``) — no new adapter class introduced.
    """
    from fresh_plan.runtime.shape import _SHAPE_CLASSES
    from fresh_plan.runtime.specialist import _SPECIALIST_CLASSES

    _SHAPE_CLASSES.setdefault("sana-knowledge-shape", SanaKnowledgeShape)
    _SPECIALIST_CLASSES.setdefault(
        "knowledge-agent-specialist", KnowledgeAgentSpecialist
    )


def unregister() -> None:
    """Remove Sana-style runtime classes from framework registries.

    Used in test teardown to leave registries clean for other tests.
    """
    from fresh_plan.runtime.shape import _SHAPE_CLASSES
    from fresh_plan.runtime.specialist import _SPECIALIST_CLASSES

    _SHAPE_CLASSES.pop("sana-knowledge-shape", None)
    _SPECIALIST_CLASSES.pop("knowledge-agent-specialist", None)
