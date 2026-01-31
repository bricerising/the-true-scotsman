#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class SkillInfo:
    name: str
    description: str
    skill_md_rel: str


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def _git_short_sha(repo_dir: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_dir), "rev-parse", "--short", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None

    sha = result.stdout.strip()
    return sha or None


def _repo_version(repo_dir: Path) -> str:
    sha = _git_short_sha(repo_dir)
    return sha or "unknown"


def _to_posix_path(path: Path) -> str:
    return path.as_posix()


def _read_frontmatter(skill_md: Path) -> Tuple[Optional[str], Optional[str]]:
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None

    name: Optional[str] = None
    description: Optional[str] = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)\s*$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2)
        if key == "name":
            name = value
        elif key == "description":
            description = value

    return name, description


def _discover_skills(repo_dir: Path, skill_order: Sequence[str]) -> List[SkillInfo]:
    skills: List[SkillInfo] = []

    for child in sorted(repo_dir.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        if not skill_md.is_file():
            continue
        name, description = _read_frontmatter(skill_md)
        skills.append(
            SkillInfo(
                name=name or child.name,
                description=description or "",
                skill_md_rel=_to_posix_path(Path(child.name) / "SKILL.md"),
            )
        )

    order_index = {name: i for i, name in enumerate(skill_order)}
    skills.sort(key=lambda s: order_index.get(s.name, 10_000))
    return skills


def _read_skill_order(config_path: Path) -> List[str]:
    try:
        import json

        data = json.loads(config_path.read_text(encoding="utf-8"))
        order = data.get("skillOrder", [])
        if isinstance(order, list):
            return [str(x) for x in order if isinstance(x, str)]
    except Exception:
        return []
    return []


def _agents_md(tool_name: str, repo_rel: str, repo_version: str, skills: Sequence[SkillInfo]) -> str:
    lines: List[str] = []
    lines.append("# Progressive Disclosure Skill Rules")
    lines.append("")
    lines.append(
        f"This project vendors the-true-scotsman skills at `{repo_rel}` (version: `{repo_version}`)."
    )
    lines.append("")
    lines.append("## Rules")
    lines.append("")
    lines.append("- DO NOT load all skill files at once.")
    lines.append("- First, decide which skill(s) apply (language + task keywords).")
    lines.append("- Then open only the relevant `*/SKILL.md` files and follow their workflows.")
    lines.append("- Use a tight loop: **Evaluate → Implement → Verify** (run checks until green).")
    lines.append("")
    lines.append("## Workflow")
    lines.append("")
    lines.append("1. **Evaluate**: restate the goal + constraints; identify entry points; pick 1–3 relevant skills.")
    lines.append("2. **Implement**: make the smallest change that meets the goal; keep diffs reviewable.")
    lines.append("3. **Verify**: run tests/lint/build; iterate until green; summarize behavior changes (if any).")
    lines.append("")
    lines.append("## Quick Picker")
    lines.append("")
    for s in skills:
        rel = f"{repo_rel}/{s.skill_md_rel}"
        if s.name == "select-design-pattern":
            lines.append(f"- Need to choose a GoF pattern: `{rel}` (use before any `apply-*` skills)")
        elif s.name == "consumer-test-coverage":
            lines.append(f"- Adding/expanding consumer-facing tests: `{rel}`")
        elif s.name == "typescript-style-guide":
            lines.append(f"- Working in TypeScript code: `{rel}`")
        elif s.name.startswith("apply-"):
            lines.append(f"- Applying a GoF pattern: `{rel}`")
        else:
            lines.append(f"- `{s.name}`: `{rel}`")
    lines.append("")
    lines.append("## Helper: Recommend Skills")
    lines.append("")
    lines.append("If you're unsure which skill(s) to use, run:")
    lines.append("")
    lines.append(f"`python3 {repo_rel}/scripts/recommend-skills.py --project-dir . --prompt \"<your prompt>\"`")
    lines.append("")
    lines.append("## Skill Index")
    lines.append("")
    for s in skills:
        rel = f"{repo_rel}/{s.skill_md_rel}"
        desc = f" - {s.description}" if s.description else ""
        lines.append(f"- `{s.name}`: `{rel}`{desc}")
    lines.append("")
    lines.append(f"(Generated for {tool_name}.)")
    lines.append("")
    return "\n".join(lines)


def _write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} already exists (use --force to overwrite)")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Generate tool instruction files (Codex/Claude/Cursor/Copilot) for a project."
    )
    parser.add_argument("--project-dir", default=".", help="Project directory to write into (default: .)")
    parser.add_argument("--repo-dir", help="Path to the-true-scotsman repo (default: inferred from script)")
    parser.add_argument("--tool", choices=("codex", "claude", "cursor", "copilot", "all"), default="all")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args(list(argv))

    repo_dir = Path(args.repo_dir).resolve() if args.repo_dir else _repo_root_from_script()
    project_dir = Path(args.project_dir).resolve()

    config_path = repo_dir / "skills-config.json"
    skill_order = _read_skill_order(config_path) if config_path.is_file() else []
    skills = _discover_skills(repo_dir, skill_order)
    repo_version = _repo_version(repo_dir)

    repo_rel = os.path.relpath(repo_dir, project_dir)
    repo_rel = Path(repo_rel).as_posix()

    if args.tool in ("codex", "all"):
        content = _agents_md("Codex", repo_rel, repo_version, skills)
        _write_file(project_dir / ".codex" / "AGENTS.md", content, args.force)

    if args.tool in ("claude", "all"):
        content = _agents_md("Claude", repo_rel, repo_version, skills)
        _write_file(project_dir / ".claude" / "AGENTS.md", content, args.force)

    if args.tool in ("cursor", "all"):
        content = _agents_md("Cursor", repo_rel, repo_version, skills)
        _write_file(project_dir / ".cursorrules", content, args.force)

    if args.tool in ("copilot", "all"):
        content = _agents_md("GitHub Copilot", repo_rel, repo_version, skills)
        _write_file(project_dir / ".github" / "copilot-instructions.md", content, args.force)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
