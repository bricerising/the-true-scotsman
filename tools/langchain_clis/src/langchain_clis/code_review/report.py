"""Parse protocol outputs and write shareable reports."""

from __future__ import annotations

import datetime as _dt
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class CritiqueFinding:
    finding_id: str
    title: str
    severity: str
    confidence: str
    location: str


@dataclass(frozen=True)
class VerdictItem:
    finding_id: str
    severity: Optional[str]
    fix_priority: Optional[str]
    status: str  # CONFIRMED/DISMISSED/CONTESTED


_CRITIQUE_HEADER_RE = re.compile(
    r"^###\s+(?P<id>[A-Z0-9]+-\d{2}):\s+(?P<title>.+)\s+\\((?P<sev>CRITICAL|HIGH|MEDIUM|LOW),\s+CONFIDENCE:\s+(?P<conf>HIGH|MEDIUM|LOW)\\)\\s*$"
)


def parse_critique(critique_text: str) -> Dict[str, CritiqueFinding]:
    findings: Dict[str, CritiqueFinding] = {}
    current_id: Optional[str] = None
    current: Dict[str, str] = {}

    for raw in critique_text.splitlines():
        header = _CRITIQUE_HEADER_RE.match(raw.strip())
        if header:
            if current_id and current:
                findings[current_id] = CritiqueFinding(
                    finding_id=current_id,
                    title=current.get("title", ""),
                    severity=current.get("severity", ""),
                    confidence=current.get("confidence", ""),
                    location=current.get("location", ""),
                )
            current_id = header.group("id")
            current = {
                "title": header.group("title").strip(),
                "severity": header.group("sev").strip(),
                "confidence": header.group("conf").strip(),
            }
            continue
        if current_id and raw.strip().startswith("- Location:"):
            current["location"] = raw.split(":", 1)[1].strip()

    if current_id and current:
        findings[current_id] = CritiqueFinding(
            finding_id=current_id,
            title=current.get("title", ""),
            severity=current.get("severity", ""),
            confidence=current.get("confidence", ""),
            location=current.get("location", ""),
        )
    return findings


def parse_verdict(verdict_text: str) -> List[VerdictItem]:
    items: List[VerdictItem] = []
    status: Optional[str] = None
    current_id: Optional[str] = None
    current_sev: Optional[str] = None
    current_priority: Optional[str] = None

    for raw in verdict_text.splitlines():
        line = raw.strip()
        if line == "## CONFIRMED":
            status = "CONFIRMED"
            continue
        if line == "## DISMISSED":
            status = "DISMISSED"
            continue
        if line == "## CONTESTED":
            status = "CONTESTED"
            continue

        if line.startswith("### ") and status:
            if current_id:
                items.append(
                    VerdictItem(
                        finding_id=current_id,
                        severity=current_sev,
                        fix_priority=current_priority,
                        status=status,
                    )
                )
            current_id = None
            current_sev = None
            current_priority = None

            header = line[4:].strip()
            # CONFIRMED: "<ID> (<SEVERITY>)"
            # DISMISSED/CONTESTED: "<ID>"
            if status == "CONFIRMED":
                m = re.match(r"^(?P<id>[A-Z0-9]+-\d{2})\s+\\((?P<sev>CRITICAL|HIGH|MEDIUM|LOW)\\)\\s*$", header)
                if m:
                    current_id = m.group("id")
                    current_sev = m.group("sev")
                else:
                    current_id = header.split()[0]
            else:
                current_id = header.split()[0]
            continue

        if current_id and status == "CONFIRMED" and line.startswith("- Fix priority:"):
            current_priority = line.split(":", 1)[1].strip()

    if current_id and status:
        items.append(VerdictItem(finding_id=current_id, severity=current_sev, fix_priority=current_priority, status=status))
    return items


def write_report(
    *,
    out_path: Path,
    repo_label: str,
    head_sha: str,
    review_type: str,
    scope: str,
    critique: str,
    verdict: str,
) -> None:
    critique_map = parse_critique(critique)
    verdict_items = parse_verdict(verdict)

    confirmed = [v for v in verdict_items if v.status == "CONFIRMED"]
    dismissed = [v for v in verdict_items if v.status == "DISMISSED"]
    contested = [v for v in verdict_items if v.status == "CONTESTED"]

    def _title(v: VerdictItem) -> str:
        return critique_map.get(v.finding_id, CritiqueFinding(v.finding_id, "", "", "", "")).title

    def _loc(v: VerdictItem) -> str:
        return critique_map.get(v.finding_id, CritiqueFinding(v.finding_id, "", "", "", "")).location

    # Top findings: prioritize P0/P1 if present, otherwise first confirmed.
    def _priority_rank(v: VerdictItem) -> Tuple[int, str]:
        p = (v.fix_priority or "").upper()
        if p == "P0":
            return (0, v.finding_id)
        if p == "P1":
            return (1, v.finding_id)
        if p == "P2":
            return (2, v.finding_id)
        return (3, v.finding_id)

    top_confirmed = sorted(confirmed, key=_priority_rank)[:5]
    date = _dt.date.today().isoformat()

    lines: List[str] = []
    lines.append(f"# Review Report: {review_type} — {repo_label} @ {head_sha}")
    lines.append("")
    lines.append(f"- Date: {date}")
    lines.append(f"- Scope: {scope}")
    lines.append("- Artifacts:")
    lines.append("  - 1-critique.txt")
    lines.append("  - 2-defense.txt")
    lines.append("  - 3-rebuttal.txt")
    lines.append("  - 4-verdict.txt")
    lines.append("")
    lines.append("## Executive summary")
    if top_confirmed:
        for v in top_confirmed:
            title = _title(v)
            loc = _loc(v)
            sev = v.severity or ""
            prio = v.fix_priority or ""
            lines.append(f"- {v.finding_id} ({sev}, {prio}): {title} — {loc}".rstrip())
    else:
        lines.append("- No CONFIRMED findings.")
    lines.append("")
    lines.append("## Counts")
    lines.append(f"- CONFIRMED: {len(confirmed)}")
    lines.append(f"- DISMISSED: {len(dismissed)}")
    lines.append(f"- CONTESTED: {len(contested)}")
    lines.append("")
    lines.append("## Top findings (P0/P1)")
    if top_confirmed:
        for v in top_confirmed:
            title = _title(v)
            loc = _loc(v)
            sev = v.severity or ""
            prio = v.fix_priority or ""
            lines.append(f"- {v.finding_id} ({sev}, {prio}): {title} — {loc}".rstrip())
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("## Full verdict")
    lines.append("### CONFIRMED")
    if confirmed:
        for v in sorted(confirmed, key=_priority_rank):
            title = _title(v)
            loc = _loc(v)
            sev = v.severity or ""
            prio = v.fix_priority or ""
            lines.append(f"- {v.finding_id} ({sev}, {prio}): {title} — {loc}".rstrip())
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("### DISMISSED")
    if dismissed:
        for v in dismissed:
            title = _title(v)
            lines.append(f"- {v.finding_id}: {title}".rstrip())
    else:
        lines.append("- None.")
    lines.append("")
    lines.append("### CONTESTED")
    if contested:
        for v in contested:
            title = _title(v)
            lines.append(f"- {v.finding_id}: {title}".rstrip())
    else:
        lines.append("- None.")
    lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
