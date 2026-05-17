#!/usr/bin/env python3
"""
PreToolUse hook: fresh-plan grounding gate.

Blocks Edit/Write/MultiEdit on substantive fresh-plan artifacts unless
required preparatory Reads happened in the current session. Structural
enforcement of grounded-reads discipline per README session-start step 5
HARD RULE + CLIPPY-COMPANION + probing.md investigation-before-claim.

D66 — Roadmap deliverable #20.

Wired via fresh-plan/plugin/.claude-plugin/plugin.json hooks section.
Receives JSON via stdin per Claude Code hook protocol; reads
transcript_path from input to scan tool_use history; returns exit 0
(allow) or 2 (block) with stderr message.

Adapted from pbs-bureau plugin/hooks/architectural_commit_gate.py;
narrowed to a single check (required-Reads freshness via whole-session
transcript scan). Profile-anchored validation, archive-citation
cross-check, and provenance-breadcrumb regex from the parent are
deferred per D66 §D (Phase C+ if natural-failure surfaces).

Freshness-window strategy: whole-session scan. Claude Code's
transcript_path is per-session per the hooks API (each transcript JSONL
has a single sessionId across all events). We scan ALL events in the
transcript + sibling sub-agent transcripts. No call-count window. This
avoids the cascade-load failure mode where prep Reads done at session
start get pushed out of a fixed-size window before a long cascade
completes.

Honest limitations:
- Detects FILE-READ-HAPPENED, not GROUNDED-EVALUATION-HAPPENED
- AI could Read perfunctorily; quality remains convention-grade
- Hook fires at write-boundary; doesn't gate sketch-stage semantically
- Activation requires /reload-plugins on fresh-plan-clippy branch
"""

import json
import re
import sys
from pathlib import Path
from typing import Iterable

# Substantive fresh-plan artifact path patterns (relative to repo root).
# Hook fires on these paths.
SUBSTANTIVE_PATTERNS = [
    re.compile(r"fresh-plan/decisions/D\d+[^/]*\.md$"),
    re.compile(r"fresh-plan/impl/src/.*\.py$"),
    re.compile(r"fresh-plan/schemas/.*\.json$"),
]

# Required Reads per substantive write. Discipline source-of-truth for
# fresh-plan grounded-reads at session-start (per README step 5 HARD RULE
# + CLIPPY-COMPANION D-entry shape + probing.md investigation-before-claim).
REQUIRED_READS = [
    "fresh-plan/CLIPPY-COMPANION.md",
    "fresh-plan/probing.md",
]


def is_substantive_artifact(path: str) -> bool:
    return any(p.search(path) for p in SUBSTANTIVE_PATTERNS)


def extract_write_content(tool_input: dict) -> str:
    """Extract content being written/edited. Supports Edit (new_string),
    Write (content), and MultiEdit (edits[].new_string). Kept as
    defensive helper for future content-scan checks (D66 §D D-1)."""
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


def gather_session_transcript_paths(transcript_path: str) -> list[str]:
    """Return main-session transcript path + all sibling sub-agent
    transcript paths.

    Claude Code records sub-agent transcripts at
    `<project>/<session_id>/subagents/agent-*.jsonl` — siblings of the
    main JSONL named `<session_id>.jsonl`. Sub-agent prep-Reads live in
    those sibling files; they count for freshness because sub-agents
    dispatched in the current session ARE the current session for
    discipline-execution purposes.
    """
    if not transcript_path:
        return []
    paths = [transcript_path]
    p = Path(transcript_path)
    subagent_dir = p.with_suffix("") / "subagents"
    if subagent_dir.is_dir():
        paths.extend(sorted(str(f) for f in subagent_dir.glob("*.jsonl")))
    return paths


def extract_read_paths(events: Iterable[dict]) -> list[str]:
    """Scan ALL events for Read tool_use; extract file_path arguments.

    Whole-session scan per architectural_commit_gate.py pattern.
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
    if not target or not is_substantive_artifact(target):
        return 0

    # This is a substantive-artifact write. Check preparatory Reads.
    # Whole-session scan: aggregate main-session transcript + all
    # sibling sub-agent transcripts.
    events = []
    for tp in gather_session_transcript_paths(transcript_path):
        events.extend(read_transcript_events(tp))
    session_reads = extract_read_paths(events)

    missing = [
        req for req in REQUIRED_READS
        if not any(path_matches(rp, req) for rp in session_reads)
    ]

    if missing:
        missing_list = "\n".join(f"    - {m}" for m in missing)
        msg = (
            "BLOCK: fresh-plan substantive write requires preparatory Reads "
            "not found in current session.\n"
            f"  Missing Reads:\n{missing_list}\n"
            "  Per: fresh-plan/README.md session-start step 5 (HARD RULE — "
            "Cite-or-Read-or-Flag) + CLIPPY-COMPANION.md (D-entry shape) + "
            "probing.md (investigation-before-claim discipline).\n"
            "Resolve by Reading the named files via Read tool, then retry "
            "the Edit/Write."
        )
        print(msg, file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
