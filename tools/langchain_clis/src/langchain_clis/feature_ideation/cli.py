from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from langchain_clis.feature_ideation.runner import FeatureIdeationConfig, run_feature_ideation
from langchain_clis.shared.model import ModelConfig
from langchain_clis.shared.skills import resolve_skills_dir

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


def _cwd_path() -> Path:
    return Path.cwd()


@app.command()
def run(
    focus: Annotated[str, typer.Option("--focus", help="Optional focus area (e.g., 'DX', 'billing', 'observability').")] = "",
    num_ideas: Annotated[int, typer.Option("--num-ideas", min=3, max=25, help="How many ideas to propose.")] = 8,
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
            help="Spec folder to read (default: <repo>/specs if present).",
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
        typer.Option("--out-dir", file_okay=False, dir_okay=True, help="Output directory (default: .codex/feature-ideation/<HEAD_SHA>/)."),
    ] = None,
    max_readme_chars: Annotated[int, typer.Option("--max-readme-chars", min=1_000, max=200_000)] = 25_000,
    max_spec_chars: Annotated[int, typer.Option("--max-spec-chars", min=2_000, max=400_000)] = 80_000,
    max_spec_files: Annotated[int, typer.Option("--max-spec-files", min=1, max=300)] = 60,
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Write context+prompt but do not call the model.")] = False,
    model: Annotated[str, typer.Option("--model", help="Model name (default: $ESB_IDEATE_MODEL or gpt-4.1).")] = os.environ.get(
        "ESB_IDEATE_MODEL", "gpt-4.1"
    ),
    temperature: Annotated[float, typer.Option("--temperature", min=0.0, max=1.5)] = 0.2,
) -> None:
    resolved_skills_dir = resolve_skills_dir(skills_dir)
    model_cfg = ModelConfig(provider="openai", model=model, temperature=temperature)
    cfg = FeatureIdeationConfig(
        repo_dir=repo.resolve(),
        skills_dir=resolved_skills_dir,
        out_dir=out_dir.resolve() if out_dir else None,
        spec_dir=spec_dir.resolve() if spec_dir else None,
        focus=focus,
        num_ideas=num_ideas,
        max_readme_chars=max_readme_chars,
        max_spec_chars=max_spec_chars,
        max_spec_files=max_spec_files,
        dry_run=dry_run,
        model=model_cfg,
    )

    result = run_feature_ideation(cfg)
    console.print(f"[bold]Artifacts:[/bold] {result.out_dir}")
    console.print(f"- `0-context.txt`: {result.context_path}")
    console.print(f"- `0-prompt.txt`: {result.prompt_path}")
    console.print(f"- `1-ideas.md`: {result.ideas_path}")


def main() -> None:
    app()
