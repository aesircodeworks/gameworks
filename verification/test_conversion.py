"""Mapping completeness tests for the 416-file CCGS → Aesir ledger."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

from scripts.build_migration import _convert_file
from scripts.ccgs_convert import convert_markdown

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (ROOT / "verification" / "expected_sources.txt").read_text(encoding="utf-8").splitlines()
MANIFEST = ROOT / "MIGRATION-MANIFEST.csv"
SNAPSHOT = ROOT / ".hermes" / "source-snapshot"
LEDGER = ROOT / ".hermes" / "source-sha256.json"
PLAN = ROOT / ".hermes" / "plans" / "2026-09-04_144926-convert-ccgs-to-aesir-gameworks-profile.md"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
DELETE_SOURCES = {
    ".DS_Store",
    ".claude/.DS_Store",
    "CCGS Skill Testing Framework/.DS_Store",
    "docs/.DS_Store",
    "production/session-state/.gitkeep",
    "src/.gitkeep",
}


class ConversionTransformTests(unittest.TestCase):
    def test_reference_fence_rewrites_claude_runtime_tokens(self) -> None:
        source = "```text\nAskUserQuestion\n.claude/docs/example.md\n```\n"

        converted = convert_markdown(source, kind="reference", source_name="example")

        self.assertIn("clarify", converted)
        self.assertNotIn("AskUserQuestion", converted)
        self.assertNotIn(".claude/", converted)

    def test_workflow_catalog_uses_reference_conversion(self) -> None:
        source = "artifact:\n  glob: .claude/docs/technical-preferences.md\n"

        converted = _convert_file(
            source,
            ".claude/docs/workflow-catalog.yaml",
            "skills/studio/gameworks/references/workflow-catalog.yaml",
            [],
        )

        self.assertNotIn(".claude/", converted)
        self.assertIn("gameworks references/technical-preferences.md", converted)


def _rows() -> list[dict]:
    with MANIFEST.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class ConversionLedgerTests(unittest.TestCase):
    def test_manifest_exists_with_required_columns(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "MIGRATION-MANIFEST.csv does not exist")
        rows = _rows()
        self.assertGreater(len(rows), 0)
        for required in ("source", "destinations", "action", "source_sha256"):
            self.assertIn(required, rows[0])

    def test_expected_source_inventory(self) -> None:
        self.assertEqual(len(EXPECTED), 416)
        self.assertEqual(EXPECTED, sorted(EXPECTED, key=lambda s: s.encode()))
        if LEDGER.is_file():
            keys = json.loads(LEDGER.read_text(encoding="utf-8"))
            self.assertEqual(EXPECTED, sorted(keys, key=lambda s: s.encode()))
        if SNAPSHOT.is_dir():
            snap = sorted(
                p.relative_to(SNAPSHOT).as_posix()
                for p in SNAPSHOT.rglob("*")
                if p.is_file()
            )
            self.assertEqual(EXPECTED, sorted(snap, key=lambda s: s.encode()))

    def test_manifest_accounts_for_every_source(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "MIGRATION-MANIFEST.csv does not exist")
        rows = _rows()
        self.assertEqual(len(rows), 416)
        sources = [row["source"] for row in rows]
        self.assertEqual(len(set(sources)), 416)
        self.assertEqual(sorted(sources, key=lambda s: s.encode()), EXPECTED)

    def test_actions_and_destinations(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "MIGRATION-MANIFEST.csv does not exist")
        rows = _rows()
        seen_dest: dict[str, str] = {}
        deletes = []
        for row in rows:
            dests = json.loads(row["destinations"])
            self.assertIsInstance(dests, list)
            action = row["action"]
            self.assertIn(action, {"convert", "rewrite", "delete", "split", "preserve"})
            self.assertTrue(SHA_RE.match(row["source_sha256"]), row["source"])
            if action == "delete":
                self.assertEqual(dests, [])
                deletes.append(row["source"])
            elif action == "split":
                self.assertEqual(len(dests), 2, row["source"])
            else:
                self.assertEqual(len(dests), 1, row["source"])
            for dest in dests:
                self.assertNotIn(dest, seen_dest, f"duplicate dest {dest}")
                seen_dest[dest] = row["source"]
                self.assertTrue((ROOT / dest).exists(), f"missing destination {dest} from {row['source']}")
        self.assertEqual(sorted(deletes), sorted(DELETE_SOURCES))
        self.assertEqual(len(deletes), 6)

    def test_source_hashes_match_frozen_ledger(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "MIGRATION-MANIFEST.csv does not exist")
        rows = _rows()
        ledger = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.is_file() else None
        for row in rows:
            digest = row["source_sha256"]
            self.assertTrue(SHA_RE.match(digest), row["source"])
            if ledger is not None:
                self.assertEqual(digest, ledger[row["source"]], row["source"])
            snap = SNAPSHOT / row["source"]
            if snap.is_file() and row["action"] != "delete":
                self.assertEqual(digest, hashlib.sha256(snap.read_bytes()).hexdigest(), row["source"])

    def test_action_counts_match_plan(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "MIGRATION-MANIFEST.csv does not exist")
        rows = _rows()
        counts = {key: 0 for key in ("convert", "rewrite", "delete", "split", "preserve")}
        for row in rows:
            counts[row["action"]] += 1
        self.assertEqual(counts["convert"], 386)
        self.assertEqual(counts["rewrite"], 21)
        self.assertEqual(counts["delete"], 6)
        self.assertEqual(counts["split"], 2)
        self.assertEqual(counts["preserve"], 1)


if __name__ == "__main__":
    unittest.main()
