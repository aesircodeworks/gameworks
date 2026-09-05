#!/usr/bin/env python3
"""Capture and verify live-profile preservation without printing secrets."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

import yaml

PROTECTED_NAMES = {
    ".env",
    "auth.json",
    "state.db",
    "state.db-shm",
    "state.db-wal",
    "hermes_state.db",
    "response_store.db",
    "response_store.db-shm",
    "response_store.db-wal",
}
PROTECTED_DIRS = {
    "memories",
    "sessions",
    "logs",
    "cache",
    "image_cache",
    "audio_cache",
    "document_cache",
    "browser_screenshots",
    "checkpoints",
    "sandboxes",
    "backups",
}
HERMES_AGENT = Path("skills/autonomous-ai-agents/hermes-agent")
DEFAULT_OWNED = (
    "SOUL.md",
    "config.yaml",
    "distribution.yaml",
    "skills/studio",
    "skills/workflows",
    "skills/agents",
    "skills/rules",
    "skills/engines",
    "skills/quality",
    "skills/support",
    "agent-hooks/aesir-gameworks",
    "skill-bundles/aesir-gameworks.yaml",
)
POLICY_KEYS = {
    "approvals.mode",
    "approvals.deny",
    "command_allowlist",
    "memory.write_approval",
    "skills.write_approval",
    "delegation.max_concurrent_children",
    "checkpoints.enabled",
    "agent.verify_on_stop",
    "hooks",
    "hooks_auto_accept",
}
INSTALLER_META = {"distribution.yaml"}


def _chmod_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, stat.S_IRWXU)


def _chmod_private_file(path: Path) -> None:
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_owned(rel: str, owned: tuple[str, ...]) -> bool:
    return any(rel == item or rel.startswith(item.rstrip("/") + "/") for item in owned)


def walk_files(home: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for path in sorted(home.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = _rel(path, home)
        files[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def capture(home: Path, output: Path, owned: tuple[str, ...] = DEFAULT_OWNED) -> None:
    _chmod_private_dir(output.parent)
    files = walk_files(home)
    config = None
    cfg_path = home / "config.yaml"
    if cfg_path.is_file():
        config = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
    payload = {
        "profile_home": str(home),
        "files": files,
        "owned": list(owned),
        "config": config,
        "protected": sorted(
            rel
            for rel in files
            if Path(rel).name in PROTECTED_NAMES
            or rel.split("/", 1)[0] in PROTECTED_DIRS
            or rel.startswith(HERMES_AGENT.as_posix() + "/")
            or rel == HERMES_AGENT.as_posix() + "/SKILL.md"
            or rel.startswith(HERMES_AGENT.as_posix())
        ),
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _chmod_private_file(output)


def _nested_get(data: dict, dotted: str):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return object()
        cur = cur[part]
    return cur


def verify(home: Path, baseline_path: Path) -> int:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    owned = tuple(baseline.get("owned") or DEFAULT_OWNED)
    before = baseline["files"]
    after = walk_files(home)
    problems: list[str] = []
    for rel, digest in before.items():
        if _is_owned(rel, owned):
            continue
        if rel not in after:
            problems.append(f"deleted {rel}")
        elif after[rel] != digest:
            problems.append(f"changed {rel}")
    for rel in after:
        if rel in before:
            continue
        if _is_owned(rel, owned) or Path(rel).name in INSTALLER_META or rel in INSTALLER_META:
            continue
        # empty bootstrap dirs are not files; new files outside owned fail
        problems.append(f"added {rel}")
    if baseline.get("config") is not None and (home / "config.yaml").is_file():
        now = yaml.safe_load((home / "config.yaml").read_text(encoding="utf-8")) or {}
        before_cfg = baseline["config"] or {}

        def walk(prefix: str, old, new) -> None:
            if prefix.lstrip(".") in POLICY_KEYS or any(prefix.lstrip(".").startswith(k + ".") for k in POLICY_KEYS):
                return
            if type(old) is not type(new):
                problems.append(f"config type changed {prefix or '<root>'}")
                return
            if isinstance(old, dict):
                keys = set(old) | set(new)
                for key in sorted(keys):
                    dotted = f"{prefix}.{key}" if prefix else key
                    if dotted in POLICY_KEYS:
                        continue
                    if key not in old:
                        problems.append(f"config added {dotted}")
                    elif key not in new:
                        problems.append(f"config removed {dotted}")
                    else:
                        walk(dotted, old[key], new[key])
            elif old != new:
                problems.append(f"config changed {prefix}")

        walk("", before_cfg, now)
    if problems:
        print("preservation: FAIL")
        for item in problems:
            print(item)
        return 1
    print("preservation: PASS")
    return 0


def restore_config(home: Path, baseline_path: Path) -> None:
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    config = baseline.get("config")
    if config is None:
        raise SystemExit("baseline has no config")
    dest = home / "config.yaml"
    dest.write_text(yaml.safe_dump(config, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print("restored config.yaml from baseline (values not printed)")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    cap = sub.add_parser("capture")
    cap.add_argument("--profile-home", type=Path, required=True)
    cap.add_argument("--output", type=Path, required=True)
    ver = sub.add_parser("verify")
    ver.add_argument("--profile-home", type=Path, required=True)
    ver.add_argument("--baseline", type=Path, required=True)
    rest = sub.add_parser("restore-config")
    rest.add_argument("--profile-home", type=Path, required=True)
    rest.add_argument("--baseline", type=Path, required=True)
    args = parser.parse_args()
    if args.cmd == "capture":
        capture(args.profile_home.expanduser().resolve(), args.output.expanduser())
        print(str(args.output))
        return
    if args.cmd == "restore-config":
        restore_config(args.profile_home.expanduser().resolve(), args.baseline.expanduser())
        return
    sys.exit(verify(args.profile_home.expanduser().resolve(), args.baseline.expanduser()))


if __name__ == "__main__":
    main()
