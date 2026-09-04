"""Synthetic Hermes-payload tests for Aesir shell hooks."""

from __future__ import annotations

import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "agent-hooks" / "aesir-gameworks"


def run_hook(name: str, payload: dict, cwd: Path | None = None) -> subprocess.CompletedProcess:
    script = HOOKS / name
    return subprocess.run(
        ["bash", str(script)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=str(cwd or ROOT),
        timeout=15,
    )


class HookTests(unittest.TestCase):
    def test_scripts_are_executable_syntax(self) -> None:
        scripts = [p for p in HOOKS.glob("*.sh")]
        self.assertGreaterEqual(len(scripts), 12)
        for script in scripts:
            proc = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, script.name + proc.stderr)

    def test_observers_return_json(self) -> None:
        payload = {"hook_event_name": "pre_llm_call", "session_id": "s", "cwd": str(ROOT), "tool_input": {}}
        for name in (
            "session-start.sh",
            "detect-project-gaps.sh",
            "restore-session-context.sh",
            "checkpoint-session-state.sh",
            "session-end.sh",
            "notify-session.sh",
            "log-subagent-start.sh",
            "log-subagent-stop.sh",
        ):
            result = run_hook(name, payload)
            self.assertEqual(result.returncode, 0, name + result.stderr)
            data = json.loads(result.stdout.strip() or "{}")
            self.assertTrue(data == {} or "context" in data, name)

    def test_validate_commit_blocks_bad_json(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init"], cwd=tmp, check=True, capture_output=True)
        (tmp / "assets/data").mkdir(parents=True)
        bad = tmp / "assets/data/stats.json"
        bad.write_text("{not json")
        subprocess.run(["git", "add", "assets/data/stats.json"], cwd=tmp, check=True, capture_output=True)
        result = run_hook(
            "validate-commit.sh",
            {"tool_name": "terminal", "tool_input": {"command": "git commit -m x"}, "cwd": str(tmp)},
            cwd=tmp,
        )
        self.assertEqual(result.returncode, 2)
        data = json.loads(result.stdout)
        self.assertEqual(data.get("action"), "block")

    def test_validate_commit_blocks_todo_format(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init"], cwd=tmp, check=True, capture_output=True)
        src = tmp / "src/gameplay/foo.gd"
        src.parent.mkdir(parents=True)
        src.write_text("TODO fix this later\n")
        subprocess.run(["git", "add", "src/gameplay/foo.gd"], cwd=tmp, check=True, capture_output=True)
        result = run_hook(
            "validate-commit.sh",
            {"tool_name": "terminal", "tool_input": {"command": "git commit -m x"}, "cwd": str(tmp)},
            cwd=tmp,
        )
        self.assertEqual(result.returncode, 2)

    def test_validate_push_blocks_protected_force(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init", "-b", "main"], cwd=tmp, check=True, capture_output=True)
        (tmp / "README").write_text("x")
        subprocess.run(["git", "add", "README"], cwd=tmp, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=tmp, check=True, capture_output=True)
        result = run_hook(
            "validate-push.sh",
            {"tool_name": "terminal", "tool_input": {"command": "git push --force origin main"}, "cwd": str(tmp)},
            cwd=tmp,
        )
        self.assertEqual(result.returncode, 2)

    def test_assets_ignore_non_asset_paths(self) -> None:
        result = run_hook(
            "validate-project-assets.sh",
            {"tool_name": "write_file", "tool_input": {"path": "skills/aesir-core/foo.md"}},
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout.strip() or "{}"), {})

    def test_no_env_reads(self) -> None:
        for script in HOOKS.glob("*.sh"):
            text = script.read_text(encoding="utf-8")
            self.assertNotIn(".env", text)
            self.assertNotIn("auth.json", text)
            self.assertNotIn("state.db", text)

    def test_not_a_git_repo(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        result = run_hook(
            "validate-commit.sh",
            {"tool_name": "terminal", "tool_input": {"command": "git commit -m x"}, "cwd": str(tmp)},
            cwd=tmp,
        )
        self.assertEqual(result.returncode, 0)
