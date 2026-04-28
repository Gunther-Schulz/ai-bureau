#!/usr/bin/env bash
# dev-link.sh — link this repo's plugin/ folder into the Claude Code
# plugin cache as a symlink, for fast iteration during development.
# After running, edits to skills here are visible to Claude Code on
# `/reload-plugins` without needing to bump version or reinstall.
#
# Idempotent. Re-run after any `claude plugin uninstall` or after
# bumping plugin.json version.

set -euo pipefail

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_PLUGIN="$REPO_DIR/plugin"
MARKETPLACE_MANIFEST="$REPO_DIR/.claude-plugin/marketplace.json"
PLUGIN_MANIFEST="$SRC_PLUGIN/.claude-plugin/plugin.json"

if [[ ! -f "$PLUGIN_MANIFEST" ]]; then
  echo "Error: plugin manifest not found at $PLUGIN_MANIFEST" >&2
  exit 1
fi
if [[ ! -f "$MARKETPLACE_MANIFEST" ]]; then
  echo "Error: marketplace manifest not found at $MARKETPLACE_MANIFEST" >&2
  exit 1
fi

VERSION=$(jq -r .version "$PLUGIN_MANIFEST")
PLUGIN_NAME=$(jq -r .name "$PLUGIN_MANIFEST")
MARKETPLACE_NAME=$(jq -r .name "$MARKETPLACE_MANIFEST")

CACHE_DIR="$HOME/.claude/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION"

mkdir -p "$(dirname "$CACHE_DIR")"

# If already linked correctly, no-op.
if [[ -L "$CACHE_DIR" ]]; then
  CURRENT_TARGET=$(readlink -f "$CACHE_DIR")
  EXPECTED_TARGET=$(readlink -f "$SRC_PLUGIN")
  if [[ "$CURRENT_TARGET" == "$EXPECTED_TARGET" ]]; then
    echo "Already linked: $CACHE_DIR → $SRC_PLUGIN"
    exit 0
  fi
fi

# Replace any existing entry (copy or stale symlink) with a fresh symlink.
rm -rf "$CACHE_DIR"
ln -s "$SRC_PLUGIN" "$CACHE_DIR"
echo "Linked: $CACHE_DIR → $SRC_PLUGIN"
echo
echo "Next: in Claude Code, run /reload-plugins to pick up the change."
echo "Future edits to plugin/ are picked up by /reload-plugins alone — no"
echo "reinstall needed unless you change the version in plugin.json."
