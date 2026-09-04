#!/usr/bin/env python3
"""Allowlisted, idempotent merge of distribution config into an existing profile."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path

import yaml

ALLOWLIST = (
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
)


def _get(data: dict, dotted: str):
    cur = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _set(data: dict, dotted: str, value) -> None:
    parts = dotted.split(".")
    cur = data
    for part in parts[:-1]:
        nxt = cur.get(part)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[part] = nxt
        cur = nxt
    cur[parts[-1]] = copy.deepcopy(value)


def _hook_identity(entry: dict) -> tuple:
    if not isinstance(entry, dict):
        return ("non-dict", repr(entry))
    return (entry.get("command"), entry.get("matcher"), entry.get("timeout"), entry.get("fail_closed"))


def merge_hooks(existing, incoming):
    if not isinstance(existing, dict):
        existing = {}
    if not isinstance(incoming, dict):
        return existing
    out = copy.deepcopy(existing)
    for event, entries in incoming.items():
        if not isinstance(entries, list):
            out[event] = copy.deepcopy(entries)
            continue
        current = list(out.get(event) or [])
        by_id = {_hook_identity(e): i for i, e in enumerate(current) if isinstance(e, dict)}
        for entry in entries:
            ident = _hook_identity(entry)
            if ident in by_id:
                current[by_id[ident]] = copy.deepcopy(entry)
            else:
                current.append(copy.deepcopy(entry))
                by_id[ident] = len(current) - 1
        out[event] = current
    return out


def merge_list(existing, incoming):
    if not isinstance(existing, list):
        existing = []
    if not isinstance(incoming, list):
        return existing
    out = list(existing)
    seen = {json_key(x) for x in out}
    for item in incoming:
        key = json_key(item)
        if key not in seen:
            out.append(copy.deepcopy(item))
            seen.add(key)
    return out


def json_key(value) -> str:
    return yaml.safe_dump(value, sort_keys=True)


def merge_config(current: dict, incoming: dict) -> dict:
    result = copy.deepcopy(current)
    for key in ALLOWLIST:
        value = _get(incoming, key)
        if value is None:
            continue
        if key == "hooks":
            _set(result, key, merge_hooks(_get(result, key), value))
        elif key in {"approvals.deny", "command_allowlist"}:
            _set(result, key, merge_list(_get(result, key) or [], value))
        else:
            _set(result, key, value)
    return result


def apply(profile_home: Path, source: Path) -> None:
    current_path = profile_home / "config.yaml"
    current = yaml.safe_load(current_path.read_text(encoding="utf-8")) if current_path.is_file() else {}
    incoming = yaml.safe_load(source.read_text(encoding="utf-8")) or {}
    if not isinstance(current, dict) or not isinstance(incoming, dict):
        raise SystemExit("config must be a mapping")
    merged = merge_config(current, incoming)
    current_path.write_text(yaml.safe_dump(merged, sort_keys=False, allow_unicode=True), encoding="utf-8")
    again = merge_config(merged, incoming)
    if again != merged:
        raise SystemExit("config merge is not idempotent")
    print(f"merged allowlisted keys into {current_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", help="profile name")
    parser.add_argument("--profile-home", type=Path)
    parser.add_argument("--from", dest="source", type=Path, required=True)
    args = parser.parse_args()
    if args.profile_home:
        home = args.profile_home
    elif args.profile:
        home = Path.home() / ".hermes" / "profiles" / args.profile
    else:
        raise SystemExit("pass --profile or --profile-home")
    apply(home.expanduser().resolve(), args.source.expanduser().resolve())


if __name__ == "__main__":
    main()
