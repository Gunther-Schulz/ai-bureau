"""
Tests for fresh_plan_grounding_gate.py PreToolUse hook (D66; Roadmap #20).

Invokes the hook as a subprocess with synthetic stdin payload + a
tempfile transcript JSONL that mocks Read tool_use events. Verifies
exit-code semantics and stderr content per design.

Run from repo root:
    python -m unittest fresh-plan.plugin.tests.test_grounding_gate -v

Or directly:
    python fresh-plan/plugin/tests/test_grounding_gate.py
"""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
HOOK_PATH = REPO_ROOT / "fresh-plan" / "plugin" / "hooks" / "fresh_plan_grounding_gate.py"


def build_transcript(jsonl_path: Path, read_paths: list[str]) -> None:
    """Write a mock transcript JSONL containing synthetic Read tool_use
    events. Mirrors the assistant-message + tool_use block shape that
    Claude Code records in transcript files."""
    with open(jsonl_path, "w") as f:
        for rp in read_paths:
            event = {
                "type": "assistant",
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": rp},
                        }
                    ],
                },
            }
            f.write(json.dumps(event) + "\n")


def invoke_hook(payload: dict) -> tuple[int, str]:
    """Run hook as subprocess with payload JSON on stdin. Return
    (returncode, stderr_text)."""
    proc = subprocess.run(
        ["python3", str(HOOK_PATH)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=15,
    )
    return proc.returncode, proc.stderr


class TestGroundingGate(unittest.TestCase):
    def test_d_entry_write_with_required_reads(self) -> None:
        """D-entry write with BOTH required Reads present → exit 0."""
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "session.jsonl"
            build_transcript(transcript, [
                "/abs/path/fresh-plan/CLIPPY-COMPANION.md",
                "/abs/path/fresh-plan/probing.md",
            ])
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "fresh-plan/decisions/D99-test.md",
                    "old_string": "x",
                    "new_string": "y",
                },
                "transcript_path": str(transcript),
            }
            code, stderr = invoke_hook(payload)
            self.assertEqual(code, 0, f"Expected exit 0; got {code}. stderr={stderr}")

    def test_d_entry_write_without_required_reads(self) -> None:
        """D-entry write with only ONE required Read (probing.md missing)
        → exit 2 + stderr names probing.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "session.jsonl"
            build_transcript(transcript, [
                "/abs/path/fresh-plan/CLIPPY-COMPANION.md",
            ])
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "fresh-plan/decisions/D99-test.md",
                    "old_string": "x",
                    "new_string": "y",
                },
                "transcript_path": str(transcript),
            }
            code, stderr = invoke_hook(payload)
            self.assertEqual(code, 2, f"Expected exit 2; got {code}. stderr={stderr}")
            self.assertIn("probing.md", stderr)
            # CLIPPY-COMPANION.md was Read; should NOT be in missing list.
            # Verify by checking it's not listed under the "Missing Reads:" block.
            missing_block = stderr.split("Missing Reads:", 1)[1] if "Missing Reads:" in stderr else ""
            self.assertNotIn("CLIPPY-COMPANION.md", missing_block.split("Per:")[0])

    def test_impl_src_write_without_required_reads(self) -> None:
        """impl/src/*.py write with empty transcript (no required Reads)
        → exit 2 + stderr lists BOTH missing Reads."""
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript = Path(tmpdir) / "session.jsonl"
            build_transcript(transcript, [])
            payload = {
                "tool_name": "Edit",
                "tool_input": {
                    "file_path": "fresh-plan/impl/src/runtime/shape.py",
                    "old_string": "x",
                    "new_string": "y",
                },
                "transcript_path": str(transcript),
            }
            code, stderr = invoke_hook(payload)
            self.assertEqual(code, 2, f"Expected exit 2; got {code}. stderr={stderr}")
            self.assertIn("CLIPPY-COMPANION.md", stderr)
            self.assertIn("probing.md", stderr)


if __name__ == "__main__":
    unittest.main()
