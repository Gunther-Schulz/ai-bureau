#!/usr/bin/env python3
"""
PreToolUse hook: architectural commit gate.

Blocks Write/Edit operations on architectural artifacts unless required
preparatory Reads happened in the current session. Structural enforcement
of execution-fidelity discipline per drafts/execution-fidelity.md +
DISCIPLINES.md Disciplines 1, 3, 9, 10.

Wired via plugin.json hooks section. Receives JSON via stdin per Claude
Code hook protocol; reads transcript_path from input to scan tool_use
history; returns exit 0 (allow) or 2 (block) with stderr message.

Failure modes covered (per drafts/execution-fidelity.md):
- Disguise #1 Compaction pattern-matching: skill-freshness check forces
  re-Read post-compact
- Disguise #4 Skipping steps that feel covered: blocking forces explicit
  Read at write boundary
- Disguise #5 Substituting AI judgment for codified rule: hook is the
  rule; AI judgment can't bypass
- Provenance hygiene drift: Check 4 blocks narrative-breadcrumb regex
  matches in canonical content (Layer 0/1/2/3) — structural enforcement
  upgrade for coherence-audit Lens 5 v0.2.1 prose discipline that kept
  recurring across sessions

Honest limitations:
- Detects FILE-READ-HAPPENED, not GREENFIELD-EVALUATION-HAPPENED
- AI could Read perfunctorily; quality remains convention-grade
- Hook fires at write-boundary; doesn't gate Round 2 sharpening
  semantically (no per-Round mechanical signal)
- Check 4 regex catches highest-frequency narrative patterns (session-N
  / AMENDED session / this-commit / this-session / earlier-in-session);
  cannot catch semantic narrative without keywords; AI can perturb to
  evade at cost of unnatural language

Freshness-window strategy: whole-session scan. Claude Code's
transcript_path is per-session per the hooks API (verified: each
transcript JSONL has a single sessionId across all events). We scan ALL
events in the transcript — no call-count window. This avoids the
cascade-load failure mode where prep Reads done at session start get
pushed out of a fixed-size window before a long architectural cascade
(Edits + Bash + Reads + sub-agent calls) completes.

Per session-16 (commit 55c016c) escalation from procedural redundancy
(B+C: Discipline 10 + Round 1 checklist) to structural enforcement (A:
this hook) due to recurrent META-failure pattern.
"""

import json
import re
import sys
from pathlib import Path
from typing import Iterable

# Architectural artifact path patterns (relative to repo root).
# Hook fires Strict on these paths.
ARCHITECTURAL_PATTERNS = [
    re.compile(r"(^|/)arch/[^/]+\.md$"),
    re.compile(r"(^|/)docs/decisions/[^/]+\.md$"),
    re.compile(r"(^|/)ARCHITECTURE\.md$"),
    re.compile(r"(^|/)GLOSSARY\.md$"),
    re.compile(r"(^|/)MAINTENANCE\.md$"),
    re.compile(r"(^|/)DISCIPLINES\.md$"),
]

# Canonical-content paths where provenance breadcrumbs are forbidden
# (Check 4). Subset of ARCHITECTURAL_PATTERNS — EXCLUDES docs/decisions/*
# because Layer 4 DRs are the explicit narrative-home per MAINTENANCE.md
# DR template Sharpening provenance section. Also excludes DISCIPLINES.md
# (Layer 0 anchor; may legitimately reference canonical exemplars per
# Discipline 10 wording).
CANONICAL_CONTENT_PATTERNS = [
    re.compile(r"(^|/)arch/[^/]+\.md$"),
    re.compile(r"(^|/)ARCHITECTURE\.md$"),
    re.compile(r"(^|/)GLOSSARY\.md$"),
    re.compile(r"(^|/)MAINTENANCE\.md$"),
]

# Required reads per architectural commit.
REQUIRED_SKILL = "plugin/skills/decision-design-sharpening/SKILL.md"
REQUIRED_PROFILE_INDEX = "profiles/INDEX.md"
PROFILE_GLOB_PATTERN = re.compile(r"(^|/)profiles/[A-Z]\d?[a-z]?-[^/]+\.md$")
ARCHIVE_PATH_PATTERN = re.compile(r"archive/[^\s\"'`)]+\.md")

