#!/usr/bin/env python3
"""Deterministic CCGS → Aesir migration builder."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from ccgs_convert import ATTRIBUTION, convert_catalog, convert_markdown, kind_for, map_source, source_name_for  # noqa: E402

PLAN = ROOT / ".hermes" / "plans" / "2026-09-04_144926-convert-ccgs-to-aesir-gameworks-profile.md"
EXPECTED = ROOT / "verification" / "expected_sources.txt"
LEDGER = ROOT / ".hermes" / "source-sha256.json"


def _load_plan_rows() -> list[tuple[str, str, str]]:
    text = PLAN.read_text(encoding="utf-8")
    return re.findall(r"^\| `([^`]+)` \| `([^`]+)` \| (convert|rewrite|delete|split|preserve) \|$", text, re.M)


def _dests_from_plan(cell: str, action: str) -> list[str]:
    if action == "delete":
        return []
    if " + " in cell:
        return [part.strip() for part in cell.split(" + ")]
    return [cell]


def assert_rules_match_plan() -> None:
    rows = _load_plan_rows()
    if len(rows) != 416:
        raise SystemExit(f"Appendix B rows: {len(rows)}")
    for source, dest_cell, action in rows:
        got_action, got_dests = map_source(source)
        exp_dests = _dests_from_plan(dest_cell, action)
        if got_action != action or got_dests != exp_dests:
            raise SystemExit(f"rule mismatch for {source}: {got_action} {got_dests} != {action} {exp_dests}")


def _names(snapshot: Path, kind: str) -> list[str]:
    if kind == "workflow":
        return sorted(p.name for p in (snapshot / ".claude" / "skills").iterdir() if p.is_dir())
    return sorted(p.stem for p in (snapshot / ".claude" / "agents").glob("*.md"))


def _atomic_write(path: Path, data: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    if isinstance(data, bytes):
        tmp.write_bytes(data)
    else:
        tmp.write_text(data, encoding="utf-8")
    tmp.replace(path)


def _safe_dest(staging: Path, rel: str) -> Path:
    dest = (staging / rel).resolve()
    if dest == staging.resolve() or staging.resolve() not in dest.parents:
        raise SystemExit(f"path traversal: {rel}")
    return dest


def _convert_file(src_text: str, src: str, dest: str, workflows: list[str]) -> str:
    kind = kind_for(src, dest)
    name = source_name_for(src, dest)
    if dest.endswith("claude-settings.json") or dest.endswith("UPGRADING-CCGS.md"):
        body = src_text
        if not body.endswith("\n"):
            body += "\n"
        if dest.endswith(".md") and ATTRIBUTION.strip() not in body:
            body = ATTRIBUTION + "\n" + body
        return body
    if dest.endswith("catalog.yaml"):
        return convert_catalog(src_text, workflows, [])
    if dest.endswith(".yaml") or dest.endswith(".yml"):
        converted = convert_markdown(src_text, kind="reference", source_name=name, workflow_names=workflows)
        return converted
    if dest.endswith(".sh"):
        return src_text  # rewritten later by dedicated hook/status ports
    if dest in {".gitignore", "README.md", "CONTRIBUTING.md", "SECURITY.md", "SOUL.md", "config.yaml"}:
        converted = convert_markdown(src_text, kind="reference", source_name=name, workflow_names=workflows)
        return converted
    return convert_markdown(src_text, kind=kind, source_name=name, workflow_names=workflows)


def write_manifest(rows: list[dict], dest: Path) -> None:
    tmp = dest.with_suffix(".csv.tmp")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "destinations", "action", "source_sha256"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    tmp.replace(dest)


def build(source: Path, staging: Path, manifest_only: bool) -> None:
    assert_rules_match_plan()
    expected = EXPECTED.read_text(encoding="utf-8").splitlines()
    snapshot_files = sorted(
        p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file()
    )
    if snapshot_files != expected:
        extra = sorted(set(snapshot_files) - set(expected))
        missing = sorted(set(expected) - set(snapshot_files))
        raise SystemExit(f"snapshot != expected_sources extra={extra[:8]} missing={missing[:8]}")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    workflows = _names(source, "workflow")
    used_dests: set[str] = set()
    rows: list[dict] = []
    counts = {"convert": 0, "rewrite": 0, "delete": 0, "split": 0, "preserve": 0, "unmapped": 0}
    if not manifest_only:
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True)
    for rel in expected:
        action, dests = map_source(rel)
        src_path = source / rel
        digest = hashlib.sha256(src_path.read_bytes()).hexdigest()
        if digest != ledger[rel]:
            if action == "delete":
                digest = ledger[rel]
            else:
                raise SystemExit(f"hash mismatch before write: {rel}")
        for dest in dests:
            if dest in used_dests:
                raise SystemExit(f"duplicate destination {dest}")
            used_dests.add(dest)
        rows.append(
            {
                "source": rel,
                "destinations": json.dumps(dests, separators=(",", ":")),
                "action": action,
                "source_sha256": digest,
            }
        )
        counts[action] += 1
        if manifest_only or action == "delete":
            continue
        raw = src_path.read_bytes()
        for dest in dests:
            if dest == "config.yaml":
                continue  # generated later via disposable Hermes profile
            if dest == "SOUL.md":
                continue  # authored exactly in Task 4
            target = _safe_dest(staging, dest)
            target.parent.mkdir(parents=True, exist_ok=True)
            if action == "preserve" or dest.endswith("claude-settings.json"):
                target.write_bytes(raw)
                continue
            text = raw.decode("utf-8")
            converted = _convert_file(text, rel, dest, workflows)
            if dest.endswith("PLUGINS.md") and "unity" in dest:
                converted = converted.replace("../modules/input.md", "modules/input.md")
                converted = converted.replace("../modules/ui.md", "modules/ui.md")
            target.write_text(converted, encoding="utf-8")
    write_manifest(rows, ROOT / "MIGRATION-MANIFEST.csv")
    if not manifest_only:
        # Always keep LICENSE in staging from snapshot.
        shutil.copy2(source / "LICENSE", staging / "LICENSE")
    print(
        f"{len(expected)} source files accounted for; {counts['unmapped']} unmapped; {counts['delete']} deletions"
    )
    print(
        f"actions convert={counts['convert']} rewrite={counts['rewrite']} "
        f"delete={counts['delete']} split={counts['split']} preserve={counts['preserve']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / ".hermes" / "source-snapshot")
    parser.add_argument("--staging", type=Path, default=ROOT / ".migration-staging")
    parser.add_argument("--manifest-only", action="store_true")
    args = parser.parse_args()
    build(args.source.resolve(), args.staging.resolve(), args.manifest_only)


if __name__ == "__main__":
    main()
