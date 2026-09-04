"""Allowlist merge and idempotence tests for apply_profile_config."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.apply_profile_config import merge_config


class ConfigMergeTests(unittest.TestCase):
    def test_allowlisted_scalar_changes(self) -> None:
        current = {"approvals": {"mode": "manual"}, "model": {"default": "keep"}}
        incoming = {"approvals": {"mode": "smart"}, "model": {"default": "ignore"}}
        merged = merge_config(current, incoming)
        self.assertEqual(merged["approvals"]["mode"], "smart")
        self.assertEqual(merged["model"]["default"], "keep")

    def test_list_dedup(self) -> None:
        current = {"command_allowlist": ["git status*"]}
        incoming = {"command_allowlist": ["git status*", "git diff*"]}
        merged = merge_config(current, incoming)
        self.assertEqual(merged["command_allowlist"], ["git status*", "git diff*"])
        again = merge_config(merged, incoming)
        self.assertEqual(again, merged)

    def test_hooks_update_by_identity_and_preserve_unrelated(self) -> None:
        current = {
            "hooks": {
                "pre_llm_call": [
                    {"command": "other.sh", "timeout": 5},
                    {"command": "session-start.sh", "timeout": 10},
                ]
            }
        }
        incoming = {
            "hooks": {
                "pre_llm_call": [
                    {"command": "session-start.sh", "timeout": 10, "fail_closed": False},
                    {"command": "detect-project-gaps.sh", "timeout": 10},
                ]
            }
        }
        merged = merge_config(current, incoming)
        commands = [e["command"] for e in merged["hooks"]["pre_llm_call"]]
        self.assertEqual(commands[0], "other.sh")
        self.assertIn("detect-project-gaps.sh", commands)
        self.assertEqual(merge_config(merged, incoming), merged)

    def test_roundtrip_file(self) -> None:
        from scripts.apply_profile_config import apply

        tmp = Path(tempfile.mkdtemp())
        home = tmp
        (home / "config.yaml").write_text("model:\n  default: keep\napprovals:\n  mode: manual\n")
        src = tmp / "dist.yaml"
        src.write_text("approvals:\n  mode: smart\nmemory:\n  write_approval: true\n")
        apply(home, src)
        apply(home, src)
        text = (home / "config.yaml").read_text()
        self.assertIn("mode: smart", text)
        self.assertIn("default: keep", text)


if __name__ == "__main__":
    unittest.main()
