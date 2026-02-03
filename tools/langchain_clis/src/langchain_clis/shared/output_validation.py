"""Lightweight output format validation for non-review CLIs."""

from __future__ import annotations

import re


class ValidationError(RuntimeError):
    pass


def validate_feature_ideation_report(text: str, *, min_ideas: int) -> None:
    _require(text, "# Feature Ideation Report")
    _require(text, "## Ideas (prioritized)")
    _require(text, "## Next steps")
    _require(text, "## Open questions")

    ideas = len(re.findall(r"(?m)^\\d+\\.\\s+\\S", text))
    if ideas < min_ideas:
        raise ValidationError(f"Expected at least {min_ideas} ideas (found {ideas}).")


def validate_progress_update_markdown(text: str) -> None:
    _require(text, "# Progress Update")
    _require_any(text, ["## Done", "## Completed"])
    _require(text, "## Next")
    _require_any(text, ["## Risks / blockers", "## Risks", "## Blockers"])
    _require_any(text, ["## Verification", "## Validation"])


def validate_progress_update_slack(text: str) -> None:
    required = ["Done:", "Next:", "Risks:", "Verification:"]
    missing = [r for r in required if r not in text]
    if missing:
        raise ValidationError(f"Missing required sections: {missing}")


_ALIGNMENT_RE = re.compile(r"(?m)^Alignment:\\s*(PASS|PARTIAL|FAIL)\\s*$")
_MISALIGNMENT_ID_RE = re.compile(r"(?m)^###\\s+(SA-\\d{2}):\\s+\\S")


def validate_spec_alignment_report(text: str) -> None:
    _require(text, "# Spec Alignment Report")
    _require(text, "## Summary")
    _require(text, "## Misalignments")
    _require(text, "## Spec updates needed")
    _require(text, "## Questions")

    m = _ALIGNMENT_RE.search(text)
    if not m:
        raise ValidationError("Missing Alignment line (expected: 'Alignment: PASS|PARTIAL|FAIL').")
    alignment = m.group(1)
    ids = _MISALIGNMENT_ID_RE.findall(text)
    if alignment != "PASS" and not ids:
        raise ValidationError(f"Alignment={alignment} requires at least one SA-XX misalignment item.")


def _require(text: str, needle: str) -> None:
    if needle not in text:
        raise ValidationError(f"Missing required section: {needle}")


def _require_any(text: str, needles: list[str]) -> None:
    if any(n in text for n in needles):
        return
    raise ValidationError(f"Missing required section (one of): {needles}")
