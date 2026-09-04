"""Deterministic CCGS → Aesir path mapping and Markdown conversion."""

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath

HOOK_RENAMES = {
    "detect-gaps.sh": "detect-project-gaps.sh",
    "log-agent-stop.sh": "log-subagent-stop.sh",
    "log-agent.sh": "log-subagent-start.sh",
    "notify.sh": "notify-session.sh",
    "post-compact.sh": "restore-session-context.sh",
    "pre-compact.sh": "checkpoint-session-state.sh",
    "session-start.sh": "session-start.sh",
    "session-stop.sh": "session-end.sh",
    "validate-assets.sh": "validate-project-assets.sh",
    "validate-commit.sh": "validate-commit.sh",
    "validate-push.sh": "validate-push.sh",
    "validate-skill-change.sh": "validate-aesir-skill-change.sh",
}

ATTRIBUTION = (
    "> **Upstream:** Derived from Claude Code Game Studios by Donchitos (MIT). "
    "https://github.com/Donchitos/Claude-Code-Game-Studios — adapted for Hermes Agent / Aesir Gameworks.\n"
)

DELEGATION_CONTRACT = """
## Delegation Contract

- **Required inputs:** goal, relevant workspace paths, constraints, and any prior verdicts.
- **Allowed decision scope:** recommendations and domain analysis only; the user owns creative and strategic decisions.
- **Expected return schema:** `status`, `findings`, `recommendations`, `blockers`, `artifacts`.
- **Escalation:** send unresolved cross-domain conflicts to the matching director/lead listed in this skill.
- **Context:** the parent must pass this role text in `delegate_task.context`. A delegated child must not be expected to discover parent-only context.
"""

FENCE_RE = re.compile(r"(```[\s\S]*?```|~~~[\s\S]*?~~~)")
FRONTMATTER_RE = re.compile(r"^---\n([\s\S]*?)\n---\n?", re.M)

TOOL_PHRASES = [
    (re.compile(r"\bAskUserQuestion\b"), "clarify"),
    (re.compile(r"\bWebSearch\b"), "web_search"),
    (re.compile(r"\bWebFetch\b"), "web_extract"),
    (re.compile(r"\bthe Task tool\b"), "the delegate_task tool"),
    (re.compile(r"`Task`"), "`delegate_task`"),
    (re.compile(r"\bTask subagent\b"), "delegate_task subagent"),
    (re.compile(r"\bUse Task\b"), "Use delegate_task"),
    (re.compile(r"\bthe Read tool\b"), "the read_file tool"),
    (re.compile(r"`Read`"), "`read_file`"),
    (re.compile(r"\bthe Glob tool\b"), "the search_files tool"),
    (re.compile(r"`Glob`"), "`search_files`"),
    (re.compile(r"\bthe Grep tool\b"), "the search_files tool"),
    (re.compile(r"`Grep`"), "`search_files`"),
    (re.compile(r"\bthe Write tool\b"), "the write_file tool"),
    (re.compile(r"`Write`"), "`write_file`"),
    (re.compile(r"\bthe Edit tool\b"), "the patch tool"),
    (re.compile(r"`Edit`"), "`patch`"),
    (re.compile(r"\bthe Bash tool\b"), "the terminal tool"),
    (re.compile(r"`Bash`"), "`terminal`"),
    (re.compile(r"\bGlob / Grep\b"), "search_files"),
    (re.compile(r"\bGlob/Grep\b"), "search_files"),
]


