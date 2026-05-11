"""Tests for fresh_plan.validator.dependency.

Covers D32 (cycle detection, topological sort) + D33 (version-range
intersection and conflict resolution).
"""
from __future__ import annotations

import pytest

from fresh_plan.validator.dependency import (
    DependencyGraph,
    find_cycle,
    intersect_ranges,
    max_satisfying,
    resolve_versions,
    satisfies,
    topological_sort,
)


# --- Cycle detection (D32 §2) -----------------------------------------------


def test_topological_sort_simple_dag():
    """3-extension DAG: A → B → C; load order = [A, B, C]."""
    g = DependencyGraph()
    g.add_edge("a", "b")  # b depends on a
    g.add_edge("b", "c")  # c depends on b
    sorted_, remainder = topological_sort(g)
    assert remainder == []
    assert sorted_ == ["a", "b", "c"]


def test_topological_sort_independent_alphabetical(tmp_path):
    """Independent extensions sorted alphabetically per D32 §3 determinism."""
    g = DependencyGraph()
    for n in ["zebra", "apple", "mango"]:
        g.add_node(n)
    sorted_, remainder = topological_sort(g)
    assert remainder == []
    assert sorted_ == ["apple", "mango", "zebra"]


def test_cycle_detection_two_extensions():
    """D32 worked example: ext-a → ext-b → ext-a."""
    g = DependencyGraph()
    g.add_edge("ext-a", "ext-b")
    g.add_edge("ext-b", "ext-a")
    sorted_, remainder = topological_sort(g)
    assert remainder, "expected unsorted remainder due to cycle"
    cycle = find_cycle(g, remainder)
    # Cycle should include both nodes returning to the start
    assert len(cycle) >= 3
    assert cycle[0] == cycle[-1]
    assert set(cycle) == {"ext-a", "ext-b"}


def test_cycle_detection_three_extensions():
    """3-extension cycle: A → B → C → A."""
    g = DependencyGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    sorted_, remainder = topological_sort(g)
    assert remainder
    cycle = find_cycle(g, remainder)
    assert cycle[0] == cycle[-1]
    assert set(cycle) >= {"a", "b", "c"}


# --- Version-range intersection (D33 §B) ------------------------------------


def test_satisfies_basic():
    assert satisfies("1.0.0", ">=1.0.0")
    assert not satisfies("0.9.0", ">=1.0.0")
    assert satisfies("1.5.0", ">=1.0.0 <2.0.0")
    assert not satisfies("2.0.0", ">=1.0.0 <2.0.0")


def test_max_satisfying_returns_highest_in_range():
    versions = ["1.0.0", "1.2.0", "1.5.0", "2.0.0"]
    assert max_satisfying(versions, ">=1.0.0 <2.0.0") == "1.5.0"
    assert max_satisfying(versions, ">=1.0.0") == "2.0.0"
    assert max_satisfying(versions, ">=3.0.0") is None


def test_intersect_ranges_combines_with_whitespace():
    assert intersect_ranges([">=1.0.0", "<2.0.0"]) == ">=1.0.0 <2.0.0"


def test_resolve_versions_compatible_ranges_pick_highest():
    """D33: two declarers, compatible ranges → highest version in intersection."""
    requirements = {
        "dep": [
            ("workspace", ">=1.0.0"),
            ("other-ext", "<2.0.0"),
        ]
    }
    available = {"dep": ["1.0.0", "1.2.0", "1.5.0", "2.0.0"]}
    selected, conflicts = resolve_versions(requirements, available)
    assert conflicts == []
    assert selected["dep"] == "1.5.0"


def test_resolve_versions_empty_intersection_yields_conflict():
    """D33: two declarers with incompatible ranges → version-conflict."""
    requirements = {
        "dep": [
            ("consumer-a", ">=1.0.0 <2.0.0"),
            ("consumer-b", ">=2.0.0"),
        ]
    }
    available = {"dep": ["1.0.0", "1.5.0", "2.0.0"]}
    selected, conflicts = resolve_versions(requirements, available)
    assert "dep" not in selected
    assert len(conflicts) == 1
    c = conflicts[0]
    assert c.extension_id == "dep"
    assert len(c.declarers) == 2
    declarers_ids = {d[0] for d in c.declarers}
    assert declarers_ids == {"consumer-a", "consumer-b"}


def test_resolve_versions_no_available_versions_inside_range():
    """Intersection non-empty in semver-space, but no local version inside it."""
    requirements = {
        "dep": [
            ("workspace", ">=3.0.0"),
        ]
    }
    available = {"dep": ["1.0.0", "2.0.0"]}
    selected, conflicts = resolve_versions(requirements, available)
    assert "dep" not in selected
    assert len(conflicts) == 1
    assert "intersection" in conflicts[0].reason or "satisfies" in conflicts[0].reason
