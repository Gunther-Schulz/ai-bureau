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

Honest limitations:
- Detects FILE-READ-HAPPENED, not GREENFIELD-EVALUATION-HAPPENED
- AI could Read perfunctorily; quality remains convention-grade
- Hook fires at write-boundary; doesn't gate Round 2 sharpening
  semantically (no per-Round mechanical signal)

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

# Required reads per architectural commit.
REQUIRED_SKILL = "plugin/skills/decision-design-sharpening/SKILL.md"
REQUIRED_PROFILE_INDEX = "profiles/INDEX.md"
PROFILE_GLOB_PATTERN = re.compile(r"(^|/)profiles/[A-Z]\d?[a-z]?-[^/]+\.md$")
ARCHIVE_PATH_PATTERN = re.compile(r"archive/[^\s\"'`)]+\.md")

# Look back this many tool calls when checking freshness.
FRESHNESS_WINDOW = 100

# Minimum profile cluster members read for high-impact decisions.
MIN_PROFILE_READS = 3


def is_architectural_artifact(path: str) -> bool:
    return any(p.search(path) for p in ARCHITECTURAL_PATTERNS)


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


def extract_read_paths(events: Iterable[dict], window: int) -> list[str]:
    """Scan recent events for Read tool_use; extract file_path arguments."""
    read_paths = []
    recent = list(events)[-window:] if window > 0 else list(events)
    for event in recent:
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
    events = read_transcript_events(transcript_path) if transcript_path else []
    recent_reads = extract_read_paths(events, FRESHNESS_WINDOW)

    blocks: list[str] = []

    # Check 1: skill freshness
    if not any(path_matches(rp, REQUIRED_SKILL) for rp in recent_reads):
        blocks.append(
            f"BLOCK: decision-design-sharpening SKILL.md not Read in last "
            f"{FRESHNESS_WINDOW} tool calls.\n"
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
        profile_reads = [rp for rp in recent_reads if PROFILE_GLOB_PATTERN.search(rp)]
        index_read = any(path_matches(rp, REQUIRED_PROFILE_INDEX) for rp in recent_reads)
        if len(profile_reads) < MIN_PROFILE_READS or not index_read:
            blocks.append(
                f"BLOCK: profile-anchored validation requires Read of "
                f"`{REQUIRED_PROFILE_INDEX}` + ≥{MIN_PROFILE_READS} cluster "
                f"members in last {FRESHNESS_WINDOW} tool calls. "
                f"Found: {len(profile_reads)} profile reads, "
                f"INDEX={'yes' if index_read else 'no'}.\n"
                f"  Per: DISCIPLINES.md Discipline 3 profile-anchored validation."
            )

    # Check 3: archive-citation cross-check (greenfield evaluation)
    write_content = tool_input.get("content") or tool_input.get("new_string") or ""
    if isinstance(write_content, str) and write_content:
        cited_archive_paths = set(ARCHIVE_PATH_PATTERN.findall(write_content))
        unread_citations = []
        for cited in cited_archive_paths:
            if not any(rp.endswith(cited) or rp.endswith("/" + cited) for rp in recent_reads):
                unread_citations.append(cited)
        if unread_citations:
            citations_list = "\n".join(f"    - {c}" for c in sorted(unread_citations))
            blocks.append(
                f"BLOCK: archive sources cited but not Read in current session "
                f"(greenfield-evaluation requires direct Read per "
                f"DISCIPLINES.md Discipline 10):\n{citations_list}"
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