def map_source(src: str) -> tuple[str, list[str]]:
    """Return (action, destinations) using deterministic path rules."""
    posix = PurePosixPath(src)
    name = posix.name
    if name == ".DS_Store" or name == ".gitkeep":
        return "delete", []
    if src == "LICENSE":
        return "preserve", ["LICENSE"]
    if src in {".gitignore", "README.md", "CONTRIBUTING.md", "SECURITY.md"}:
        return "rewrite", [src]
    if src == "CLAUDE.md":
        return "split", [
            "SOUL.md",
            "skills/aesir-core/aesir-gameworks/references/original-studio-architecture.md",
        ]
    if src == ".claude/settings.json":
        return "split", [
            "config.yaml",
            "skills/aesir-core/aesir-gameworks/references/upstream/claude-settings.json",
        ]
    if src == "UPGRADING.md":
        return "rewrite", ["skills/aesir-core/aesir-gameworks/references/upstream/UPGRADING-CCGS.md"]
    if src == ".claude/docs/CLAUDE-local-template.md":
        return "rewrite", ["skills/aesir-support/aesir-project-bootstrap/templates/AGENTS.md"]
    if src == ".claude/docs/settings-local-template.md":
        return "rewrite", ["skills/aesir-core/aesir-gameworks/references/profile-settings-template.md"]
    if src == ".claude/statusline.sh":
        return "rewrite", ["skills/aesir-support/aesir-studio-status/scripts/status.sh"]
    if src == "CCGS Skill Testing Framework/catalog.yaml":
        return "rewrite", ["skills/aesir-quality/aesir-framework-qa/references/catalog.yaml"]
    if src == "CCGS Skill Testing Framework/CLAUDE.md":
        return "convert", ["skills/aesir-quality/aesir-framework-qa/references/authoring-policy.md"]
    if src == "CCGS Skill Testing Framework/README.md":
        return "convert", ["skills/aesir-quality/aesir-framework-qa/references/README.md"]
    if src == "CCGS Skill Testing Framework/quality-rubric.md":
        return "convert", ["skills/aesir-quality/aesir-framework-qa/references/quality-rubric.md"]
    if src == "CCGS Skill Testing Framework/templates/agent-test-spec.md":
        return "convert", ["skills/aesir-quality/aesir-framework-qa/templates/agent-test-spec.md"]
    if src == "CCGS Skill Testing Framework/templates/skill-test-spec.md":
        return "convert", ["skills/aesir-quality/aesir-framework-qa/templates/skill-test-spec.md"]
    if src.startswith(".claude/hooks/"):
        return "rewrite", [f"agent-hooks/aesir-gameworks/{HOOK_RENAMES[name]}"]
    if src.startswith(".claude/agents/") and src.endswith(".md"):
        stem = posix.stem
        return "convert", [f"skills/aesir-agents/aesir-agent-{stem}/SKILL.md"]
    if src.startswith(".claude/rules/") and src.endswith(".md"):
        stem = posix.stem
        return "convert", [f"skills/aesir-rules/aesir-rule-{stem}/SKILL.md"]
    if src.startswith(".claude/skills/") and src.endswith("/SKILL.md"):
        stem = posix.parts[2]
        return "convert", [f"skills/aesir-workflows/aesir-{stem}/SKILL.md"]
    if src == ".claude/agent-memory/lead-programmer/MEMORY.md":
        return "convert", ["skills/aesir-agents/aesir-agent-lead-programmer/references/upstream-memory.md"]
    if src.startswith(".claude/docs/templates/"):
        rel = "/".join(posix.parts[3:])
        return "convert", [f"skills/aesir-support/aesir-project-templates/templates/{rel}"]
    if src.startswith(".claude/docs/hooks-reference/"):
        rel = "/".join(posix.parts[3:])
        return "convert", [f"skills/aesir-core/aesir-gameworks/references/hooks/{rel}"]
    if src.startswith(".claude/docs/"):
        rel = "/".join(posix.parts[2:])
        return "convert", [f"skills/aesir-core/aesir-gameworks/references/{rel}"]
    if src.startswith("CCGS Skill Testing Framework/skills/"):
        stem = posix.stem
        return "convert", [f"skills/aesir-workflows/aesir-{stem}/references/behavior-spec.md"]
    if src.startswith("CCGS Skill Testing Framework/agents/"):
        stem = posix.stem
        return "convert", [f"skills/aesir-agents/aesir-agent-{stem}/references/behavior-spec.md"]
    if src == "design/CLAUDE.md":
        return "convert", ["skills/aesir-core/aesir-gameworks/references/project-policies/design.md"]
    if src == "design/registry/entities.yaml":
        return "convert", ["skills/aesir-support/aesir-project-templates/templates/registries/entities.yaml"]
    if src == "docs/CLAUDE.md":
        return "convert", ["skills/aesir-core/aesir-gameworks/references/project-policies/documentation.md"]
    if src == "docs/COLLABORATIVE-DESIGN-PRINCIPLE.md":
        return "convert", ["skills/aesir-core/aesir-gameworks/references/collaborative-design-principle.md"]
    if src == "docs/WORKFLOW-GUIDE.md":
        return "convert", ["skills/aesir-core/aesir-gameworks/references/workflow-guide.md"]
    if src == "docs/architecture/tr-registry.yaml":
        return "convert", ["skills/aesir-support/aesir-project-templates/templates/registries/tr-registry.yaml"]
    if src == "docs/registry/architecture.yaml":
        return "convert", ["skills/aesir-support/aesir-project-templates/templates/registries/architecture.yaml"]
    if src == "docs/engine-reference/README.md":
        return "convert", ["skills/aesir-engines/aesir-engine-reference/references/README.md"]
    if src.startswith("docs/engine-reference/"):
        rel = "/".join(posix.parts[2:])
        return "convert", [f"skills/aesir-engines/aesir-engine-reference/references/{rel}"]
    if src.startswith("docs/examples/"):
        rel = "/".join(posix.parts[2:])
        return "convert", [f"skills/aesir-core/aesir-gameworks/examples/{rel}"]
    if src == "src/CLAUDE.md":
        return "convert", ["skills/aesir-core/aesir-gameworks/references/project-policies/source.md"]
    raise KeyError(f"unmapped source: {src}")


