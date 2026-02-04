from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


class SkillsDirError(RuntimeError):
    pass


def resolve_skills_dir(provided: Optional[Path]) -> Path:
    if provided:
        return _validate_skills_dir(provided)

    env = os.environ.get("ESB_SKILLS_DIR")
    if env:
        return _validate_skills_dir(Path(env))

    # Default install location (Codex skills live under ~/.codex/skills).
    default = Path.home() / ".codex" / "skills"
    if default.exists() and default.is_dir():
        return _validate_skills_dir(default)

    # Auto-detect: walk up from cwd looking for review-protocol/SKILL.md
    cwd = Path.cwd().resolve()
    for root in [cwd, *cwd.parents]:
        candidate = root / "review-protocol" / "SKILL.md"
        if candidate.exists():
            return _validate_skills_dir(root)

    raise SkillsDirError(
        "Could not locate enterprise-software-playbook skills root. Provide --skills-dir or set ESB_SKILLS_DIR."
    )


def _validate_skills_dir(skills_dir: Path) -> Path:
    skills_dir = skills_dir.resolve()
    required = [
        skills_dir / "review-protocol" / "SKILL.md",
        skills_dir / "enterprise-web-app-workflow" / "SKILL.md",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SkillsDirError(f"Invalid skills dir (missing required files): {missing}")
    return skills_dir


def skill_hints_markdown(skills_dir: Path, *, review_type: str, max_chars: int = 8_000) -> str:
    """
    Returns an optional, bounded markdown hint pulled from the skill library to guide reviewers.
    """
    from langchain_clis.code_review.config import ReviewType

    rt = ReviewType(review_type)
    skill_files = _skill_files_for_review_type(rt)
    if not skill_files:
        return ""

    parts: list[str] = []
    for rel in skill_files:
        path = skills_dir / rel
        if not path.exists():
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        parts.append(f"## {rel}\n\n{_strip_frontmatter(raw).strip()}\n")

    if not parts:
        return ""
    merged = "\n".join(parts).strip() + "\n"
    if len(merged) <= max_chars:
        return merged
    return merged[: max_chars - 200] + "\n\n[... skill hints truncated ...]\n"


def skill_hints_markdown_for_task(skills_dir: Path, *, task: str, max_chars: int = 8_000) -> str:
    """
    Returns an optional, bounded markdown hint pulled from the skill library to guide non-review CLIs.
    """
    task_key = task.strip().lower()
    skill_files = _skill_files_for_task(task_key)
    if not skill_files:
        return ""

    parts: list[str] = []
    for rel in skill_files:
        path = skills_dir / rel
        if not path.exists():
            continue
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        parts.append(f"## {rel}\n\n{_strip_frontmatter(raw).strip()}\n")

    if not parts:
        return ""
    merged = "\n".join(parts).strip() + "\n"
    if len(merged) <= max_chars:
        return merged
    return merged[: max_chars - 200] + "\n\n[... skill hints truncated ...]\n"


def _skill_files_for_review_type(review_type: "ReviewType") -> list[Path]:
    # Keep this intentionally small to avoid exploding context.
    from langchain_clis.code_review.config import ReviewType

    if review_type == ReviewType.security:
        return [Path("apply-security-patterns/SKILL.md")]
    if review_type == ReviewType.resilience:
        return [Path("apply-resilience-patterns/SKILL.md")]
    if review_type in (ReviewType.testing, ReviewType.correctness):
        return [Path("consumer-test-coverage/SKILL.md")]
    if review_type == ReviewType.performance:
        return [Path("apply-observability-patterns/SKILL.md")]
    if review_type == ReviewType.maintainability:
        return [Path("typescript-style-guide/SKILL.md")]
    if review_type == ReviewType.architecture:
        return [Path("select-architecture-pattern/SKILL.md"), Path("select-design-pattern/SKILL.md")]
    if review_type == ReviewType.api_design:
        return [Path("spec-driven-development/SKILL.md"), Path("shared-platform-library/SKILL.md")]
    if review_type == ReviewType.general:
        return [Path("enterprise-web-app-workflow/SKILL.md")]
    return []


def _skill_files_for_task(task: str) -> list[Path]:
    # Keep this intentionally small to avoid exploding context.
    if task == "ideation":
        return [Path("enterprise-web-app-workflow/SKILL.md"), Path("spec-driven-development/SKILL.md")]
    if task == "progress":
        return [Path("enterprise-web-app-workflow/SKILL.md"), Path("spec-driven-development/SKILL.md")]
    if task == "spec-alignment":
        return [Path("spec-driven-development/SKILL.md")]
    return []


def _strip_frontmatter(markdown: str) -> str:
    lines = markdown.splitlines()
    if len(lines) >= 2 and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1 :])
    return markdown
