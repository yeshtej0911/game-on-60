#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || { echo "FFmpeg is required"; exit 1; }
[ -f .env ] || cp .env.example .env
[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
python -m app.db_init
python -m app.daily_run
exec uvicorn app.api:app --host 127.0.0.1 --port 8090
