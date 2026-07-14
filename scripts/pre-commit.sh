#!/usr/bin/env bash
set -e

echo "==> Running uv format..."
uv format

echo "==> Running tests..."
uv run pytest

echo "==> Running uv build..."
uv build

echo "==> Pre-commit checks passed."
