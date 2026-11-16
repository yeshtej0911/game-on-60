param([string]$Time = "06:00")
$ErrorActionPreference = "Stop"
$project = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $project "scripts\run-daily.ps1"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$runner`""
$trigger = New-ScheduledTaskTrigger -Daily -At $Time
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)
Register-ScheduledTask -TaskName "GAME ON 60 Daily Content Run" -Action $action -Trigger $trigger -Settings $settings -Description "Generate GAME ON 60 draft videos; publishing remains manual." -Force | Out-Null
Write-Host "Scheduled GAME ON 60 daily run at $Time. The PC must be awake and connected."
Write-Host "Only enable this after setting DEMO_MODE=false and configuring API credentials."
