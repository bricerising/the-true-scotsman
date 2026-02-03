"""Git helpers for diff/excerpt context building."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


class GitError(RuntimeError):
    pass


def _run_git(repo_dir: Path, args: List[str]) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(repo_dir),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        stderr = getattr(exc, "stderr", "") or ""
        raise GitError(f"git {' '.join(args)} failed. {stderr}".strip()) from exc
    return proc.stdout


def is_git_repo(repo_dir: Path) -> bool:
    try:
        _run_git(repo_dir, ["rev-parse", "--is-inside-work-tree"])
    except GitError:
        return False
    return True


def head_sha(repo_dir: Path, ref: str = "HEAD") -> str:
    return _run_git(repo_dir, ["rev-parse", ref]).strip()


def diff_text(repo_dir: Path, *, base: Optional[str], head: str, diff_file: Optional[Path]) -> str:
    if diff_file:
        return diff_file.read_text(encoding="utf-8")
    if base:
        # PR-style: merge-base...head
        return _run_git(repo_dir, ["diff", "--patch", "--no-color", f"{base}...{head}"])
    # Default: all working tree + staged changes vs HEAD
    return _run_git(repo_dir, ["diff", "--patch", "--no-color", "HEAD"])


@dataclass(frozen=True)
class Hunk:
    new_start: int
    new_count: int


@dataclass(frozen=True)
class FileChange:
    path: str
    hunks: Tuple[Hunk, ...]


def _parse_hunk_header(line: str) -> Optional[Hunk]:
    # @@ -a,b +c,d @@
    if not line.startswith("@@ "):
        return None
    try:
        header = line.split("@@")[1].strip()
        # header is like: "-12,3 +45,9"
        parts = header.split(" ")
        new_part = next(p for p in parts if p.startswith("+"))
        new_range = new_part[1:]
        if "," in new_range:
            start_s, count_s = new_range.split(",", 1)
            return Hunk(new_start=int(start_s), new_count=int(count_s))
        return Hunk(new_start=int(new_range), new_count=1)
    except Exception:
        return None


def parse_unified_diff(diff: str) -> Tuple[FileChange, ...]:
    current_path: Optional[str] = None
    hunks: List[Hunk] = []
    files: List[FileChange] = []

    for raw in diff.splitlines():
        if raw.startswith("diff --git "):
            if current_path is not None:
                files.append(FileChange(path=current_path, hunks=tuple(hunks)))
            hunks = []
            current_path = None
            continue

        if raw.startswith("+++ "):
            # +++ b/path OR +++ /dev/null
            parts = raw.split(maxsplit=1)
            if len(parts) == 2 and parts[1].startswith("b/"):
                current_path = parts[1][2:]
            continue

        hunk = _parse_hunk_header(raw)
        if hunk:
            hunks.append(hunk)

    if current_path is not None:
        files.append(FileChange(path=current_path, hunks=tuple(hunks)))

    return tuple(files)


def _merge_intervals(intervals: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    sorted_intervals = sorted((start, end) for start, end in intervals if start <= end)
    merged: List[Tuple[int, int]] = []
    for start, end in sorted_intervals:
        if not merged:
            merged.append((start, end))
            continue
        prev_start, prev_end = merged[-1]
        if start <= prev_end + 1:
            merged[-1] = (prev_start, max(prev_end, end))
            continue
        merged.append((start, end))
    return merged


def build_line_excerpts(
    repo_dir: Path,
    changes: Tuple[FileChange, ...],
    *,
    context_lines: int,
    max_excerpt_lines_per_file: int,
) -> Dict[str, str]:
    excerpts: Dict[str, str] = {}
    for change in changes:
        file_path = repo_dir / change.path
        if not file_path.exists() or not file_path.is_file():
            continue
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        intervals: List[Tuple[int, int]] = []
        for hunk in change.hunks:
            start = max(1, hunk.new_start - context_lines)
            end = min(len(lines), hunk.new_start + max(hunk.new_count - 1, 0) + context_lines)
            intervals.append((start, end))
        merged = _merge_intervals(intervals)

        out_lines: List[str] = []
        total = 0
        for start, end in merged:
            if total >= max_excerpt_lines_per_file:
                break
            chunk = lines[start - 1 : end]
            remaining = max_excerpt_lines_per_file - total
            chunk = chunk[:remaining]
            out_lines.append(f"--- {change.path}:{start}-{start + len(chunk) - 1} ---")
            for i, text in enumerate(chunk, start=start):
                out_lines.append(f"{i:>6} | {text}")
            total += len(chunk)

        if out_lines:
            excerpts[change.path] = "\n".join(out_lines).strip() + "\n"

    return excerpts
