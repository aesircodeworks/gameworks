"""Synthetic preservation capture/verify tests. No live profile data."""

from __future__ import annotations

import json
import shutil
import stat
import tempfile
import unittest
from pathlib import Path

from scripts.check_profile_preservation import capture, restore_config, verify


class PreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.home = self.tmp / "profile"
        self.home.mkdir()
        (self.home / "skills/autonomous-ai-agents/hermes-agent").mkdir(parents=True)
        (self.home / "skills/autonomous-ai-agents/hermes-agent/SKILL.md").write_text("keep\n")
        (self.home / ".env").write_text("SECRET=1\n")
        (self.home / "config.yaml").write_text("model:\n  default: x\napprovals:\n  mode: smart\n")
        (self.home / "memories").mkdir()
        (self.home / "memories/MEMORY.md").write_text("user fact\n")
        self.baseline = self.tmp / "private" / "baseline.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_capture_is_owner_only(self) -> None:
        capture(self.home, self.baseline)
        self.assertEqual(self.baseline.stat().st_mode & 0o777, stat.S_IRUSR | stat.S_IWUSR)
        data = json.loads(self.baseline.read_text())
        self.assertIn("skills/autonomous-ai-agents/hermes-agent/SKILL.md", data["files"])
        self.assertIn(".env", data["files"])

    def test_verify_passes_unchanged(self) -> None:
        capture(self.home, self.baseline)
        self.assertEqual(verify(self.home, self.baseline), 0)

    def test_verify_fails_on_protected_change(self) -> None:
        capture(self.home, self.baseline)
        (self.home / "skills/autonomous-ai-agents/hermes-agent/SKILL.md").write_text("mutated\n")
        self.assertEqual(verify(self.home, self.baseline), 1)

    def test_owned_paths_may_change(self) -> None:
        capture(self.home, self.baseline)
        dest = self.home / "skills/studio/gameworks"
        dest.mkdir(parents=True)
        (dest / "SKILL.md").write_text("new\n")
        self.assertEqual(verify(self.home, self.baseline), 0)

    def test_restore_config(self) -> None:
        capture(self.home, self.baseline)
        (self.home / "config.yaml").write_text("model:\n  default: overwritten\n")
        restore_config(self.home, self.baseline)
        self.assertIn("default: x", (self.home / "config.yaml").read_text())


if __name__ == "__main__":
    unittest.main()
