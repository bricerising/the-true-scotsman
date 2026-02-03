from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from langchain_clis.shared.model import ModelConfig

class ReviewType(str, Enum):
    general = "general"
    security = "security"
    correctness = "correctness"
    performance = "performance"
    maintainability = "maintainability"
    testing = "testing"
    architecture = "architecture"
    resilience = "resilience"
    api_design = "api-design"
    accessibility = "accessibility"


@dataclass(frozen=True)
class ReviewConfig:
    review_type: ReviewType
    repo_dir: Path
    skills_dir: Path

    out_dir: Optional[Path]

    git_base: Optional[str]
    git_head: str
    diff_file: Optional[Path]

    context_lines: int
    max_diff_chars: int
    max_excerpt_lines_per_file: int

    rigor: int
    dry_run: bool
    model: ModelConfig
