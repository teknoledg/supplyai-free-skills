#!/usr/bin/env bash
# Install SupplyAI free skills into an Agent Skills host.
# Usage: ./install.sh --host <cursor|vscode|antigravity|devin|codex|claude> [--scope project|user] [--skill NAME]... [--dest DIR]
# project scope installs into the current directory; user scope into your home directory.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
host=""; scope="project"; dest=""; skills=()
while [ $# -gt 0 ]; do
  case "$1" in
    --host) host="$2"; shift 2;;
    --scope) scope="$2"; shift 2;;
    --skill) skills+=("$2"); shift 2;;
    --dest) dest="$2"; shift 2;;
    -h|--help) sed -n '2,4p' "$0"; exit 0;;
    *) echo "unknown argument: $1" >&2; exit 2;;
  esac
done
if [ -z "$dest" ]; then
  base="."; [ "$scope" = "user" ] && base="$HOME"
  case "$host:$scope" in
    cursor:*) dest="$base/.cursor/skills";;
    vscode:project) dest="$base/.github/skills";;
    vscode:user) dest="$base/.copilot/skills";;
    antigravity:project|devin:*|codex:*) dest="$base/.agents/skills";;
    antigravity:user) dest="$HOME/.gemini/config/skills";;
    claude:*) dest="$base/.claude/skills";;
    *) echo "unknown --host '$host' (cursor, vscode, antigravity, devin, codex, claude)" >&2; exit 2;;
  esac
fi
if [ ${#skills[@]} -eq 0 ]; then
  for d in "$here"/plugins/*/skills/*/; do skills+=("$(basename "$d")"); done
fi
mkdir -p "$dest"
for s in "${skills[@]}"; do
  src="$(ls -d "$here"/plugins/*/skills/"$s" 2>/dev/null | head -1)"
  if [ -z "$src" ]; then echo "no such skill: $s" >&2; exit 1; fi
  if [ -e "$dest/$s" ]; then echo "exists, not overwriting: $dest/$s" >&2; exit 1; fi
  cp -R "$src" "$dest/$s"
  echo "installed $s -> $dest/$s"
done
