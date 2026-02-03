"""Validation helpers for review-protocol artifacts."""

from __future__ import annotations

import re
from typing import List, Set


class ValidationError(RuntimeError):
    pass


_FINDING_ID_RE = re.compile(r"^###\s+([A-Z0-9]+-\d{2})\\b", re.MULTILINE)


def _extract_ids(text: str) -> List[str]:
    return _FINDING_ID_RE.findall(text)


def validate_critique(text: str, *, max_findings: int) -> None:
    ids = _extract_ids(text)
    if not ids:
        raise ValidationError("No findings found (expected '### <ID>: ...').")
    if len(ids) > max_findings:
        raise ValidationError(f"Too many findings: {len(ids)} (max {max_findings}).")
    if len(set(ids)) != len(ids):
        raise ValidationError("Duplicate finding IDs.")

    required_fields = ["- Location:", "- Evidence:", "- Fix:"]
    for finding_id in ids:
        block = _block_for_id(text, finding_id)
        for field in required_fields:
            if field not in block:
                raise ValidationError(f"{finding_id} missing required field: {field}")


def validate_defense(defense_text: str, critique_text: str) -> None:
    expected = _extract_ids(critique_text)
    if not expected:
        raise ValidationError("Cannot validate defense without critique IDs.")
    found = _extract_ids(defense_text)
    if set(found) != set(expected):
        raise ValidationError(f"Defense IDs mismatch. Expected {expected}, got {found}.")
    _validate_status_headers(defense_text, allowed={"ACCEPT", "DISPUTE", "CONTEXT"})


def validate_rebuttal(rebuttal_text: str, critique_text: str) -> None:
    expected = _extract_ids(critique_text)
    found = _extract_ids(rebuttal_text)
    if set(found) != set(expected):
        raise ValidationError(f"Rebuttal IDs mismatch. Expected {expected}, got {found}.")
    _validate_status_headers(rebuttal_text, allowed={"CONCEDE", "MAINTAIN", "ESCALATE"})


def validate_verdict(verdict_text: str, critique_text: str) -> None:
    expected = set(_extract_ids(critique_text))
    if not expected:
        raise ValidationError("Cannot validate verdict without critique IDs.")

    if "## CONFIRMED" not in verdict_text or "## DISMISSED" not in verdict_text or "## CONTESTED" not in verdict_text:
        raise ValidationError("Verdict missing required sections: CONFIRMED/DISMISSED/CONTESTED.")

    mentioned = set(_extract_ids(verdict_text))
    if not mentioned:
        raise ValidationError("Verdict contains no finding IDs.")
    # Verdict may omit some items (e.g., if defender+attacker concede), but prefer full coverage.
    missing = expected - mentioned
    if missing:
        raise ValidationError(f"Verdict missing finding IDs: {sorted(missing)}")


def _validate_status_headers(text: str, *, allowed: Set[str]) -> None:
    # Expected: "### <ID> — <STATUS>"
    bad: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("### "):
            continue
        if "—" not in line:
            continue
        status = line.split("—", 1)[1].strip().split()[0]
        if status not in allowed:
            bad.append(status)
    if bad:
        raise ValidationError(f"Unexpected status values: {sorted(set(bad))}")


def _block_for_id(text: str, finding_id: str) -> str:
    parts = re.split(r"^###\s+", text, flags=re.MULTILINE)
    for part in parts:
        if part.startswith(f"{finding_id}"):
            return part
    return ""
