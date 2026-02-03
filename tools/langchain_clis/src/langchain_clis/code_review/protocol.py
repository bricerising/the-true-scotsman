from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

from langchain_clis.code_review.config import ReviewType


class ProtocolError(RuntimeError):
    pass


@dataclass(frozen=True)
class TypeAddon:
    review_type: ReviewType
    prefix: str
    text: str


@dataclass(frozen=True)
class ProtocolTemplates:
    attacker_base: str
    addons: Dict[ReviewType, TypeAddon]
    defender: str
    rebuttal: str
    judge: str

    @staticmethod
    def load(skills_dir: Path) -> "ProtocolTemplates":
        path = skills_dir / "review-protocol" / "references" / "protocol.md"
        if not path.exists():
            raise ProtocolError(f"Missing protocol template: {path}")
        text = path.read_text(encoding="utf-8")

        attacker_base = _extract_blockquote_after(text, needle="**Base prompt (always include):**")
        addons = _extract_type_addons(text)
        defender = _extract_sentence_after(text, needle="### Defender (defense)")
        rebuttal = _extract_sentence_after(text, needle="### Attacker (rebuttal)")
        judge = _extract_sentence_after(text, needle="### Judge (verdict)")
        return ProtocolTemplates(
            attacker_base=attacker_base.strip(),
            addons=addons,
            defender=defender.strip(),
            rebuttal=rebuttal.strip(),
            judge=judge.strip(),
        )

    def attacker_prompt(self, review_type: ReviewType, *, max_findings: int) -> Tuple[str, str]:
        addon = self.addons.get(review_type)
        if not addon:
            raise ProtocolError(f"Unknown review type addon: {review_type}")
        base = self.attacker_base.replace("top 10–12", f"top {max_findings}")
        return base, addon.text

    def prefix_for(self, review_type: ReviewType) -> str:
        addon = self.addons.get(review_type)
        if not addon:
            raise ProtocolError(f"Unknown review type addon: {review_type}")
        return addon.prefix


def _extract_blockquote_after(text: str, *, needle: str) -> str:
    lines = text.splitlines()
    try:
        start_idx = next(i for i, line in enumerate(lines) if needle in line)
    except StopIteration as exc:
        raise ProtocolError(f"Failed to locate protocol section: {needle}") from exc

    collected = []
    in_quote = False
    for line in lines[start_idx + 1 :]:
        if line.strip().startswith(">"):
            in_quote = True
            collected.append(re.sub(r"^\s*>\s?", "", line))
            continue
        if in_quote:
            break
    if not collected:
        raise ProtocolError(f"Failed to parse blockquote after: {needle}")
    return "\n".join(collected).strip()


def _extract_sentence_after(text: str, *, needle: str) -> str:
    lines = text.splitlines()
    try:
        start_idx = next(i for i, line in enumerate(lines) if line.strip() == needle)
    except StopIteration as exc:
        raise ProtocolError(f"Failed to locate protocol section: {needle}") from exc

    for line in lines[start_idx + 1 :]:
        if not line.strip():
            continue
        # The doc uses a quoted sentence.
        return line.strip().strip("“”\"")
    raise ProtocolError(f"Failed to parse sentence after: {needle}")


_ADDON_HEADER_RE = re.compile(r"^- `(?P<name>[^`]+)` \(PREFIX=`(?P<prefix>[^`]+)`\):\s*$")


def _extract_type_addons(text: str) -> Dict[ReviewType, TypeAddon]:
    addons: Dict[ReviewType, TypeAddon] = {}
    lines = text.splitlines()

    # Parse lines like: - `general` (PREFIX=`CR`):
    i = 0
    while i < len(lines):
        match = _ADDON_HEADER_RE.match(lines[i])
        if not match:
            i += 1
            continue
        name = match.group("name").strip()
        prefix = match.group("prefix").strip()

        body: list[str] = []
        i += 1
        while i < len(lines):
            if _ADDON_HEADER_RE.match(lines[i]):
                break
            if lines[i].startswith("  - "):
                body.append(lines[i][4:])
            i += 1

        review_type = _to_review_type(name)
        addons[review_type] = TypeAddon(review_type=review_type, prefix=prefix, text="\n".join(body).strip())
    if not addons:
        raise ProtocolError("Failed to parse type add-ons from protocol.md")
    return addons


def _to_review_type(name: str) -> ReviewType:
    normalized = name.strip()
    for rt in ReviewType:
        if rt.value == normalized:
            return rt
    raise ProtocolError(f"Unknown review type in protocol.md: {name}")
