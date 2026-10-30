#!/usr/bin/env bash
# Run on the Linux amd64 Python 3.12 target while internet is available.
set -euo pipefail
cd "$(dirname "$0")/.."
python3.12 -m pip download --only-binary=:all: --dest wheelhouse -r requirements.lock
python3.12 scripts/hash_wheels.py
