from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from langchain_clis.shared.model import ModelConfig
from langchain_clis.shared.skills import resolve_skills_dir
from langchain_clis.spec_alignment.runner import SpecAlignmentConfig, run_spec_alignment

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


def _cwd_path() -> Path:
    return Path.cwd()


@app.command()
def run(
    repo: Annotated[
        Path,
        typer.Option("--repo", exists=True, file_okay=False, dir_okay=True, help="Target repo directory (default: cwd)."),
    ] = _cwd_path(),
    spec_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--spec-dir",
            exists=True,
            file_okay=False,
            dir_okay=True,
            help="Spec folder to compare against (default: <repo>/specs if present).",
        ),
    ] = None,
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
        typer.Option("--out-dir", file_okay=False, dir_okay=True, help="Output directory (default: .codex/spec-alignment/<HEAD_SHA>/)."),
    ] = None,
    git_base: Annotated[
        Optional[str],
        typer.Option("--git-base", help="Git base ref (PR-style diff uses merge-base: <base>...<head>)."),
    ] = None,
    git_head: Annotated[str, typer.Option("--git-head", help="Git head ref (default: HEAD).")] = "HEAD",
    diff_file: Annotated[
        Optional[Path],
        typer.Option("--diff-file", exists=True, file_okay=True, dir_okay=False, help="Unified diff file to check."),
    ] = None,
    context_lines: Annotated[int, typer.Option("--context-lines", min=0, max=200)] = 12,
    max_diff_chars: Annotated[int, typer.Option("--max-diff-chars", min=5_000)] = 60_000,
    max_excerpt_lines: Annotated[int, typer.Option("--max-excerpt-lines", min=50)] = 200,
    max_spec_chars: Annotated[int, typer.Option("--max-spec-chars", min=2_000, max=400_000)] = 80_000,
    max_spec_files: Annotated[int, typer.Option("--max-spec-files", min=1, max=300)] = 60,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Write context+prompt but do not call the model.")] = False,
    model: Annotated[str, typer.Option("--model", help="Model name (default: $ESB_SPEC_ALIGN_MODEL or gpt-4.1).")] = os.environ.get(
        "ESB_SPEC_ALIGN_MODEL", "gpt-4.1"
    ),
    temperature: Annotated[float, typer.Option("--temperature", min=0.0, max=1.5)] = 0.0,
) -> None:
    resolved_skills_dir = resolve_skills_dir(skills_dir)
    model_cfg = ModelConfig(provider="openai", model=model, temperature=temperature)
    cfg = SpecAlignmentConfig(
        repo_dir=repo.resolve(),
        skills_dir=resolved_skills_dir,
        out_dir=out_dir.resolve() if out_dir else None,
        spec_dir=spec_dir.resolve() if spec_dir else None,
        git_base=git_base,
        git_head=git_head,
        diff_file=diff_file.resolve() if diff_file else None,
        context_lines=context_lines,
        max_diff_chars=max_diff_chars,
        max_excerpt_lines_per_file=max_excerpt_lines,
        max_spec_chars=max_spec_chars,
        max_spec_files=max_spec_files,
        dry_run=dry_run,
        model=model_cfg,
    )

    result = run_spec_alignment(cfg)
    console.print(f"[bold]Artifacts:[/bold] {result.out_dir}")
    console.print(f"- `0-context.txt`: {result.context_path}")
    console.print(f"- `0-prompt.txt`: {result.prompt_path}")
    console.print(f"- `1-alignment.md`: {result.report_path}")


def main() -> None:
    app()
