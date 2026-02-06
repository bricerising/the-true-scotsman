#!/usr/bin/env python3
"""
Check repo-level skill documentation consistency.

This script enforces lightweight drift guards for:
- workflow-stage headings in README/PROMPTS
- skill discoverability in README
- skill usability prompts in PROMPTS
"""

import re
import sys
from pathlib import Path

REQUIRED_WORKFLOW_HEADINGS = (
    "Define (what are we building?)",
    "Standardize (make it consistent)",
    "Harden (make it survive reality)",
    "Verify (prove behavior)",
    "Mechanics (in-process building blocks)",
)

PATTERN_SKILLS = {
    "patterns-creational",
    "patterns-structural",
    "patterns-behavioral",
}


def _load_text(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {path}")


def _check_headings(readme_text: str, prompts_text: str, errors: list[str]) -> None:
    for heading in REQUIRED_WORKFLOW_HEADINGS:
        if heading not in readme_text:
            errors.append(f"README.md missing workflow heading: {heading}")
        if heading not in prompts_text:
            errors.append(f"PROMPTS.md missing workflow heading: {heading}")


def _check_readme_skills(skill_names: list[str], readme_text: str, errors: list[str]) -> None:
    for skill_name in skill_names:
        path_ref = f"skills/{skill_name}/SKILL.md"
        if path_ref not in readme_text:
            errors.append(f"README.md missing skill link: {path_ref}")


def _check_prompt_skills(skill_names: list[str], prompts_text: str, errors: list[str]) -> None:
    for skill_name in skill_names:
        if skill_name in PATTERN_SKILLS:
            if (
                "Use patterns-<creational|structural|behavioral>" in prompts_text
                or re.search(rf"\bUse\s+{re.escape(skill_name)}\b", prompts_text)
            ):
                continue
            errors.append(
                "PROMPTS.md missing pattern prompt coverage for "
                f"{skill_name} (expected combined or direct pattern prompt)"
            )
            continue

        if not re.search(rf"\bUse\s+{re.escape(skill_name)}\b", prompts_text):
            errors.append(f"PROMPTS.md missing copy/paste usage prompt for skill: {skill_name}")


def _check_finish_order(prompts_text: str, errors: list[str]) -> None:
    if "run finish first" in prompts_text.lower():
        errors.append("PROMPTS.md contains contradictory guidance: 'run finish first'")


def run_checks(repo_root: Path) -> list[str]:
    errors: list[str] = []

    readme_path = repo_root / "README.md"
    prompts_path = repo_root / "PROMPTS.md"
    skills_root = repo_root / "skills"

    readme_text = _load_text(readme_path)
    prompts_text = _load_text(prompts_path)

    if not skills_root.is_dir():
        return [f"Missing skills directory: {skills_root}"]

    skill_names = sorted(
        skill_dir.name for skill_dir in skills_root.iterdir() if skill_dir.is_dir()
    )
    _check_headings(readme_text, prompts_text, errors)
    _check_readme_skills(skill_names, readme_text, errors)
    _check_prompt_skills(skill_names, prompts_text, errors)
    _check_finish_order(prompts_text, errors)
    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    try:
        errors = run_checks(repo_root)
    except ValueError as error:
        print(f"[ERROR] {error}")
        return 1

    if errors:
        print("[ERROR] Repository consistency checks failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print("[OK] Repository consistency checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
