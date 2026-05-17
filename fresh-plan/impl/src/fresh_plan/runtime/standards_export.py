"""Standards-compatibility export converters — D77 §B (closes Phase C C9).

Per D77 §B + D68 §A C9 + D24 standards-compat tracker: pure conversion
functions from the fresh-plan event envelope (D10 + D23) to two industry
standards:

  - **CloudEvents 1.0** (CNCF spec; https://cloudevents.io/) — generic
    event envelope for cross-system event propagation. Mapping: fresh-plan
    ``event.id`` ↔ CloudEvents ``id``; ``workspace://<workspace-id>`` ↔
    ``source``; ``event.payload-subtype`` ↔ ``type``; ``event.payload`` ↔
    ``data``; constant ``application/json`` ↔ ``datacontenttype``;
    ``event.timestamp`` ↔ ``time``; CloudEvents ``specversion='1.0'``.

  - **W3C PROV-DM / PROV-JSON** (https://www.w3.org/TR/prov-dm/ +
    https://www.w3.org/TR/prov-json/) — provenance/attribution standard.
    Mapping: fresh-plan ``event`` ↔ ``prov:Activity``; ``event.actors[].id``
    ↔ ``prov:Agent``; ``event.actors[]`` × ``event.id`` ↔
    ``prov:wasAttributedTo`` (activity-attribution relation).

Per D77 §A: **NON-BREAKING** — fresh-plan event envelope is UNCHANGED.
These are EXPORT-ONLY (one-way) serializations invoked at export time;
the canonical in-memory shape and the persisted JSONL stay fresh-plan's
own envelope per D10 + D43.

Per D45 + D77 §B triad (D77 §B.2):

  - **Detection** — ``to_cloudevents`` and ``event_chain_to_prov_json``
    raise ``ValueError`` when a fresh-plan event is missing one of its
    required envelope fields (``id`` / ``timestamp`` / ``payload-subtype``
    / ``actors`` / ``payload``). Per "no silent substitution" discipline:
    a malformed event is surfaced at conversion time rather than producing
    a CloudEvent / PROV record with missing canonical fields.
  - **Surface** — direct callers see ``ValueError`` with a structured
    message naming the missing field + the offending event id (when
    available). Adapter callers (``ProvJsonExportAdapter.call``) catch
    this and re-wrap as ``AdapterCallError(category='protocol-error')``
    per D48 §D D-3 starter category vocabulary REUSE.
  - **Recovery** — caller decides per call site: export adapter aborts
    + surfaces the failure to the operator; in-test scenarios assert on
    the surfaced ``ValueError`` directly.

Scope cuts (per D77 §D):

  - PROV-DM library dependency — D77 ships a hand-rolled PROV-JSON
    serializer (JSON-LD shape; trivial to construct by hand) to avoid
    pulling a heavy ``prov`` dependency for export-only purposes. Future
    PROV-O / round-trip integration could switch to the ``prov`` library
    via a same-module adaption layer.
  - prov:Entity per-payload-subtype mapping — the simple mapping
    (Activity / Agent / wasAttributedTo) covers the per D77 §B locked
    contract. Per-payload-subtype prov:Entity assertion content + per-
    payload prov:wasGeneratedBy is deferred per D77 §D D-3 deployment-
    specific mapping work.
  - OpenTelemetry / AsyncAPI / Activity Streams mappings — D24 standards-
    compat tracker carry-over; future export adapters register at the
    same ``prov-json-export-ext`` extension pattern per D29 namespacing.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


# ----------------------------------------------------------------------
# PROV-JSON canonical namespace
# ----------------------------------------------------------------------

PROV_NAMESPACE = "http://www.w3.org/ns/prov#"


# Fresh-plan event required envelope fields (D10 + D23 — schema.event.json).
#
# NOTE: this list is intentionally NARROWER than the canonical event schema
# (which also requires `prev-event`) BY DESIGN — this validator runs at
# EXPORT time, where chain-integrity (prev-event linkage) has already been
# enforced upstream (B1 validator + per-event checks + AEGIS integrity
# protocol per D40 §B + D76). The exporter does not consume prev-event in
# either the CloudEvents or PROV-JSON shape, so requiring it here would
# only surface a redundant gate. A cold reader spotting the omission
# should NOT treat it as a hole; the chain-integrity contract is enforced
# elsewhere per D45 detection-surface-recovery layering.
_REQUIRED_EVENT_FIELDS = (
    "id",
    "timestamp",
    "payload-subtype",
    "actors",
    "payload",
)


def _validate_event_envelope(event: dict, *, context: str) -> None:
    """Per D77 §B.2 Detection: raise ValueError on missing required field.

    No silent substitution — a malformed event is surfaced at conversion
    time rather than producing a downstream record with missing fields.

    Narrower than the canonical event.schema.json (omits `prev-event`) BY
    DESIGN — see _REQUIRED_EVENT_FIELDS module-level comment.
    """
    if not isinstance(event, dict):
        raise ValueError(
            f"{context}: event must be a dict (got {type(event).__name__})"
        )
    missing = [f for f in _REQUIRED_EVENT_FIELDS if f not in event]
    if missing:
        event_id = event.get("id", "<no-id>")
        raise ValueError(
            f"{context}: event id={event_id!r} missing required "
            f"envelope field(s): {missing}"
        )
    actors = event.get("actors")
    if not isinstance(actors, list) or len(actors) < 1:
        raise ValueError(
            f"{context}: event id={event.get('id')!r} `actors` must be a "
            f"non-empty list (got {type(actors).__name__})"
        )


# ----------------------------------------------------------------------
# CloudEvents 1.0 conversion (per CNCF cloudevents/sdk-python v2.0.0)
# ----------------------------------------------------------------------


def to_cloudevents(event: dict, *, workspace_id: Optional[str] = None):
    """Convert a fresh-plan event (dict) to a cloudevents.v1.http.CloudEvent.

    Per D77 §B.1 mapping (CloudEvents 1.0):

      - ``id`` ← ``event.id``
      - ``source`` ← ``workspace://<workspace-id>`` when ``workspace_id``
        is provided, else ``workspace://unknown`` (export-only contract;
        the source is a CloudEvents required attribute and the workspace
        is the only meaningful authority for fresh-plan events). Callers
        with workspace context SHOULD supply ``workspace_id``.
      - ``type`` ← ``event.payload-subtype``
      - ``specversion`` ← ``1.0`` (SDK default)
      - ``datacontenttype`` ← ``application/json``
      - ``time`` ← ``event.timestamp`` (ISO-8601 UTC per D10)
      - ``data`` ← ``event.payload`` (the subtype-specific payload dict)

    Per D77 §B.2 Detection: raises ``ValueError`` when ``event`` is missing
    a required envelope field (id / timestamp / payload-subtype / actors /
    payload).

    Args:
        event: fresh-plan event dict matching ``schemas/event.schema.json``.
        workspace_id: optional workspace identifier for the
            ``source`` attribute. Required by CloudEvents spec; defaults
            to ``unknown`` if absent.

    Returns:
        ``cloudevents.v1.http.CloudEvent`` instance carrying the mapped
        attributes + data.

    Raises:
        ValueError: when ``event`` is missing a required envelope field.
    """
    from cloudevents.v1.http import CloudEvent

    _validate_event_envelope(event, context="to_cloudevents")

    source_id = workspace_id or "unknown"
    attributes = {
        "id": event["id"],
        "source": f"workspace://{source_id}",
        "type": event["payload-subtype"],
        "datacontenttype": "application/json",
        "time": event["timestamp"],
    }
    return CloudEvent(attributes, event["payload"])


# ----------------------------------------------------------------------
# W3C PROV-DM / PROV-JSON conversion (hand-rolled JSON-LD shape)
# ----------------------------------------------------------------------


def event_chain_to_prov_json(
    events: list[dict], workspace_id: str
) -> dict:
    """Convert a fresh-plan event chain to a PROV-JSON document (dict).

    Per D77 §B.1 mapping (W3C PROV-DM via PROV-JSON serialization):

      - Each fresh-plan event ↦ one ``prov:Activity`` with
        - ``prov:startTime`` ← event.timestamp
        - ``prov:type`` ← event.payload-subtype
        - identifier ← ``"fresh-plan:event:<event-id>"``
      - Each unique ``actor.id`` across all events ↦ one ``prov:Agent``
        with identifier ``"fresh-plan:actor:<actor-id>"``.
      - Each (actor, event) pair ↦ one ``prov:wasAttributedTo`` relation
        binding the Activity to the Agent.
      - The workspace itself is also surfaced as a ``prov:Agent``
        (identifier ``"fresh-plan:workspace:<workspace-id>"``); each
        Activity carries an attribution to the workspace agent.

    Per W3C PROV-JSON spec (https://www.w3.org/TR/prov-json/): the document
    is a JSON object with the top-level keys ``prefix`` (namespace map),
    ``activity``, ``agent``, ``wasAttributedTo`` (relation map). Empty
    event chain yields a document with zero activities (no failure).

    Per D77 §B.2 Detection: raises ``ValueError`` when any event is
    missing a required envelope field.

    Args:
        events: ordered list of fresh-plan event dicts.
        workspace_id: workspace identifier (becomes the per-document
            workspace Agent + appears in attributions).

    Returns:
        dict in PROV-JSON shape.

    Raises:
        ValueError: when any event is missing a required envelope field
            OR ``workspace_id`` is empty.
    """
    if not workspace_id:
        raise ValueError(
            "event_chain_to_prov_json: workspace_id must be a non-empty string"
        )

    activities: dict[str, dict] = {}
    agents: dict[str, dict] = {}
    attributions: dict[str, dict] = {}

    # Always include the workspace agent (even for empty chains — gives
    # the PROV-JSON document an anchored subject identity per workspace).
    workspace_agent_id = f"fresh-plan:workspace:{workspace_id}"
    agents[workspace_agent_id] = {
        "prov:type": "workspace",
        "prov:label": workspace_id,
    }

    for index, event in enumerate(events):
        _validate_event_envelope(
            event, context=f"event_chain_to_prov_json[{index}]"
        )
        event_id = event["id"]
        activity_id = f"fresh-plan:event:{event_id}"
        activities[activity_id] = {
            "prov:startTime": event["timestamp"],
            "prov:type": event["payload-subtype"],
        }

        for actor in event["actors"]:
            actor_id = actor.get("id")
            if not actor_id:
                raise ValueError(
                    f"event_chain_to_prov_json[{index}]: event id="
                    f"{event_id!r} has actor without `id` field"
                )
            agent_id = f"fresh-plan:actor:{actor_id}"
            if agent_id not in agents:
                agents[agent_id] = {
                    "prov:type": "actor",
                    "prov:label": actor_id,
                }

            # One attribution per (actor, event). Key shape:
            # "<event-id>_<actor-id>" (relation identifier — PROV-JSON
            # convention is any unique key under wasAttributedTo).
            relation_id = f"fresh-plan:attr:{event_id}_{actor_id}"
            attributions[relation_id] = {
                "prov:activity": activity_id,
                "prov:agent": agent_id,
            }

        # Each activity also attributed to the workspace agent (anchors
        # every activity to its workspace authority per fresh-plan's
        # workspace-scoped event chain D10).
        ws_attr_id = f"fresh-plan:attr:{event_id}_workspace"
        attributions[ws_attr_id] = {
            "prov:activity": activity_id,
            "prov:agent": workspace_agent_id,
        }

    return {
        "prefix": {
            "prov": PROV_NAMESPACE,
            "fresh-plan": "https://pbs-bureau.dev/fresh-plan/prov#",
        },
        "activity": activities,
        "agent": agents,
        "wasAttributedTo": attributions,
    }


def write_prov_json(
    events: list[dict], workspace_id: str, output_path: Path
) -> dict:
    """Convert + persist PROV-JSON to ``output_path`` (file I/O).

    Per D77 §B.2 Detection: file I/O failures raise OSError; conversion
    failures raise ValueError. ``ProvJsonExportAdapter.call`` re-wraps
    both as ``AdapterCallError`` per category vocabulary.

    Args:
        events: ordered list of fresh-plan event dicts.
        workspace_id: workspace identifier.
        output_path: filesystem path the JSON document is written to.

    Returns:
        the same PROV-JSON dict returned by ``event_chain_to_prov_json``.

    Raises:
        ValueError: per ``event_chain_to_prov_json``.
        OSError: file IO failure (read-only directory, permission denied,
            disk full).
    """
    prov_doc = event_chain_to_prov_json(events, workspace_id)
    output_path.write_text(json.dumps(prov_doc, indent=2, sort_keys=True))
    return prov_doc
