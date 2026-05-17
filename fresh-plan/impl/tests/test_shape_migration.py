"""Tests for D54 §B.1 shape-migration classifier (Phase B forward-bar).

Per D54 §C: three pure-function tests covering the three migration-safety
categories defined by §B.1 table:

  (i)   safe-in-place loosening
  (ii)  breaking removal
  (iii) new-era tightening

The classifier is pure-function over (prior_spec, new_spec); no boot.py
integration in this entry (deferred to Phase C+ per §D D-1).
"""
from __future__ import annotations

from fresh_plan.validator.shape_migration import classify_shape_change


def test_safe_in_place_loosening_authority_binding() -> None:
    """D54 §B.1 — loosening an authority-binding (relaxing required-role) is safe-in-place.

    Pioneer-instance canonical case: PBS-Schulz high-human-involvement v1
    → mostly-automated v2 = authority-bindings[] LOOSENING (existing
    requirements widen to admit agent-actor).
    """
    prior = {
        "id": "test-shape",
        "version": "1.0.0",
        "authority-bindings": [
            {
                "payload-subtype": "claim",
                "required-role": "attester",
                "required-actor-subtype": "human-actor",
            }
        ],
    }
    new = {
        "id": "test-shape",
        "version": "1.1.0",
        "authority-bindings": [
            {
                "payload-subtype": "claim",
                "required-role": "attester",
                # required-actor-subtype REMOVED (widened to any actor) → loosening.
            }
        ],
    }
    changes = classify_shape_change(prior, new)

    # Find the authority-bindings entry.
    ab_entries = [c for c in changes if c[0].startswith("authority-bindings.")]
    assert len(ab_entries) == 1
    slot, prior_val, new_val, category = ab_entries[0]
    assert category == "safe-in-place", (
        f"authority-binding loosening (relaxing required-actor-subtype) "
        f"should be safe-in-place; got {category!r}"
    )


def test_breaking_removal_required_capability() -> None:
    """D54 §B.1 — removing a required-capability is breaking (existing impl may no longer be valid)."""
    prior = {
        "id": "test-shape",
        "version": "1.0.0",
        "required-capabilities": ["substrate-skills", "rag-retrieval"],
    }
    new = {
        "id": "test-shape",
        "version": "2.0.0",
        "required-capabilities": ["substrate-skills"],  # rag-retrieval removed
    }
    changes = classify_shape_change(prior, new)

    # Find the required-capabilities entry for the removed capability.
    cap_removals = [
        c
        for c in changes
        if c[0].startswith("required-capabilities.") and c[2] is None
    ]
    assert len(cap_removals) == 1, (
        f"expected one required-capabilities removal entry; got {cap_removals}"
    )
    slot, prior_val, new_val, category = cap_removals[0]
    assert category == "breaking", (
        f"required-capability removal should be breaking; got {category!r}"
    )
    assert prior_val == "rag-retrieval"


def test_new_era_tightening_actor_requirements_min() -> None:
    """D54 §B.1 — tightening actor-requirements (min upward) is new-era.

    Existing actors stand under prior shape; new events must satisfy the
    tightened cardinality under D52 §B.1 enforcement.
    """
    prior = {
        "id": "test-shape",
        "version": "1.0.0",
        "actor-requirements": {
            "human-actor": {"min": 1, "max": 5},
        },
    }
    new = {
        "id": "test-shape",
        "version": "1.1.0",
        "actor-requirements": {
            "human-actor": {"min": 2, "max": 5},  # min tightened upward
        },
    }
    changes = classify_shape_change(prior, new)

    ar_entries = [c for c in changes if c[0].startswith("actor-requirements.")]
    assert len(ar_entries) == 1
    slot, prior_val, new_val, category = ar_entries[0]
    assert category == "new-era", (
        f"actor-requirements min tightening should be new-era; got {category!r}"
    )
    assert prior_val == {"min": 1, "max": 5}
    assert new_val == {"min": 2, "max": 5}