def kind_for(src: str, dest: str) -> str:
    if dest.endswith("/SKILL.md") and "/aesir-workflows/" in dest:
        return "workflow"
    if dest.endswith("/SKILL.md") and "/aesir-agents/" in dest:
        return "agent"
    if dest.endswith("/SKILL.md") and "/aesir-rules/" in dest:
        return "rule"
    if dest.endswith("behavior-spec.md"):
        return "behavior-spec"
    if dest.endswith(".sh"):
        return "shell"
    return "reference"


def source_name_for(src: str, dest: str) -> str:
    posix = PurePosixPath(dest if dest else src)
    if posix.name == "SKILL.md":
        return posix.parent.name.removeprefix("aesir-agent-").removeprefix("aesir-rule-").removeprefix("aesir-")
    if posix.name == "behavior-spec.md":
        return posix.parts[-3].removeprefix("aesir-agent-").removeprefix("aesir-rule-").removeprefix("aesir-")
    return PurePosixPath(src).stem


def _parse_yaml_simple(block: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in block.splitlines():
        if ":" not in raw or raw.startswith(" ") or raw.startswith("-"):
            continue
        key, _, value = raw.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def _hermes_frontmatter(kind: str, source_name: str, original: dict[str, str]) -> str:
    original_desc = original.get("description", "").strip()
    if kind == "workflow":
        name = f"aesir-{source_name}"
        trigger = f"Use when running the Aesir {source_name} workflow."
        tags = "workflow"
        related = "[aesir-gameworks]"
    elif kind == "agent":
        name = f"aesir-agent-{source_name}"
        trigger = f"Use when delegating work to the {source_name} role."
        tags = "agent-role"
        related = "[aesir-gameworks]"
    elif kind == "rule":
        name = f"aesir-rule-{source_name}"
        trigger = f"Use when changing files governed by {source_name} rules."
        tags = "path-rules"
        related = "[aesir-gameworks]"
    else:
        name = original.get("name", source_name)
        trigger = original_desc or f"Use when working with Aesir {source_name}."
        tags = "reference"
        related = "[aesir-gameworks]"
    description = trigger if not original_desc or original_desc.startswith("Use when") else f"{trigger} {original_desc}"
    description = description.replace('"', "'")
    return (
        "---\n"
        f"name: {name}\n"
        f"description: \"{description}\"\n"
        "version: 1.0.0\n"
        'author: "Donchitos; Hermes adaptation by Aesir Gameworks"\n'
        "license: MIT\n"
        "metadata:\n"
        "  hermes:\n"
        f"    tags: [aesir-gameworks, game-development, {tags}]\n"
        f"    related_skills: {related}\n"
        "---\n"
    )


def _slash_replacer(names: list[str]):
    ordered = sorted(set(names), key=len, reverse=True)
    pattern = re.compile(
        r"(?<![A-Za-z0-9_-])/(?!aesir-)(" + "|".join(re.escape(n) for n in ordered) + r")(?![A-Za-z0-9_-])"
    )

    def repl(match: re.Match) -> str:
        return f"/aesir-{match.group(1)}"

    return lambda text: pattern.sub(repl, text)


def _rewrite_claude_paths(text: str) -> str:
    text = text.replace("../modules/input.md", "modules/input.md")
    text = text.replace("../modules/ui.md", "modules/ui.md")
    text = text.replace(".claude/docs/templates/", "skill_view('aesir-project-templates', file_path='templates/")
    # Fix the above if it created unclosed quotes: do targeted regex instead.
    return text


def _rewrite_paths(text: str) -> str:
    replacements = [
        (".claude/docs/templates/", "aesir-project-templates templates/"),
        (".claude/docs/hooks-reference/", "aesir-gameworks references/hooks/"),
        (".claude/docs/", "aesir-gameworks references/"),
        (".claude/hooks/", "agent-hooks/aesir-gameworks/"),
        (".claude/statusline.sh", "aesir-studio-status scripts/status.sh"),
        ("CCGS Skill Testing Framework/skills/", "aesir-workflows behavior specs: "),
        ("CCGS Skill Testing Framework/", "aesir-framework-qa references/"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    text = re.sub(r"\.claude/agents/([A-Za-z0-9_-]+)(?:\.md)?", r"skill_view('aesir-agent-\1')", text)
    text = re.sub(r"\.claude/skills/([A-Za-z0-9_-]+)", r"skill_view('aesir-\1')", text)
    text = re.sub(r"\.claude/rules/([A-Za-z0-9_-]+)(?:\.md)?", r"skill_view('aesir-rule-\1')", text)
    text = text.replace(".claude/", "(game-workspace)/")
    return text


def _transform_live(text: str, prefix_slash) -> str:
    text = _rewrite_paths(text)
    text = prefix_slash(text)
    for pattern, repl in TOOL_PHRASES:
        text = pattern.sub(repl, text)
    text = re.sub(r"\bRead, Glob, Grep, Bash, Write, Task, clarify\b", "read_file, search_files, terminal, write_file, delegate_task, clarify", text)
    text = re.sub(r"\bRead, Glob, Grep, Write, Edit, Bash, web_search\b", "read_file, search_files, write_file, patch, terminal, web_search", text)
    text = re.sub(r"\bRead, Glob, Grep, Write, Edit, Bash\b", "read_file, search_files, write_file, patch, terminal", text)
    text = re.sub(r"\bRead, Glob, Grep\b", "read_file, search_files", text)
    text = text.replace("Claude Code Game Studios", "Aesir Gameworks")
    text = text.replace("Claude Code", "Hermes Agent")
    text = text.replace("built for-Claude", "built for-Hermes")
    return text


def convert_markdown(text: str, *, kind: str, source_name: str, workflow_names: list[str] | None = None) -> str:
    """Return Hermes-native Markdown without mutating the source file.

    kind is one of: workflow, agent, rule, reference, behavior-spec.
    It must preserve fenced examples, rewrite live instructions and links,
    add MIT/upstream attribution, and produce valid Hermes frontmatter for
    workflow/agent/rule documents.
    """
    workflow_names = workflow_names or []
    prefix_slash = _slash_replacer(workflow_names) if workflow_names else (lambda s: s)
    original_fm: dict[str, str] = {}
    body = text
    fm_match = FRONTMATTER_RE.match(text)
    if fm_match:
        original_fm = _parse_yaml_simple(fm_match.group(1))
        body = text[fm_match.end() :]
    pieces: list[str] = []
    last = 0
    for fence in FENCE_RE.finditer(body):
        pieces.append(_transform_live(body[last:fence.start()], prefix_slash))
        fenced = fence.group(0)
        # Convert instruction-like fences; leave engine/code samples mostly intact
        # except forbidden runtime tokens that contract tests scan for in SKILL.md.
        if kind in {"workflow", "agent", "rule", "behavior-spec"}:
            fenced = prefix_slash(fenced)
            for pattern, repl in TOOL_PHRASES:
                fenced = pattern.sub(repl, fenced)
            fenced = fenced.replace(".claude/", "(game-workspace)/")
        pieces.append(fenced)
        last = fence.end()
    pieces.append(_transform_live(body[last:], prefix_slash))
    converted_body = "".join(pieces).lstrip("\n")
    if ATTRIBUTION.strip() not in converted_body:
        converted_body = ATTRIBUTION + "\n" + converted_body
    if kind in {"workflow", "agent", "rule"}:
        header = _hermes_frontmatter(kind, source_name, original_fm)
        if kind == "agent" and "## Delegation Contract" not in converted_body:
            converted_body = converted_body.rstrip() + "\n" + DELEGATION_CONTRACT
        if kind == "rule" and "target game workspace" not in converted_body:
            converted_body += (
                "\n## Scope\n\n"
                "These rules apply to a target game workspace, not the Aesir profile repository.\n"
            )
        return header + "\n" + converted_body
    if kind == "behavior-spec":
        converted_body = converted_body.replace("argument-hint", "invocation arguments")
        converted_body = converted_body.replace("allowed-tools", "Hermes tools")
        converted_body = converted_body.replace("user-invocable", "user-invocable (Hermes skill)")
    return converted_body if converted_body.endswith("\n") else converted_body + "\n"


def convert_catalog(text: str, workflow_names: list[str], agent_names: list[str]) -> str:
    import yaml

    data = yaml.safe_load(text) or {}
    for skill in data.get("skills") or []:
        name = str(skill.get("name") or "")
        if name and not name.startswith("aesir-"):
            skill["name"] = f"aesir-{name}"
        spec = str(skill.get("spec") or "")
        match = re.search(r"/([A-Za-z0-9_-]+)\.md$", spec)
        if match:
            skill["spec"] = f"skills/aesir-workflows/aesir-{match.group(1)}/references/behavior-spec.md"
    for agent in data.get("agents") or []:
        name = str(agent.get("name") or "")
        if name and not name.startswith("aesir-"):
            agent["name"] = f"aesir-agent-{name}"
        spec = str(agent.get("spec") or "")
        match = re.search(r"/([A-Za-z0-9_-]+)\.md$", spec)
        if match:
            agent["spec"] = f"skills/aesir-agents/aesir-agent-{match.group(1)}/references/behavior-spec.md"
    names = {s.get("name") for s in data.get("skills") or []}
    if "aesir-vertical-slice" not in names:
        data.setdefault("skills", []).append(
            {
                "name": "aesir-vertical-slice",
                "spec": "skills/aesir-workflows/aesir-vertical-slice/references/behavior-spec.md",
                "last_static": "",
                "last_static_result": "",
                "last_spec": "",
                "last_spec_result": "",
                "last_category": "",
                "last_category_result": "",
                "priority": "high",
                "category": "utility",
            }
        )
    dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
    return ATTRIBUTION.replace("> **Upstream:**", "# Upstream:") + dumped
