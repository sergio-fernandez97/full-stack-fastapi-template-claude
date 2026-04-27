#!/usr/bin/env bash
set -e

cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

if git diff --name-only 2>/dev/null | grep -q "^backend/.*\.py$"; then
    echo "[HOOK: backend-validation] Running ruff check on backend..."
    cd backend && uv run ruff check app tests \
        || echo "[HOOK: backend-validation] ruff check found issues."
fi
