from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from langchain_clis.code_review.config import ReviewConfig, ReviewType
from langchain_clis.code_review.runner import run_review
from langchain_clis.shared.model import ModelConfig
from langchain_clis.shared.skills import resolve_skills_dir

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


def _cwd_path() -> Path:
    return Path.cwd()


@app.command()
def run(
    review_type: Annotated[
        ReviewType,
        typer.Option(
            "--review-type",
            help="Review axis. 'general' runs a multi-specialist, merged critique by default.",
        ),
    ] = ReviewType.general,
    repo: Annotated[
        Path,
        typer.Option(
            "--repo",
            exists=True,
            file_okay=False,
            dir_okay=True,
            help="Target repo directory to review (default: current working directory).",
        ),
    ] = _cwd_path(),
    skills_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--skills-dir",
            exists=True,
            file_okay=False,
            dir_okay=True,
            help="Path to the enterprise-software-playbook skills root. Defaults to $ESB_SKILLS_DIR or auto-detect.",
        ),
    ] = None,
    out_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--out-dir",
            file_okay=False,
            dir_okay=True,
            help="Output directory. Defaults to .codex/review-protocol/<HEAD_SHA>/<REVIEW_TYPE>/ in the target repo.",
        ),
    ] = None,
    git_base: Annotated[
        Optional[str],
        typer.Option("--git-base", help="Git base ref (PR-style diff uses merge-base: <base>...<head>)."),
    ] = None,
    git_head: Annotated[
        str,
        typer.Option("--git-head", help="Git head ref for diff (default: HEAD)."),
    ] = "HEAD",
    diff_file: Annotated[
        Optional[Path],
        typer.Option(
            "--diff-file",
            exists=True,
            file_okay=True,
            dir_okay=False,
            help="Path to a unified diff/patch file to review instead of running git diff.",
        ),
    ] = None,
    context_lines: Annotated[
        int,
        typer.Option("--context-lines", min=0, max=200, help="Extra context lines around changed hunks for excerpts."),
    ] = 12,
    max_diff_chars: Annotated[
        int,
        typer.Option("--max-diff-chars", min=5_000, help="Truncate diff beyond this many characters (helps fit model context)."),
    ] = 60_000,
    max_excerpt_lines: Annotated[
        int,
        typer.Option("--max-excerpt-lines", min=50, help="Max excerpt lines per file (merged intervals)."),
    ] = 200,
    rigor: Annotated[
        int,
        typer.Option("--rigor", min=1, max=3, help="1=fewer specialists, 3=more specialists (default depends on review type)."),
    ] = 0,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Write context + prompts but do not call the model."),
    ] = False,
    model: Annotated[
        str,
        typer.Option("--model", help="Model name for all agents (default: $ESB_REVIEW_MODEL or gpt-4.1)."),
    ] = os.environ.get("ESB_REVIEW_MODEL", "gpt-4.1"),
    temperature: Annotated[
        float,
        typer.Option("--temperature", min=0.0, max=1.5, help="Sampling temperature."),
    ] = 0.0,
) -> None:
    resolved_skills_dir = resolve_skills_dir(skills_dir)
    model_cfg = ModelConfig(provider="openai", model=model, temperature=temperature)
    cfg = ReviewConfig(
        review_type=review_type,
        repo_dir=repo.resolve(),
        skills_dir=resolved_skills_dir,
        out_dir=out_dir.resolve() if out_dir else None,
        git_base=git_base,
        git_head=git_head,
        diff_file=diff_file.resolve() if diff_file else None,
        context_lines=context_lines,
        max_diff_chars=max_diff_chars,
        max_excerpt_lines_per_file=max_excerpt_lines,
        rigor=rigor,
        dry_run=dry_run,
        model=model_cfg,
    )

    result = run_review(cfg)
    console.print(f"[bold]Artifacts:[/bold] {result.out_dir}")
    console.print(f"- `1-critique.txt`: {result.critique_path}")
    console.print(f"- `2-defense.txt`: {result.defense_path}")
    console.print(f"- `3-rebuttal.txt`: {result.rebuttal_path}")
    console.print(f"- `4-verdict.txt`: {result.verdict_path}")
    console.print(f"- `5-report.md`: {result.report_path}")


def main() -> None:
    app()
