#!/usr/bin/env bash
set -euo pipefail

# Basic plugin structure validation
[ -f ".claude-plugin/plugin.json" ] || { echo "Missing plugin.json" >&2; exit 2; }
exit 0
