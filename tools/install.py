#!/usr/bin/env python3
"""Install the complete local library without replacing existing skills."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def plan(source: Path, destination: Path):
    manifest = json.loads((source / "reconstruct-orchestrate/references/skill-map.json").read_text())
    names = [item["name"] for item in manifest["skills"]]
    if len(names) != len(set(names)) or not names:
        raise ValueError("The skill manifest is empty or contains duplicate names")
    for name in names:
        if Path(name).name != name or not name.startswith("reconstruct-"):
            raise ValueError(f"Invalid skill name: {name}")
        if not (source / name / "SKILL.md").is_file():
            raise ValueError(f"Missing skill: {name}")
        if destination.resolve().is_relative_to((source / name).resolve()):
            raise ValueError(f"Destination cannot be inside source skill: {source / name}")
        target = destination / name
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Refusing to replace existing skill: {target}")
    return names


def install(source: Path, destination: Path, dry_run=False):
    names = plan(source, destination)
    if dry_run:
        return names
    destination.mkdir(parents=True, exist_ok=True)
    # Stage every source before exposing any skill; only this process's new paths
    # are removed on failure. No overwrite or hidden update behavior is provided.
    created = []
    with tempfile.TemporaryDirectory(prefix=".reconstruct-install-", dir=destination) as staging:
        staging = Path(staging)
        for name in names:
            shutil.copytree(source / name, staging / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        try:
            for name in names:
                target = destination / name
                target.mkdir()  # exclusive reservation; catches a concurrent install
                created.append(target)
                shutil.copytree(staging / name, target, dirs_exist_ok=True)
                if os.name == "posix":
                    # Windows-mounted source trees commonly report mode 0777.
                    # New user skills should not inherit group/world write access.
                    for path in [target, *target.rglob("*")]:
                        path.chmod(0o755 if path.is_dir() or path.suffix == ".py" else 0o644)
        except BaseException:
            for target in reversed(created):
                shutil.rmtree(target)
            raise
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT / "skills")
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        names = install(args.source.resolve(), args.dest.expanduser().resolve(), args.dry_run)
    except (OSError, ValueError, KeyError) as exc:
        print(f"Install stopped: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"action": "planned" if args.dry_run else "installed",
                      "destination": str(args.dest.expanduser().resolve()), "skills": names}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
