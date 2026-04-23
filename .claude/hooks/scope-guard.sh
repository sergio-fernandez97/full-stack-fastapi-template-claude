#!/usr/bin/env bash
set -e

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

CHANGED=$(git diff --name-only 2>/dev/null \
    | grep -v "^backend/app/" \
    | grep -v "^backend/tests/" \
    | grep -v "^\.claude/" \
    | grep -v "^\.git" \
    | grep -v "^HOOKS\.md$" \
    || true)

if [ -n "$CHANGED" ]; then
    echo "[HOOK: scope-guard] WARNING: Changes detected outside allowed scope:"
    echo "$CHANGED"
    echo "Allowed: backend/app/**, backend/tests/**"
fi
