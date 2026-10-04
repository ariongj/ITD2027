$ErrorActionPreference = 'Stop'
$taskDirectory=Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path -LiteralPath "$taskDirectory\qa\preview.pid")) { exit 0 }
$taskPid=[int](Get-Content -LiteralPath "$taskDirectory\qa\preview.pid")
$taskProcess=Get-CimInstance Win32_Process -Filter "ProcessId = $taskPid" -ErrorAction SilentlyContinue
if ($taskProcess -and $taskProcess.CommandLine -like "*$taskDirectory\preview.mjs*") { Stop-Process -Id $taskPid; Write-Output 'Alternative preview stopped.' }