# High-signal narrative-breadcrumb regex patterns. Forbidden in canonical
# content (Layer 0/1/2/3) per ARCHITECTURE.md cross-cutting principle
# "Provenance hygiene" + coherence-audit Lens 5 v0.2.1. Provenance lives
# in HANDOFF + git log + commit messages + DRs — not canonical content.
#
# Iterative pattern set: tune as real false-positives surface. Initial
# scope = highest-frequency natural-failure-mode patterns from session-16
# substrate cargo-cult + session-18 cascade pollution.
BREADCRUMB_PATTERNS: list[tuple["re.Pattern[str]", str]] = [
    (re.compile(r"\bsession[\s\-]\d+\b", re.IGNORECASE),
     "session-N reference"),
    (re.compile(r"\bAMENDED session\b", re.IGNORECASE),
     "AMENDED session marker"),
    (re.compile(r"\b(?:in )?this commit\b", re.IGNORECASE),
     "this-commit reference"),
    (re.compile(r"\b(?:in )?this session\b", re.IGNORECASE),
     "this-session reference"),
    (re.compile(r"\bearlier in (?:the )?session\b", re.IGNORECASE),
     "earlier-in-session reference"),
]

# Minimum profile cluster members read for high-impact decisions.
MIN_PROFILE_READS = 3


def is_architectural_artifact(path: str) -> bool:
    return any(p.search(path) for p in ARCHITECTURAL_PATTERNS)


def is_canonical_content(path: str) -> bool:
    """Layer 0/1/2/3 canonical content where provenance breadcrumbs are
    forbidden. Excludes docs/decisions/* (Layer 4 DRs)."""
    return any(p.search(path) for p in CANONICAL_CONTENT_PATTERNS)


def extract_write_content(tool_input: dict) -> str:
    """Extract content being written/edited. Supports Edit (new_string),
    Write (content), and MultiEdit (edits[].new_string)."""
    if not isinstance(tool_input, dict):
        return ""
    content = tool_input.get("content")
    if isinstance(content, str):
        return content
    new_string = tool_input.get("new_string")
    if isinstance(new_string, str):
        return new_string
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        parts = []
        for edit in edits:
            if isinstance(edit, dict):
                ns = edit.get("new_string")
                if isinstance(ns, str):
                    parts.append(ns)
        return "\n".join(parts)
    return ""


def find_breadcrumbs(content: str) -> list[tuple[str, str]]:
    """Scan content for narrative-breadcrumb patterns. Return list of
    (matched_text, pattern_label) tuples (deduplicated by caller)."""
    if not isinstance(content, str) or not content:
        return []
    found = []
    for pattern, label in BREADCRUMB_PATTERNS:
        for m in pattern.finditer(content):
            found.append((m.group(0), label))
    return found


