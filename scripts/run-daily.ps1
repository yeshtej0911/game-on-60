$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)
if (-not (Test-Path ".venv\Scripts\python.exe")) { throw "Virtual environment missing. Run scripts/run-local.ps1 first." }
$log = Join-Path (Get-Location) "output\scheduled-run.log"
New-Item -ItemType Directory -Force -Path "output" | Out-Null
& .\.venv\Scripts\python.exe -m app.daily_run *>> $log
