$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) { throw "FFmpeg is required. Install it and add it to PATH." }
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "Created .env with DEMO_MODE=true." }
if (-not (Test-Path ".venv")) { py -3.11 -m venv .venv }
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
python -m app.db_init
python -m app.daily_run
Write-Host "Starting local review dashboard at http://127.0.0.1:8090"
uvicorn app.api:app --host 127.0.0.1 --port 8090
