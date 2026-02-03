"""Small, bounded helpers for reading repo text safely."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence


@dataclass(frozen=True)
class BundledFile:
    path: Path
    rel: str
    text: str


def read_repo_readme(repo_dir: Path, *, max_chars: int) -> str:
    candidates = [repo_dir / "README.md", repo_dir / "README.rst", repo_dir / "README.txt"]
    for path in candidates:
        if not path.exists() or not path.is_file():
            continue
        return _read_text(path, max_chars=max_chars)
    return ""


def list_repo_top_level(repo_dir: Path, *, max_entries: int = 200) -> str:
    entries: list[str] = []
    for p in sorted(repo_dir.iterdir(), key=lambda x: x.name.lower()):
        if p.name in {".git", ".codex", ".venv", "venv", "__pycache__"}:
            continue
        suffix = "/" if p.is_dir() else ""
        entries.append(p.name + suffix)
        if len(entries) >= max_entries:
            entries.append("... (truncated)")
            break
    return "\n".join(entries).strip() + ("\n" if entries else "")


def bundle_directory(
    dir_path: Path,
    *,
    include_exts: Sequence[str],
    max_files: int,
    max_chars: int,
    exclude_dirs: Optional[Iterable[str]] = None,
) -> str:
    include = {e.lower() for e in include_exts}
    excluded = {".git", ".codex", ".venv", "venv", "__pycache__", "node_modules", "dist", ".next"}
    if exclude_dirs:
        excluded |= {d for d in exclude_dirs}

    if not dir_path.exists() or not dir_path.is_dir():
        return ""

    files: list[Path] = []
    for p in sorted(dir_path.rglob("*"), key=lambda x: str(x).lower()):
        if p.is_dir():
            continue
        if any(part in excluded for part in p.parts):
            continue
        if p.suffix.lower() not in include:
            continue
        files.append(p)
        if len(files) >= max_files:
            break

    bundled: list[BundledFile] = []
    for p in files:
        rel = str(p.relative_to(dir_path))
        text = _read_text(p, max_chars=max_chars)
        if not text.strip():
            continue
        bundled.append(BundledFile(path=p, rel=rel, text=text))

    return format_bundled_files(bundled, max_chars=max_chars)


def format_bundled_files(files: Sequence[BundledFile], *, max_chars: int) -> str:
    out: list[str] = []
    total = 0
    for f in files:
        header = f"--- {f.rel} ---\n"
        body = f.text.rstrip() + "\n"
        chunk = header + body + "\n"
        remaining = max_chars - total
        if remaining <= 0:
            out.append("[... truncated ...]\n")
            break
        if len(chunk) <= remaining:
            out.append(chunk)
            total += len(chunk)
            continue
        out.append(chunk[: max(0, remaining - 50)] + "\n[... truncated ...]\n")
        break
    return "".join(out).strip() + ("\n" if out else "")


def _read_text(path: Path, *, max_chars: int) -> str:
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""
    except OSError:
        return ""
    if len(raw) <= max_chars:
        return raw
    return raw[: max_chars - 200] + "\n\n[... truncated ...]\n"
