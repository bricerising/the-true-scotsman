#!/usr/bin/env python3
"""
Package a skill folder into a distributable .skill archive.

Usage:
    python3 package_skill.py skills/<skill-folder> ./dist
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

from quick_validate import _parse_frontmatter, validate_skill

SKIP_FILE_NAMES = {".DS_Store"}
SKIP_DIR_NAMES = {"__pycache__"}


def _load_frontmatter(skill_md: Path) -> dict[str, str]:
    content = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise ValueError("Invalid frontmatter format in SKILL.md")
    frontmatter_text = match.group(1)
    frontmatter, parse_error = _parse_frontmatter(frontmatter_text)
    if parse_error:
        raise ValueError(f"Invalid YAML in frontmatter: {parse_error}")
    return frontmatter


def _iter_skill_files(skill_dir: Path):
    for path in sorted(skill_dir.rglob("*")):
        if path.is_dir():
            continue
        if path.name in SKIP_FILE_NAMES:
            continue
        if any(part.startswith(".") for part in path.relative_to(skill_dir).parts):
            continue
        if any(part in SKIP_DIR_NAMES for part in path.relative_to(skill_dir).parts[:-1]):
            continue
        if not path.is_file():
            raise ValueError(f"Unsupported non-file entry in skill: {path}")
        yield path


def package_skill(skill_dir: Path, output_dir: Path) -> Path:
    valid, message = validate_skill(skill_dir)
    if not valid:
        raise ValueError(f"Skill validation failed: {message}")

    skill_md = skill_dir / "SKILL.md"
    frontmatter = _load_frontmatter(skill_md)
    skill_name = frontmatter.get("name", "").strip()
    if not skill_name:
        raise ValueError("Skill frontmatter is missing a non-empty 'name'")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{skill_name}.skill"

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for file_path in _iter_skill_files(skill_dir):
            relative_path = file_path.relative_to(skill_dir)
            archive_name = f"{skill_name}/{relative_path.as_posix()}"
            archive.write(file_path, archive_name)

    return archive_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Package a skill folder into a .skill archive.")
    parser.add_argument("skill_dir", help="Path to the skill folder (for example: skills/plan)")
    parser.add_argument("output_dir", help="Directory where the .skill archive will be written")
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    skill_dir = Path(args.skill_dir)
    output_dir = Path(args.output_dir)

    try:
        archive_path = package_skill(skill_dir, output_dir)
    except ValueError as error:
        print(f"[ERROR] {error}")
        return 1

    print(f"[OK] Packaged skill: {archive_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
