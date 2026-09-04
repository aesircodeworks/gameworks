"""Layout, counts, attribution, and runtime-vocabulary contract for Aesir Gameworks."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / ".hermes" / "source-snapshot"
WORKFLOW_NAMES = sorted(
    p.name for p in (SNAPSHOT / ".claude" / "skills").iterdir() if p.is_dir()
)
SLASH_RE = re.compile(
    r"(?<![A-Za-z0-9_-])/(?!aesir-)(" + "|".join(re.escape(n) for n in sorted(WORKFLOW_NAMES, key=len, reverse=True)) + r")(?![A-Za-z0-9_-])"
)
TASK_TOOL_RE = re.compile(
    r"(?:the Task tool|`Task`|Task subagent|Use Task |, Task,|, Task\b|allowed-tools:[^\n]*Task)",
    re.IGNORECASE,
)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.S)


def _skill_files() -> list[Path]:
    return sorted(ROOT.joinpath("skills").rglob("SKILL.md")) if (ROOT / "skills").is_dir() else []


def _frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise AssertionError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise AssertionError("frontmatter is not a mapping")
    return data


class ProfileContractTests(unittest.TestCase):
    def test_identity_files_exist(self) -> None:
        for name in ("distribution.yaml", "SOUL.md", "NOTICE.md", "config.yaml", "MIGRATION-MANIFEST.csv"):
            self.assertTrue((ROOT / name).is_file(), f"missing {name}")

    def test_forbidden_top_level_directories_absent(self) -> None:
        for name in (".claude", "CCGS Skill Testing Framework", "design", "docs", "production", "src"):
            self.assertFalse((ROOT / name).exists(), f"legacy root still present: {name}")

    def test_workflow_skill_count(self) -> None:
        found = list((ROOT / "skills" / "aesir-workflows").glob("aesir-*/SKILL.md"))
        self.assertEqual(len(found), 73, f"workflow skills: {len(found)}")

    def test_agent_skill_count(self) -> None:
        found = list((ROOT / "skills" / "aesir-agents").glob("aesir-agent-*/SKILL.md"))
        self.assertEqual(len(found), 49, f"agent skills: {len(found)}")

    def test_rule_skill_count(self) -> None:
        found = list((ROOT / "skills" / "aesir-rules").glob("aesir-rule-*/SKILL.md"))
        self.assertEqual(len(found), 11, f"rule skills: {len(found)}")

    def test_workflow_behavior_specs(self) -> None:
        specs = list((ROOT / "skills" / "aesir-workflows").glob("aesir-*/references/behavior-spec.md"))
        self.assertEqual(len(specs), 73, f"workflow specs: {len(specs)}")
        self.assertTrue(
            (ROOT / "skills/aesir-workflows/aesir-vertical-slice/references/behavior-spec.md").is_file()
        )

    def test_agent_behavior_specs(self) -> None:
        specs = list((ROOT / "skills" / "aesir-agents").glob("aesir-agent-*/references/behavior-spec.md"))
        self.assertEqual(len(specs), 49, f"agent specs: {len(specs)}")

    def test_skill_frontmatter_name_matches_directory(self) -> None:
        files = _skill_files()
        self.assertGreater(len(files), 0, "no SKILL.md files")
        for path in files:
            data = _frontmatter(path.read_text(encoding="utf-8"))
            self.assertEqual(data.get("name"), path.parent.name, path)

    def test_migrated_skills_have_no_claude_runtime_tokens(self) -> None:
        migrated = [
            p
            for p in _skill_files()
            if any(
                part in p.parts
                for part in (
                    "aesir-workflows",
                    "aesir-agents",
                    "aesir-rules",
                    "aesir-core",
                    "aesir-support",
                    "aesir-engines",
                    "aesir-quality",
                )
            )
            and "upstream" not in p.parts
        ]
        self.assertGreater(len(migrated), 0)
        for path in migrated:
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(".claude/", text, path)
            self.assertNotIn("AskUserQuestion", text, path)
            self.assertIsNone(TASK_TOOL_RE.search(text), f"standalone Task tool in {path}")
            hit = SLASH_RE.search(text)
            self.assertIsNone(hit, f"unprefixed /{hit.group(1) if hit else ''} in {path}")

    def test_license_copyright(self) -> None:
        self.assertIn("Copyright (c) 2026 Donchitos", (ROOT / "LICENSE").read_text(encoding="utf-8"))

    def test_notice_attribution(self) -> None:
        text = (ROOT / "NOTICE.md").read_text(encoding="utf-8")
        self.assertIn("Claude Code Game Studios", text)
        self.assertIn("Donchitos", text)
        self.assertIn("https://github.com/Donchitos/Claude-Code-Game-Studios", text)
        self.assertIn("MIT", text)


if __name__ == "__main__":
    unittest.main()
