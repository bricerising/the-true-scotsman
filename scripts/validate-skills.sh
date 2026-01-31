#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

errors=0

fail() {
  echo "ERROR: $*" >&2
  errors=$((errors + 1))
}

info() {
  echo "INFO: $*" >&2
}

list_skill_dirs() {
  local dir
  while IFS= read -r dir; do
    if [[ -f "$dir/SKILL.md" ]]; then
      basename "$dir"
    fi
  done < <(find "$REPO_ROOT" -maxdepth 1 -mindepth 1 -type d -not -name '.*' -print | sort)
}

validate_frontmatter() {
  local skill="$1"
  local file="$REPO_ROOT/$skill/SKILL.md"

  if [[ ! -f "$file" ]]; then
    fail "Missing SKILL.md for $skill"
    return 0
  fi

  local first
  first="$(head -n 1 "$file" || true)"
  if [[ "$first" != "---" ]]; then
    fail "$file: missing YAML frontmatter delimiter (---) on first line"
    return 0
  fi

  local fm
  fm="$(awk 'NR==1{next} /^---$/{exit} {print}' "$file" || true)"

  if ! grep -qE '^name:' <<<"$fm"; then
    fail "$file: frontmatter missing 'name:'"
  fi

  if ! grep -qE '^description:' <<<"$fm"; then
    fail "$file: frontmatter missing 'description:'"
  fi

  local declared
  declared="$(sed -n 's/^name:[[:space:]]*//p' <<<"$fm" | head -n 1 | tr -d '\r' || true)"
  if [[ -n "$declared" && "$declared" != "$skill" ]]; then
    fail "$file: frontmatter name '$declared' does not match directory '$skill'"
  fi

  local lines
  lines="$(wc -l < "$file" | tr -d ' ')"
  if [[ "$lines" -gt 500 ]]; then
    fail "$file: too long (${lines} lines); keep SKILL.md under 500 lines (prefer references/ for detail)"
  fi
}

validate_readme_mentions() {
  local skill="$1"
  if ! grep -Fq "${skill}/" "$REPO_ROOT/README.md"; then
    fail "README.md: missing mention for skill directory '${skill}/'"
  fi
}

validate_config_covers_skills() {
  local config="$REPO_ROOT/skills-config.json"
  if [[ ! -f "$config" ]]; then
    fail "Missing skills-config.json"
    return 0
  fi

  python3 - "$config" "$REPO_ROOT" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1])
repo_root = Path(sys.argv[2])

data = json.loads(config_path.read_text(encoding="utf-8"))

errors = []

version = data.get("version")
if version != 1:
    errors.append(f"{config_path}: expected version 1, got {version!r}")

order = data.get("skillOrder", [])
if not isinstance(order, list) or not all(isinstance(x, str) for x in order):
    errors.append(f"{config_path}: skillOrder must be an array of strings")
    order = []

repo_skills = sorted(
    [
        d.name
        for d in repo_root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and (d / "SKILL.md").is_file()
    ]
)

missing = sorted(set(repo_skills) - set(order))
extra = sorted(set(order) - set(repo_skills))
if missing:
    errors.append(f"{config_path}: skillOrder missing: {missing}")
if extra:
    errors.append(f"{config_path}: skillOrder references unknown skills: {extra}")

referenced = []
for key in ("projectDetectors", "promptDetectors"):
    detectors = data.get(key, [])
    if not isinstance(detectors, list):
        continue
    for det in detectors:
        if not isinstance(det, dict):
            continue
        skills = det.get("skills", [])
        if isinstance(skills, list):
            referenced.extend([s for s in skills if isinstance(s, str)])

unknown_refs = sorted(set(referenced) - set(repo_skills))
if unknown_refs:
    errors.append(f"{config_path}: detectors reference unknown skills: {unknown_refs}")

if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)
PY
  if [[ $? -ne 0 ]]; then
    errors=$((errors + 1))
  fi
}

validate_scripts_smoke() {
  info "Smoke testing scripts"

  if ! python3 -m py_compile "$REPO_ROOT"/scripts/*.py >/dev/null 2>&1; then
    fail "Python scripts failed to compile (py_compile)"
    return 0
  fi

  local tmp
  tmp="$(mktemp -d 2>/dev/null || mktemp -d -t true-scotsman)"

  # recommend-skills: basic prompt trigger
  if ! python3 "$REPO_ROOT/scripts/recommend-skills.py" \
    --project-dir "$tmp" \
    --prompt "Please add tests and improve coverage" \
    --format json \
    >"$tmp/recs.json" 2>/dev/null; then
    fail "scripts/recommend-skills.py failed to run"
  else
    python3 - "$tmp/recs.json" <<'PY' || errors=$((errors + 1))
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
names = [r.get("name") for r in data.get("recommendations", [])]
if "consumer-test-coverage" not in names:
    raise SystemExit("expected consumer-test-coverage in recommendations")
PY
  fi

  # generate-project-rules: ensure files are created
  if ! python3 "$REPO_ROOT/scripts/generate-project-rules.py" \
    --project-dir "$tmp" \
    --repo-dir "$REPO_ROOT" \
    --tool all \
    --force \
    >/dev/null 2>&1; then
    fail "scripts/generate-project-rules.py failed to run"
  else
    local expected=(
      ".codex/AGENTS.md"
      ".claude/AGENTS.md"
      ".cursorrules"
      ".github/copilot-instructions.md"
    )
    local rel
    for rel in "${expected[@]}"; do
      if [[ ! -f "$tmp/$rel" ]]; then
        fail "generate-project-rules: missing output $rel"
      fi
    done
  fi

  rm -rf "$tmp"
}

main() {
  info "Repo: $REPO_ROOT"

  skills=()
  while IFS= read -r skill; do
    skills+=("$skill")
  done < <(list_skill_dirs)
  if [[ ${#skills[@]} -eq 0 ]]; then
    fail "No skill directories found at repo root"
  fi

  for skill in "${skills[@]}"; do
    validate_frontmatter "$skill"
    validate_readme_mentions "$skill"
  done

  validate_config_covers_skills
  validate_scripts_smoke

  if [[ "$errors" -gt 0 ]]; then
    echo "FAIL: $errors issue(s) found." >&2
    exit 1
  fi

  echo "OK: validation passed." >&2
}

main "$@"
