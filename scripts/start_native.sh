#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
test -x .venv/bin/python || { echo 'Create .venv and install requirements.lock first (see README.md).'; exit 1; }
if [[ ! -f .env ]]; then cp .env.example .env; fi
exec .venv/bin/python scripts/serve_native.py
