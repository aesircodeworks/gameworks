#!/usr/bin/env python3
"""Deterministic Aesir distribution validator. No network access."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_ROOTS = (".claude", "CCGS Skill Testing Framework", "design", "docs", "production", "src")
CLAUDE_TOKENS = ("AskUserQuestion", ".claude/")
TASK_TOOL_RE = re.compile(
    r"(?:the Task tool|`Task`|Task subagent|Use Task |, Task,)",
    re.I,
)
MARKDOWN_CODE_RE = re.compile(r"```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]*`")


def _workflows() -> list[Path]:
    return sorted((ROOT / "skills/workflows").glob("*/SKILL.md"))


def _agents() -> list[Path]:
    return sorted((ROOT / "skills/agents").glob("*/SKILL.md"))


def _rules() -> list[Path]:
    return sorted((ROOT / "skills/rules").glob("*/SKILL.md"))


def _fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        raise ValueError(f"{path} missing frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"{path} frontmatter not a mapping")
    return data


def scope_support(failures: list[str]) -> None:
    required = [
        ROOT / "skills/studio/gameworks/SKILL.md",
        ROOT / "skills/studio/memory-policy/SKILL.md",
        ROOT / "skills/support/project-bootstrap/SKILL.md",
        ROOT / "skills/support/project-templates/SKILL.md",
        ROOT / "skills/support/studio-status/SKILL.md",
        ROOT / "skills/engines/engine-reference/SKILL.md",
        ROOT / "skills/quality/framework-qa/SKILL.md",
    ]
    for path in required:
        if not path.is_file():
            _fail(f"missing support skill {path.relative_to(ROOT)}", failures)
        else:
            data = _frontmatter(path)
            if data.get("name") != path.parent.name:
                _fail(f"name mismatch {path}", failures)
    plugins = ROOT / "docs/engine-reference/unity/PLUGINS.md"
    converted = ROOT / "skills/engines/engine-reference/references/unity/PLUGINS.md"
    if converted.is_file():
        text = converted.read_text(encoding="utf-8")
        if "../modules/input.md" in text or "../modules/ui.md" in text:
            _fail("unity plugin links still broken", failures)
    _ = plugins


def scope_workflows(failures: list[str], names: set[str] | None) -> None:
    found = _workflows()
    if names:
        found = [p for p in found if p.parent.name in names]
        missing = names - {p.parent.name for p in found}
        for name in sorted(missing):
            _fail(f"missing workflow {name}", failures)
    else:
        if len(found) != 73:
            _fail(f"workflow skills: {len(found)}/73", failures)
    for path in found:
        text = path.read_text(encoding="utf-8")
        if ".claude/" in text or "AskUserQuestion" in text or TASK_TOOL_RE.search(text):
            _fail(f"claude runtime token in {path.relative_to(ROOT)}", failures)


def scope_agents(failures: list[str]) -> None:
    found = _agents()
    if len(found) != 49:
        _fail(f"agents: {len(found)}/49", failures)
    specs = list((ROOT / "skills/agents").glob("*/references/behavior-spec.md"))
    if len(specs) != 49:
        _fail(f"behavior specs: {len(specs)}/49", failures)
    unresolved = 0
    for path in found:
        text = path.read_text(encoding="utf-8")
        if "AskUserQuestion" in text or TASK_TOOL_RE.search(text):
            unresolved += 1
            _fail(f"unresolved Claude tools: {path.relative_to(ROOT)}", failures)
    print(f"agents: {len(found)}/49; behavior specs: {len(specs)}/49; unresolved Claude tools: {unresolved}")


def scope_rules(failures: list[str]) -> None:
    found = _rules()
    if len(found) != 11:
        _fail(f"rules: {len(found)}/11", failures)
    missing_patterns = 0
    unresolved = 0
    for path in found:
        text = path.read_text(encoding="utf-8")
        if "paths:" not in text and "target file patterns" not in text.lower() and "`src/" not in text and "src/" not in text:
            missing_patterns += 1
        if ".claude/" in text or "AskUserQuestion" in text:
            unresolved += 1
    print(f"rules: {len(found)}/11; missing target patterns: {missing_patterns}; unresolved references: {unresolved}")
    if missing_patterns:
        _fail("missing target patterns", failures)
    if unresolved:
        _fail("unresolved references in rules", failures)


def scope_qa(failures: list[str]) -> None:
    wf = list((ROOT / "skills/workflows").glob("*/references/behavior-spec.md"))
    ag = list((ROOT / "skills/agents").glob("*/references/behavior-spec.md"))
    catalog = ROOT / "skills/quality/framework-qa/references/catalog.yaml"
    gaps = 0
    if catalog.is_file():
        data = yaml.safe_load(catalog.read_text(encoding="utf-8")) or {}
        skill_names = {s.get("name") for s in data.get("skills") or []}
        agent_names = {a.get("name") for a in data.get("agents") or []}
        if len(skill_names) != 73:
            gaps += abs(73 - len(skill_names))
        if len(agent_names) != 49:
            gaps += abs(49 - len(agent_names))
    else:
        gaps += 1
        _fail("missing catalog.yaml", failures)
    print(f"workflow specs: {len(wf)}/73; agent specs: {len(ag)}/49; catalog gaps: {gaps}")
    if len(wf) != 73 or len(ag) != 49 or gaps:
        _fail("qa coverage incomplete", failures)


def _markdown_files() -> list[Path]:
    files: list[Path] = []
    for base in (ROOT / "skills", ROOT / "agent-hooks"):
        if base.exists():
            files.extend(p for p in base.rglob("*") if p.suffix in {".md", ".yaml", ".yml"} and p.is_file())
    for name in ("README.md", "NOTICE.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md"):
        path = ROOT / name
        if path.is_file():
            files.append(path)
    return files


def scope_docs(failures: list[str]) -> None:
    broken = 0
    forbidden = 0
    leftover_prefix = 0
    link_re = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    prefix_re = re.compile(r"(?<![A-Za-z0-9_-])/aesir-[A-Za-z0-9_-]+")
    for path in _markdown_files():
        if "upstream" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if any(tok in text for tok in CLAUDE_TOKENS):
            forbidden += 1
        if prefix_re.search(text):
            leftover_prefix += 1
        prose = MARKDOWN_CODE_RE.sub("", text)
        for href in link_re.findall(prose):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            href = href.split("#", 1)[0]
            if not href:
                continue
            target = (path.parent / href).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if not target.exists():
                broken += 1
    print(f"broken links: {broken}; forbidden live Claude references: {forbidden}; leftover /aesir- slashes: {leftover_prefix}")
    if broken or forbidden or leftover_prefix:
        _fail("docs scan failed", failures)


def scope_all(failures: list[str]) -> None:
    manifest = ROOT / "MIGRATION-MANIFEST.csv"
    sources = 0
    if manifest.is_file():
        with manifest.open(newline="", encoding="utf-8") as handle:
            sources = sum(1 for _ in csv.DictReader(handle))
    wf = _workflows()
    wfs = list((ROOT / "skills/workflows").glob("*/references/behavior-spec.md"))
    ag = _agents()
    ags = list((ROOT / "skills/agents").glob("*/references/behavior-spec.md"))
    rules = _rules()
    hooks = list((ROOT / "agent-hooks/aesir-gameworks").glob("*.sh"))
    hooks = [p for p in hooks if p.name != "lib.sh"]
    forbidden = sum(1 for name in FORBIDDEN_ROOTS if (ROOT / name).exists())
    notice = (ROOT / "NOTICE.md").read_text(encoding="utf-8") if (ROOT / "NOTICE.md").is_file() else ""
    attribution = "PASS" if "Claude Code Game Studios" in notice and "Donchitos" in notice else "FAIL"
    print(f"sources: {sources}/416")
    print(f"workflow skills: {len(wf)}/73")
    print(f"workflow specs: {len(wfs)}/73")
    print(f"agent skills: {len(ag)}/49")
    print(f"agent specs: {len(ags)}/49")
    print(f"rule skills: {len(rules)}/11")
    print(f"shell hooks: {len(hooks)}/12")
    scope_docs(failures)
    print(f"unresolved Claude runtime tokens: {sum(1 for p in wf+ag+rules if 'AskUserQuestion' in p.read_text(encoding='utf-8'))}")
    print(f"forbidden top-level directories: {forbidden}")
    print(f"attribution: {attribution}")
    if sources != 416:
        _fail("source accounting", failures)
    if len(wf) != 73 or len(wfs) != 73 or len(ag) != 49 or len(ags) != 49 or len(rules) != 11 or len(hooks) != 12:
        _fail("count mismatch", failures)
    if forbidden:
        _fail("forbidden roots present", failures)
    if attribution != "PASS":
        _fail("attribution", failures)
    print("VERDICT: PASS" if not failures else "VERDICT: FAIL")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="all", choices=["support", "workflows", "agents", "rules", "qa", "docs", "all"])
    parser.add_argument("--names", default="")
    args = parser.parse_args()
    failures: list[str] = []
    names = {n.strip() for n in args.names.split(",") if n.strip()} or None
    if args.scope == "support":
        scope_support(failures)
    elif args.scope == "workflows":
        scope_workflows(failures, names)
    elif args.scope == "agents":
        scope_agents(failures)
    elif args.scope == "rules":
        scope_rules(failures)
    elif args.scope == "qa":
        scope_qa(failures)
    elif args.scope == "docs":
        scope_docs(failures)
    else:
        scope_all(failures)
    if failures:
        for item in failures:
            print(f"FAIL: {item}")
        sys.exit(1)
    if args.scope == "support":
        print("support scope: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
