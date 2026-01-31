#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple


@dataclass(frozen=True)
class SkillRecommendation:
    name: str
    reasons: Tuple[str, ...]


def _repo_root_from_script() -> Path:
    return Path(__file__).resolve().parent.parent


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return data


def _read_package_json_deps(project_dir: Path) -> Set[str]:
    package_json = project_dir / "package.json"
    if not package_json.is_file():
        return set()
    try:
        data = _load_json(package_json)
    except Exception:
        return set()

    deps: Set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        value = data.get(key)
        if isinstance(value, dict):
            deps.update([k for k in value.keys() if isinstance(k, str)])
    return deps


def _detect_typescript(project_dir: Path, detector: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons: List[str] = []

    markers_any = [str(x) for x in detector.get("markersAny", []) if isinstance(x, str)]
    for marker in markers_any:
        if (project_dir / marker).exists():
            reasons.append(f"Found marker file: {marker}")
            return True, reasons

    deps = _read_package_json_deps(project_dir)
    deps_any = [str(x) for x in detector.get("packageJsonDepsAny", []) if isinstance(x, str)]
    for dep in deps_any:
        if dep in deps:
            reasons.append(f"package.json dependency: {dep}")
            return True, reasons

    return False, reasons


def _compile_keyword_matcher(keyword: str) -> re.Pattern[str]:
    keyword = keyword.strip().lower()
    if not keyword:
        return re.compile(r"(?!)")

    # If it's a simple token, require word boundaries to avoid accidental matches (e.g., "test" in "latest").
    if re.fullmatch(r"[a-z0-9_-]+", keyword):
        return re.compile(rf"(?<![a-z0-9_-]){re.escape(keyword)}(?![a-z0-9_-])", re.IGNORECASE)

    return re.compile(re.escape(keyword), re.IGNORECASE)


def _prompt_triggers(prompt: str, detectors: Sequence[Dict[str, Any]]) -> Tuple[Set[str], Dict[str, List[str]]]:
    selected_skills: Set[str] = set()
    reasons_by_skill: Dict[str, List[str]] = {}

    for detector in detectors:
        name = str(detector.get("name", "detector"))
        keywords_any = [str(x) for x in detector.get("keywordsAny", []) if isinstance(x, str)]
        skills = [str(x) for x in detector.get("skills", []) if isinstance(x, str)]
        if not keywords_any or not skills:
            continue

        matched: Optional[str] = None
        for kw in keywords_any:
            if _compile_keyword_matcher(kw).search(prompt):
                matched = kw
                break

        if matched is None:
            continue

        for skill in skills:
            selected_skills.add(skill)
            reasons_by_skill.setdefault(skill, []).append(f"Prompt matched {name} keyword: {matched!r}")

    return selected_skills, reasons_by_skill


def _project_triggers(
    project_dir: Path, detectors: Sequence[Dict[str, Any]]
) -> Tuple[Set[str], Dict[str, List[str]], Dict[str, Any]]:
    selected_skills: Set[str] = set()
    reasons_by_skill: Dict[str, List[str]] = {}
    detected: Dict[str, Any] = {}

    for detector in detectors:
        name = str(detector.get("name", "detector"))
        skills = [str(x) for x in detector.get("skills", []) if isinstance(x, str)]
        if not skills:
            continue

        if name == "typescript":
            ok, reasons = _detect_typescript(project_dir, detector)
        else:
            ok, reasons = False, []

        if not ok:
            continue

        detected[name] = {"reasons": reasons}
        for skill in skills:
            selected_skills.add(skill)
            for reason in reasons:
                reasons_by_skill.setdefault(skill, []).append(f"{name}: {reason}")

    return selected_skills, reasons_by_skill, detected


def _order_skills(skills: Iterable[str], skill_order: Sequence[str]) -> List[str]:
    order_index = {name: i for i, name in enumerate(skill_order)}
    return sorted(skills, key=lambda s: order_index.get(s, 10_000))


def recommend_skills(
    project_dir: Path, prompt: str, config: Dict[str, Any]
) -> Tuple[List[SkillRecommendation], Dict[str, Any]]:
    skill_order = [str(x) for x in config.get("skillOrder", []) if isinstance(x, str)]
    project_detectors = config.get("projectDetectors", [])
    prompt_detectors = config.get("promptDetectors", [])

    if not isinstance(project_detectors, list) or not isinstance(prompt_detectors, list):
        raise ValueError("Invalid config: expected projectDetectors and promptDetectors arrays")

    project_skills, project_reasons, detected = _project_triggers(project_dir, project_detectors)
    prompt_skills, prompt_reasons = _prompt_triggers(prompt, prompt_detectors)

    combined: Set[str] = set(project_skills) | set(prompt_skills)
    ordered = _order_skills(combined, skill_order)

    recs: List[SkillRecommendation] = []
    for skill in ordered:
        reasons = tuple(project_reasons.get(skill, []) + prompt_reasons.get(skill, []))
        recs.append(SkillRecommendation(name=skill, reasons=reasons))

    meta = {
        "project_dir": str(project_dir),
        "detected": detected,
        "selected_skills": ordered,
    }
    return recs, meta


def _render_text(recs: Sequence[SkillRecommendation], repo_dir: Path) -> str:
    if not recs:
        return "No skill recommendations (no matching signals).\n"

    lines: List[str] = []
    lines.append("Skills (in order): " + ", ".join(r.name for r in recs))
    lines.append("")
    lines.append("Why:")
    for rec in recs:
        if not rec.reasons:
            lines.append(f"- {rec.name}: selected by default ordering")
            continue
        for reason in rec.reasons:
            lines.append(f"- {rec.name}: {reason}")

    lines.append("")
    lines.append("Paths:")
    for rec in recs:
        lines.append(f"- {rec.name}: {repo_dir / rec.name / 'SKILL.md'}")

    return "\n".join(lines).rstrip() + "\n"


def main(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(description="Recommend the-true-scotsman skills for a repo + prompt.")
    parser.add_argument("--project-dir", default=".", help="Project directory to scan (default: .)")
    parser.add_argument("--prompt", help="User prompt to analyze. If omitted, read from stdin.")
    parser.add_argument("--config", help="Path to skills-config.json (default: repo root).")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(list(argv))

    repo_dir = _repo_root_from_script()
    config_path = Path(args.config) if args.config else (repo_dir / "skills-config.json")
    config = _load_json(config_path)

    project_dir = Path(args.project_dir).resolve()
    prompt = args.prompt if args.prompt is not None else sys.stdin.read()
    prompt = prompt.strip()

    recs, meta = recommend_skills(project_dir, prompt, config)

    if args.format == "json":
        payload = {
            "recommendations": [{"name": r.name, "reasons": list(r.reasons)} for r in recs],
            "meta": meta,
        }
        sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        return 0

    sys.stdout.write(_render_text(recs, repo_dir))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
