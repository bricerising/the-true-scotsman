#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

MODE="global" # global | local
PROJECT_DIR="$(pwd)"
METHOD="symlink" # symlink | copy
FORCE="false"

INSTALL_CODEX="true"
INSTALL_CLAUDE="false"

CODEX_DEST=""
CLAUDE_DEST=""
SKILLS_CSV=""

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [options]

Installs this repo's skill folders into Codex/Claude skills directories.

Options:
  --global                Install to user-level skills directories (default)
  --local                 Install to <project>/.codex/skills and/or <project>/.claude/skills
  --project-dir <path>    Project directory for --local (default: cwd)

  --codex                 Enable Codex installation (default)
  --no-codex              Disable Codex installation
  --claude                Enable Claude installation
  --no-claude             Disable Claude installation
  --all                   Enable both Codex + Claude

  --dest <path>           Override Codex destination directory
  --claude-dest <path>    Override Claude destination directory

  --method symlink|copy   Install method (default: symlink)
  --skills a,b,c          Install only these skills (default: all)
  --force                 Replace existing destinations if needed

Examples:
  scripts/install.sh --all
  scripts/install.sh --local --project-dir /path/to/project --claude
  scripts/install.sh --skills typescript-style-guide,consumer-test-coverage
EOF
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

warn() {
  echo "WARN: $*" >&2
}

python_realpath_equal() {
  local a="$1"
  local b="$2"
  python3 - "$a" "$b" <<'PY'
import os
import sys

a = os.path.realpath(sys.argv[1])
b = os.path.realpath(sys.argv[2])
sys.exit(0 if a == b else 1)
PY
}

list_repo_skills() {
  local found=()
  local dir
  while IFS= read -r dir; do
    local name
    name="$(basename "$dir")"
    if [[ -f "$dir/SKILL.md" ]]; then
      found+=("$name")
    fi
  done < <(find "$REPO_ROOT" -maxdepth 1 -mindepth 1 -type d -not -name '.*' -print | sort)

  if [[ ${#found[@]} -eq 0 ]]; then
    die "No skill directories found under $REPO_ROOT"
  fi

  printf '%s\n' "${found[@]}"
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --global)
        MODE="global"
        shift
        ;;
      --local)
        MODE="local"
        shift
        ;;
      --project-dir)
        PROJECT_DIR="${2:-}"
        shift 2
        ;;
      --codex)
        INSTALL_CODEX="true"
        shift
        ;;
      --no-codex)
        INSTALL_CODEX="false"
        shift
        ;;
      --claude)
        INSTALL_CLAUDE="true"
        shift
        ;;
      --no-claude)
        INSTALL_CLAUDE="false"
        shift
        ;;
      --all)
        INSTALL_CODEX="true"
        INSTALL_CLAUDE="true"
        shift
        ;;
      --method)
        METHOD="${2:-}"
        shift 2
        ;;
      --dest)
        CODEX_DEST="${2:-}"
        shift 2
        ;;
      --claude-dest)
        CLAUDE_DEST="${2:-}"
        shift 2
        ;;
      --skills)
        SKILLS_CSV="${2:-}"
        shift 2
        ;;
      --force)
        FORCE="true"
        shift
        ;;
      -h | --help)
        usage
        exit 0
        ;;
      *)
        die "Unknown argument: $1"
        ;;
    esac
  done
}

resolve_destinations() {
  if [[ "$INSTALL_CODEX" == "false" && "$INSTALL_CLAUDE" == "false" ]]; then
    die "Nothing to install: both Codex and Claude installation are disabled."
  fi

  if [[ "$MODE" == "local" ]]; then
    [[ -z "$CODEX_DEST" ]] && CODEX_DEST="${PROJECT_DIR}/.codex/skills"
    [[ -z "$CLAUDE_DEST" ]] && CLAUDE_DEST="${PROJECT_DIR}/.claude/skills"
    return 0
  fi

  local codex_home="${CODEX_HOME:-$HOME/.codex}"
  [[ -z "$CODEX_DEST" ]] && CODEX_DEST="${codex_home}/skills"
  [[ -z "$CLAUDE_DEST" ]] && CLAUDE_DEST="$HOME/.claude/skills"
}

install_skill() {
  local skill="$1"
  local src="${REPO_ROOT}/${skill}"
  local dest_dir="$2"
  local dest="${dest_dir}/${skill}"

  if [[ ! -d "$src" ]]; then
    die "Missing skill directory: $src"
  fi
  if [[ ! -f "$src/SKILL.md" ]]; then
    die "Missing SKILL.md for: $src"
  fi

  mkdir -p "$dest_dir"

  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ "$METHOD" == "symlink" && -L "$dest" ]]; then
      if python_realpath_equal "$dest" "$src"; then
        echo "OK  : $skill already installed at $dest"
        return 0
      fi
    fi

    if [[ "$FORCE" == "true" ]]; then
      rm -rf "$dest"
    else
      warn "Skipping $skill: destination exists ($dest). Use --force to replace."
      return 0
    fi
  fi

  case "$METHOD" in
    symlink)
      ln -s "$src" "$dest"
      echo "ADD : $skill -> $dest (symlink)"
      ;;
    copy)
      cp -R "$src" "$dest"
      echo "ADD : $skill -> $dest (copy)"
      ;;
    *)
      die "Invalid --method: $METHOD (expected symlink|copy)"
      ;;
  esac
}

main() {
  parse_args "$@"
  resolve_destinations

  local skills=()
  if [[ -n "$SKILLS_CSV" ]]; then
    IFS=',' read -r -a skills <<<"$SKILLS_CSV"
  else
    while IFS= read -r skill; do
      skills+=("$skill")
    done < <(list_repo_skills)
  fi

  echo "Repo:   $REPO_ROOT"
  echo "Mode:   $MODE"
  echo "Method: $METHOD"
  echo "Skills: ${#skills[@]}"

  if [[ "$INSTALL_CODEX" == "true" ]]; then
    echo "Codex dest:  $CODEX_DEST"
    for skill in "${skills[@]}"; do
      install_skill "$skill" "$CODEX_DEST"
    done
  fi

  if [[ "$INSTALL_CLAUDE" == "true" ]]; then
    echo "Claude dest: $CLAUDE_DEST"
    for skill in "${skills[@]}"; do
      install_skill "$skill" "$CLAUDE_DEST"
    done
  fi
}

main "$@"
