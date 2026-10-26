#!/usr/bin/env python3
"""Check library discovery, sibling dependencies and local Markdown references."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def validate(root: Path):
    errors = []
    try:
        manifest = json.loads((root / "reconstruct-orchestrate/references/skill-map.json").read_text())
        items = manifest["skills"]
        names = [item["name"] for item in items]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return [f"Cannot read skill map: {exc}"]
    if not names or len(names) != len(set(names)):
        errors.append("Skill map must contain distinct names")
    discovered = {p.parent.name for p in root.glob("*/SKILL.md")}
    if discovered != set(names):
        errors.append(f"Skill map/discovery mismatch: {sorted(discovered ^ set(names))}")
    for item in items:
        name = item["name"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
            errors.append(f"Invalid skill name: {name}")
            continue
        path = root / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing {path}")
            continue
        content = path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
        if not match:
            errors.append(f"{name}: missing YAML frontmatter")
            continue
        # Authored metadata uses a deliberate simple scalar subset. Official
        # skill-creator quick_validate is a separate full frontmatter check.
        fields = dict(re.findall(r"^([a-z_-]+):\s*(.+)$", match.group(1), re.M))
        if fields.get("name", "").strip('"\'') != name:
            errors.append(f"{name}: frontmatter/directory name mismatch")
        description = fields.get("description", "").strip('"\'')
        if not description or len(description) > 1024:
            errors.append(f"{name}: invalid description length")
        if len(content.splitlines()) >= 500:
            errors.append(f"{name}: entrypoint exceeds library's 499-line limit")
        for dependency in item.get("requires_skills", []):
            if dependency not in names or dependency == name:
                errors.append(f"{name}: invalid dependency {dependency}")
        for key in ("purpose", "activate_when", "prerequisites", "outputs"):
            if not item.get(key):
                errors.append(f"{name}: missing manifest {key}")
        ui = root / name / "agents/openai.yaml"
        if not ui.is_file():
            errors.append(f"{name}: missing UI metadata")

    graph = {item["name"]: item.get("requires_skills", []) for item in items}
    active, visited = set(), set()

    def visit(name):
        if name in active:
            errors.append(f"Cyclic installation dependency at {name}")
            return
        if name in visited:
            return
        active.add(name)
        for dependency in graph.get(name, []):
            visit(dependency)
        active.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)
    for path in root.rglob("*.md"):
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            target = target.split("#", 1)[0].strip("<>")
            if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            local = (path.parent / unquote(target)).resolve()
            try:
                local.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{path.relative_to(root)}: link escapes installed library: {target}")
                continue
            if not local.exists():
                errors.append(f"{path.relative_to(root)}: broken local link: {target}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills", type=Path, default=ROOT / "skills")
    args = parser.parse_args()
    errors = validate(args.skills)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("PASS: skill discovery, metadata, dependencies and local references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
