from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from langchain_clis.code_review.config import ReviewConfig, ReviewType
from langchain_clis.code_review.runner import run_review
from langchain_clis.feature_ideation.runner import FeatureIdeationConfig, run_feature_ideation
from langchain_clis.feature_progress.runner import FeatureProgressConfig, ProgressFormat, run_feature_progress
from langchain_clis.shared.model import ModelConfig
from langchain_clis.shared.skills import SkillsDirError, resolve_skills_dir
from langchain_clis.spec_alignment.runner import SpecAlignmentConfig, run_spec_alignment


def _find_skills_root(start: Path) -> Path:
    for root in [start, *start.parents]:
        if (root / "review-protocol" / "SKILL.md").exists():
            return root
    raise RuntimeError("Failed to locate skills repo root (expected review-protocol/SKILL.md).")


SKILLS_ROOT = _find_skills_root(Path(__file__).resolve())


def _write_file(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_min_diff(repo_dir: Path, *, rel_path: str) -> Path:
    # Minimal unified diff that our parser can understand (diff --git + +++ b/<path> + @@ ... @@).
    diff = "\n".join(
        [
            f"diff --git a/{rel_path} b/{rel_path}",
            f"--- a/{rel_path}",
            f"+++ b/{rel_path}",
            "@@ -1,1 +1,1 @@",
            "-OLD",
            "+NEW",
            "",
        ]
    )
    return _write_file(repo_dir / "change.diff", diff)


class CodeReviewConsumerTests(unittest.TestCase):
    def test_code_review_dry_run_writes_default_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            _write_file(repo_dir / "foo.txt", "line 1\nline 2\nline 3\n")
            diff_path = _write_min_diff(repo_dir, rel_path="foo.txt")

            cfg = ReviewConfig(
                review_type=ReviewType.general,
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                git_base=None,
                git_head="HEAD",
                diff_file=diff_path,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                rigor=0,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            result = run_review(cfg)
            expected_out_dir = repo_dir / ".codex" / "review-protocol" / "NO_GIT" / "general"
            self.assertEqual(result.out_dir, expected_out_dir)

            context_path = expected_out_dir / "0-context.txt"
            prompts_path = expected_out_dir / "0-prompts.txt"
            self.assertTrue(context_path.exists())
            self.assertTrue(prompts_path.exists())
            self.assertTrue((expected_out_dir / "1-critique.txt").exists())
            self.assertTrue((expected_out_dir / "2-defense.txt").exists())
            self.assertTrue((expected_out_dir / "3-rebuttal.txt").exists())
            self.assertTrue((expected_out_dir / "4-verdict.txt").exists())
            self.assertTrue((expected_out_dir / "5-report.md").exists())

            context = context_path.read_text(encoding="utf-8")
            self.assertIn("REVIEW CONTEXT", context)
            self.assertIn("=== Unified diff (primary evidence) ===", context)
            self.assertIn("=== Line-numbered excerpts (for anchoring) ===", context)
            self.assertIn("--- foo.txt:1-2 ---", context)

            prompts = prompts_path.read_text(encoding="utf-8")
            self.assertIn("PROMPTS (debugging aid)", prompts)
            self.assertIn("=== Attacker base ===", prompts)

    def test_code_review_empty_diff_still_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            diff_path = _write_file(repo_dir / "empty.diff", "")

            cfg = ReviewConfig(
                review_type=ReviewType.general,
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                git_base=None,
                git_head="HEAD",
                diff_file=diff_path,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                rigor=0,
                dry_run=True,  # ignored for empty-diff fast path
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            result = run_review(cfg)
            report_path = result.out_dir / "5-report.md"
            self.assertTrue(report_path.exists())

            report = report_path.read_text(encoding="utf-8")
            self.assertIn("# Review Report:", report)
            self.assertIn("No CONFIRMED findings.", report)


class FeatureIdeationConsumerTests(unittest.TestCase):
    def test_feature_ideate_dry_run_writes_context_prompt_and_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            _write_file(repo_dir / "README.md", "# Demo Repo\n\nHello.\n")
            _write_file(repo_dir / "specs" / "spec.md", "# Spec\n\n- Must be fast.\n")

            cfg = FeatureIdeationConfig(
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                spec_dir=None,  # auto-detect <repo>/specs
                focus="observability",
                num_ideas=3,
                max_readme_chars=10_000,
                max_spec_chars=10_000,
                max_spec_files=10,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.2),
            )

            result = run_feature_ideation(cfg)
            expected_out_dir = repo_dir / ".codex" / "feature-ideation" / "NO_GIT"
            self.assertEqual(result.out_dir, expected_out_dir)

            context = result.context_path.read_text(encoding="utf-8")
            self.assertIn("FEATURE IDEATION CONTEXT", context)
            self.assertIn("=== README (trimmed) ===", context)
            self.assertIn("=== Spec folder excerpts", context)
            self.assertIn("--- spec.md ---", context)
            self.assertIn("Must be fast.", context)

            prompt = result.prompt_path.read_text(encoding="utf-8")
            self.assertIn("# Feature Ideation Report", prompt)
            self.assertIn("## Ideas (prioritized)", prompt)

            self.assertEqual(result.ideas_path.read_text(encoding="utf-8"), "")


class FeatureProgressConsumerTests(unittest.TestCase):
    def test_feature_progress_dry_run_writes_context_prompt_and_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            _write_file(repo_dir / "foo.txt", "line 1\nline 2\nline 3\n")
            diff_path = _write_min_diff(repo_dir, rel_path="foo.txt")

            cfg = FeatureProgressConfig(
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                feature="billing export",
                audience="exec",
                format=ProgressFormat.slack,
                git_base=None,
                git_head="HEAD",
                diff_file=diff_path,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            result = run_feature_progress(cfg)
            expected_out_dir = repo_dir / ".codex" / "feature-progress" / "NO_GIT"
            self.assertEqual(result.out_dir, expected_out_dir)

            context = result.context_path.read_text(encoding="utf-8")
            self.assertIn("FEATURE PROGRESS CONTEXT", context)
            self.assertIn("Format: slack", context)
            self.assertIn("=== Unified diff (evidence) ===", context)

            prompt = result.prompt_path.read_text(encoding="utf-8")
            self.assertIn("Required output format:", prompt)
            self.assertIn("Done:", prompt)
            self.assertIn("Verification:", prompt)

            self.assertEqual(result.update_path.read_text(encoding="utf-8"), "")

    def test_feature_progress_requires_git_or_diff_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()

            cfg = FeatureProgressConfig(
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                feature="",
                audience="",
                format=ProgressFormat.markdown,
                git_base=None,
                git_head="HEAD",
                diff_file=None,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            with self.assertRaises(RuntimeError):
                run_feature_progress(cfg)


class SpecAlignmentConsumerTests(unittest.TestCase):
    def test_spec_align_dry_run_writes_context_prompt_and_placeholder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()
            _write_file(repo_dir / "specs" / "api.md", "# API\n\n- Contract: stable.\n")
            _write_file(repo_dir / "foo.txt", "line 1\nline 2\nline 3\n")
            diff_path = _write_min_diff(repo_dir, rel_path="foo.txt")

            cfg = SpecAlignmentConfig(
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                spec_dir=None,  # auto-detect <repo>/specs
                git_base=None,
                git_head="HEAD",
                diff_file=diff_path,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                max_spec_chars=10_000,
                max_spec_files=10,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            result = run_spec_alignment(cfg)
            expected_out_dir = repo_dir / ".codex" / "spec-alignment" / "NO_GIT"
            self.assertEqual(result.out_dir, expected_out_dir)

            context = result.context_path.read_text(encoding="utf-8")
            self.assertIn("SPEC ALIGNMENT CONTEXT", context)
            self.assertIn("=== Spec excerpts (source of truth) ===", context)
            self.assertIn("--- api.md ---", context)
            self.assertIn("Contract: stable.", context)

            prompt = result.prompt_path.read_text(encoding="utf-8")
            self.assertIn("# Spec Alignment Report", prompt)
            self.assertIn("Alignment: PASS|PARTIAL|FAIL", prompt)

            self.assertEqual(result.report_path.read_text(encoding="utf-8"), "")

    def test_spec_align_requires_git_or_diff_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_dir = Path(tmp) / "repo"
            repo_dir.mkdir()

            cfg = SpecAlignmentConfig(
                repo_dir=repo_dir,
                skills_dir=SKILLS_ROOT,
                out_dir=None,
                spec_dir=None,
                git_base=None,
                git_head="HEAD",
                diff_file=None,
                context_lines=1,
                max_diff_chars=50_000,
                max_excerpt_lines_per_file=200,
                max_spec_chars=10_000,
                max_spec_files=10,
                dry_run=True,
                model=ModelConfig(provider="openai", model="gpt-4.1", temperature=0.0),
            )

            with self.assertRaises(RuntimeError):
                run_spec_alignment(cfg)


class SkillsDirConsumerTests(unittest.TestCase):
    def test_resolve_skills_dir_defaults_to_home_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home_dir = Path(tmp) / "home"
            skills_root = home_dir / ".codex" / "skills"
            (skills_root / "review-protocol").mkdir(parents=True)
            (skills_root / "enterprise-web-app-workflow").mkdir(parents=True)
            _write_file(skills_root / "review-protocol" / "SKILL.md", "---\nname: review-protocol\n---\n")
            _write_file(skills_root / "enterprise-web-app-workflow" / "SKILL.md", "---\nname: enterprise-web-app-workflow\n---\n")

            old_home = os.environ.get("HOME")
            old_esb = os.environ.get("ESB_SKILLS_DIR")
            old_cwd = Path.cwd()
            try:
                os.environ["HOME"] = str(home_dir)
                os.environ.pop("ESB_SKILLS_DIR", None)
                os.chdir(tmp)
                resolved = resolve_skills_dir(None)
                self.assertEqual(resolved, skills_root.resolve())
            finally:
                if old_home is None:
                    os.environ.pop("HOME", None)
                else:
                    os.environ["HOME"] = old_home
                if old_esb is None:
                    os.environ.pop("ESB_SKILLS_DIR", None)
                else:
                    os.environ["ESB_SKILLS_DIR"] = old_esb
                os.chdir(old_cwd)

    def test_resolve_skills_dir_rejects_missing_required_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad-skills"
            bad.mkdir()

            with self.assertRaises(SkillsDirError):
                resolve_skills_dir(bad)
