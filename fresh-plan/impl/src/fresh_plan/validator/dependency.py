"""Dependency graph + cycle detection + version-range intersection.

Implements D32 (boot-time resolution) and D33 (version-conflict
resolution). The graph is built across the transitive closure of
workspace.composition.extensions[] following each manifest's
`dependencies.required-extensions[]`.

Version-range library: `node-semver` (PyPI; module `nodesemver`). It
matches npm-style range semantics exactly, which is what `_common.schema.json`'s
`version-range` $def specifies. Range intersection: npm/node-semver
treats whitespace-joined ranges as AND, so we intersect by joining
all ranges with whitespace and asking `max_satisfying(...)`.

Alternative considered: a minimal hand-rolled parser. Rejected because
the schema's regex admits caret/tilde/comparator forms; reimplementing
npm's resolution semantics is more code than just using the library.

PEP 440 (`packaging.specifiers`) does NOT match npm semantics
(different operator syntax, different pre-release rules) and is not
used.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import nodesemver


@dataclass
class DependencyGraph:
    """Directed graph used for cycle detection + load order.

    `nodes` is the set of extension ids. `edges` maps node → set of
    nodes that depend on it (so a topological sort yielding predecessors
    first uses these edges directly).
    """

    nodes: set[str] = field(default_factory=set)
    edges: dict[str, set[str]] = field(default_factory=dict)

    def add_node(self, node: str) -> None:
        self.nodes.add(node)
        self.edges.setdefault(node, set())

    def add_edge(self, predecessor: str, dependent: str) -> None:
        """Record that `dependent` depends on `predecessor`.

        After this call, the edge from predecessor → dependent (i.e.,
        load `predecessor` before `dependent`) exists.
        """
        self.add_node(predecessor)
        self.add_node(dependent)
        self.edges[predecessor].add(dependent)


def topological_sort(graph: DependencyGraph) -> tuple[list[str], list[str]]:
    """Kahn's algorithm. Returns (sorted_nodes, unsorted_remainder).

    If `unsorted_remainder` is empty, the graph is a DAG and
    `sorted_nodes` is a valid load order. Otherwise the remainder
    contains a cycle (extract via `find_cycle`).

    Ties among independent extensions are broken by alphabetical order
    per D32 §3 (determinism across boots).
    """
    # in-degree = number of predecessors required
    in_degree: dict[str, int] = {n: 0 for n in graph.nodes}
    for predecessor, dependents in graph.edges.items():
        for dep in dependents:
            in_degree[dep] = in_degree.get(dep, 0) + 1

    # Use sorted list as a poor-man's priority queue. n is small enough
    # (extensions per workspace; not a hot path) that O(n²) is fine.
    ready = sorted([n for n, deg in in_degree.items() if deg == 0])
    sorted_nodes: list[str] = []
    while ready:
        n = ready.pop(0)
        sorted_nodes.append(n)
        for succ in sorted(graph.edges.get(n, set())):
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                ready.append(succ)
                ready.sort()

    remainder = sorted(graph.nodes - set(sorted_nodes))
    return sorted_nodes, remainder


def find_cycle(graph: DependencyGraph, candidate_nodes: list[str]) -> list[str]:
    """DFS for a cycle among `candidate_nodes` (the unsorted remainder).

    Returns a list of node ids tracing the cycle (e.g.,
    ["ext-a", "ext-b", "ext-a"] for a 2-extension cycle), or [] if no
    cycle reachable from candidate_nodes (which should not happen if
    the topological sort failed).
    """
    if not candidate_nodes:
        return []
    in_remainder = set(candidate_nodes)
    visited: set[str] = set()
    # path is the recursion stack; index lets us slice the cycle out
    path: list[str] = []
    path_set: set[str] = set()

    def dfs(node: str) -> Optional[list[str]]:
        if node in path_set:
            # Found a back-edge: extract the cycle.
            i = path.index(node)
            return path[i:] + [node]
        if node in visited or node not in in_remainder:
            return None
        visited.add(node)
        path.append(node)
        path_set.add(node)
        for succ in sorted(graph.edges.get(node, set())):
            if succ not in in_remainder:
                continue
            result = dfs(succ)
            if result is not None:
                return result
        path.pop()
        path_set.discard(node)
        return None

    for start in sorted(candidate_nodes):
        if start in visited:
            continue
        result = dfs(start)
        if result is not None:
            return result
    return []


def intersect_ranges(ranges: list[str]) -> str:
    """Combine multiple npm-style ranges into one (AND).

    Per nodesemver: whitespace-separated comparators within one range
    string are AND-ed. `intersect_ranges([">=1.0.0", "<2.0.0"])` →
    `">=1.0.0 <2.0.0"`.
    """
    return " ".join(r.strip() for r in ranges if r.strip())


def max_satisfying(versions: list[str], range_str: str) -> Optional[str]:
    """Return the highest version in `versions` satisfying `range_str`, else None.

    Thin wrapper around nodesemver to centralize the loose/strict flag
    and isolate the dependency.
    """
    if not versions or not range_str:
        return None
    try:
        return nodesemver.max_satisfying(versions, range_str, False)
    except Exception:  # pragma: no cover — defensive
        return None


def satisfies(version: str, range_str: str) -> bool:
    """True iff `version` satisfies `range_str`."""
    try:
        return nodesemver.satisfies(version, range_str, False)
    except Exception:  # pragma: no cover — defensive
        return False


@dataclass
class VersionConflict:
    """A range-intersection failure or no-locally-available-version failure (D33)."""

    extension_id: str
    declarers: list[tuple[str, str]]  # list of (declarer-ext-id, range)
    reason: str
    available_versions: list[str] = field(default_factory=list)


def resolve_versions(
    requirements: dict[str, list[tuple[str, str]]],
    available: dict[str, list[str]],
) -> tuple[dict[str, str], list[VersionConflict]]:
    """Resolve version selections per D33 §B.

    `requirements`: ext-id → list of (declarer-ext-id, range-string).
    `available`: ext-id → list of versions present on disk.

    Returns (selected, conflicts). `selected` is ext-id → chosen
    version. For each extension with at least one range declared,
    intersect ranges, pick the highest available version satisfying the
    intersection; on failure record a VersionConflict.
    """
    selected: dict[str, str] = {}
    conflicts: list[VersionConflict] = []

    for ext_id, declarations in requirements.items():
        if not declarations:
            continue
        combined = intersect_ranges([rng for _, rng in declarations])
        versions = available.get(ext_id, [])
        if not versions:
            # Extension absent from disk entirely: this is a resolution
            # failure, not a version conflict (D33 §B distinguishes
            # "intersection empty / no version in intersection" from
            # "extension simply not found"). Caller surfaces it as a
            # resolution failure; skip recording a version-conflict here.
            continue
        # First test: does any version satisfy at all? If not, distinguish
        # "intersection empty" from "intersection non-empty but no local hit".
        any_satisfying = [v for v in versions if satisfies(v, combined)]
        if any_satisfying:
            chosen = max_satisfying(versions, combined)
            if chosen is None:  # pragma: no cover — defensive
                conflicts.append(
                    VersionConflict(
                        extension_id=ext_id,
                        declarers=list(declarations),
                        reason="version selection failed",
                        available_versions=versions,
                    )
                )
            else:
                selected[ext_id] = chosen
        else:
            # Could be empty intersection OR no local version inside a
            # non-empty intersection. Distinguish by checking each range
            # individually against the versions: if no version satisfies
            # ALL ranges, but at least one satisfies each range alone,
            # the intersection is non-empty in semver space but no local
            # version is in it (rare); otherwise intersection is empty.
            per_range_hits = [
                any(satisfies(v, rng) for v in versions)
                for _, rng in declarations
            ]
            if all(per_range_hits):
                reason = (
                    "no locally-available version satisfies the intersection "
                    "of declared ranges"
                )
            else:
                reason = "version-range intersection is empty"
            conflicts.append(
                VersionConflict(
                    extension_id=ext_id,
                    declarers=list(declarations),
                    reason=reason,
                    available_versions=versions,
                )
            )

    return selected, conflicts