def read_transcript_events(transcript_path: str) -> list[dict]:
    """Read JSONL transcript file; return list of message events."""
    events = []
    try:
        with open(transcript_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except (OSError, IOError):
        pass
    return events


def extract_read_paths(events: Iterable[dict]) -> list[str]:
    """Scan ALL events for Read tool_use; extract file_path arguments.

    Whole-session scan: Claude Code's transcript_path is per-session per
    the hooks API (each transcript JSONL has a single sessionId across
    all events), so the entire transcript IS one session. No call-count
    window needed; this avoids the cascade-load failure mode where prep
    Reads done at session start get pushed out of a fixed-size window
    before a long architectural cascade completes.
    """
    read_paths = []
    for event in events:
        msg = event.get("message", {}) if isinstance(event, dict) else {}
        content = msg.get("content", []) if isinstance(msg, dict) else []
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            if block.get("name") != "Read":
                continue
            inp = block.get("input", {})
            if isinstance(inp, dict):
                fp = inp.get("file_path") or inp.get("filePath")
                if isinstance(fp, str):
                    read_paths.append(fp)
    return read_paths


def normalize_path(path: str) -> str:
    """Strip leading slashes; lowercase; treat absolute paths as relative."""
    p = path.lstrip("/")
    parts = p.split("/")
    # Match by tail (e.g., "GLOSSARY.md" matches "/abs/path/GLOSSARY.md")
    return p


def path_matches(read_path: str, target_suffix: str) -> bool:
    return read_path.endswith(target_suffix) or read_path.endswith("/" + target_suffix)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Malformed input; fail open (don't block on tool error)
        return 0

    tool_name = payload.get("tool_name") or payload.get("toolName") or ""
    tool_input = payload.get("tool_input") or payload.get("toolInput") or {}
    transcript_path = (
        payload.get("transcript_path")
        or payload.get("transcriptPath")
        or payload.get("session", {}).get("transcript_path", "")
    )

    if tool_name not in ("Edit", "Write", "MultiEdit"):
        return 0

    target = tool_input.get("file_path") or tool_input.get("filePath") or ""
    if not target or not is_architectural_artifact(target):
        return 0

    # This is an architectural-artifact write. Check preparatory Reads.
    # Whole-session scan: transcript_path is per-session per Claude Code
    # hooks API; we look at ALL events in the transcript (no call-count
    # window — avoids cascade-load eviction of prep Reads).
    events = read_transcript_events(transcript_path) if transcript_path else []
    session_reads = extract_read_paths(events)

    blocks: list[str] = []

    # Check 1: skill freshness
    if not any(path_matches(rp, REQUIRED_SKILL) for rp in session_reads):
        blocks.append(
            f"BLOCK: decision-design-sharpening SKILL.md not Read in current "
            f"session.\n"
            f"  Required: Read tool on `{REQUIRED_SKILL}` before architectural "
            f"commit.\n"
            f"  Per: DISCIPLINES.md Discipline 1 (skill+profile sub-section)."
        )

    # Check 2: profile freshness (architectural artifacts in arch/ or new DRs)
    is_high_impact = any(
        re.search(r"(^|/)arch/[^/]+\.md$", target)
        or re.search(r"(^|/)docs/decisions/[^/]+\.md$", target)
        for _ in [0]
    )
    if is_high_impact:
        profile_reads = [rp for rp in session_reads if PROFILE_GLOB_PATTERN.search(rp)]
        index_read = any(path_matches(rp, REQUIRED_PROFILE_INDEX) for rp in session_reads)
        if len(profile_reads) < MIN_PROFILE_READS or not index_read:
            blocks.append(
                f"BLOCK: profile-anchored validation requires Read of "
                f"`{REQUIRED_PROFILE_INDEX}` + ≥{MIN_PROFILE_READS} cluster "
                f"members in current session. "
                f"Found: {len(profile_reads)} profile reads, "
                f"INDEX={'yes' if index_read else 'no'}.\n"
                f"  Per: DISCIPLINES.md Discipline 3 profile-anchored validation."
            )

    # Check 3: archive-citation cross-check (greenfield evaluation)
    write_content = extract_write_content(tool_input)
    if write_content:
        cited_archive_paths = set(ARCHIVE_PATH_PATTERN.findall(write_content))
        unread_citations = []
        for cited in cited_archive_paths:
            if not any(rp.endswith(cited) or rp.endswith("/" + cited) for rp in session_reads):
                unread_citations.append(cited)
        if unread_citations:
            citations_list = "\n".join(f"    - {c}" for c in sorted(unread_citations))
            blocks.append(
                f"BLOCK: archive sources cited but not Read in current session "
                f"(greenfield-evaluation requires direct Read per "
                f"DISCIPLINES.md Discipline 10):\n{citations_list}"
            )

    # Check 4: provenance hygiene on canonical content (Layer 0/1/2/3).
    # Per ARCHITECTURE.md cross-cutting principle "Provenance hygiene" +
    # coherence-audit Lens 5 v0.2.1 + MAINTENANCE.md 5-layer doc model:
    # narrative breadcrumbs (session-N / AMENDED session / this-commit /
    # this-session / earlier-in-session) belong in HANDOFF + git log +
    # commit messages + DRs, NOT canonical content.
    #
    # Honest limitations: pattern-based regex catches highest-frequency
    # natural-failure-mode (numeric session/round/commit refs). Cannot
    # catch semantic narrative without keywords. AI can perturb to evade
    # ("session seventeen") at cost of unnatural language. Tune patterns
    # as real false-positives surface during work.
    if is_canonical_content(target) and write_content:
        breadcrumbs = find_breadcrumbs(write_content)
        if breadcrumbs:
            unique = sorted({(text.lower(), label, text) for text, label in breadcrumbs})
            details = "\n".join(
                f"    - \"{original}\" ({label})"
                for _, label, original in unique
            )
            blocks.append(
                f"BLOCK: provenance breadcrumbs in canonical content "
                f"(Layer 0/1/2/3) violate provenance-hygiene discipline.\n"
                f"  Per: ARCHITECTURE.md cross-cutting principle "
                f"\"Provenance hygiene\" + MAINTENANCE.md 5-layer doc "
                f"model (provenance lives in HANDOFF + git log + commit "
                f"messages + DRs — NOT canonical content).\n"
                f"  Found in write content:\n{details}\n"
                f"  Fix: move narrative to HANDOFF / git commit message / "
                f"DR Layer 4 (Sharpening provenance section). Keep DR "
                f"cross-references for rationale anchoring (e.g., \"per "
                f"`docs/decisions/<X>.md` Step Y\") — those are "
                f"legitimate references, not breadcrumbs."
            )

    if blocks:
        msg = "\n\n".join(blocks)
        msg += (
            "\n\nResolve by Reading the named files via Read tool, then retry "
            "the Edit/Write."
        )
        print(msg, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
