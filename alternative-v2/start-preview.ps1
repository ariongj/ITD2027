$ErrorActionPreference = 'Stop'
$taskDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$taskNode = 'C:\Users\A\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
if (-not (Test-Path -LiteralPath $taskNode)) { $taskNode = (Get-Command node -ErrorAction Stop).Source }
if (Test-Path -LiteralPath "$taskDirectory\qa\preview.pid") {
  $taskPid = [int](Get-Content -LiteralPath "$taskDirectory\qa\preview.pid")
  $taskProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $taskPid" -ErrorAction SilentlyContinue
  if ($taskProcess -and $taskProcess.CommandLine -like "*$taskDirectory\preview.mjs*") {
    Write-Output 'Preview already running: http://127.0.0.1:8790/'
    exit 0
  }
}
$busy = Get-NetTCPConnection -State Listen -LocalPort 8790 -ErrorAction SilentlyContinue
if ($busy) { throw 'Port 8790 is occupied. Existing service was not changed.' }
$taskProcess=Start-Process -FilePath $taskNode -ArgumentList ('"'+$taskDirectory+'\preview.mjs"') -WorkingDirectory $taskDirectory -WindowStyle Hidden -RedirectStandardOutput "$taskDirectory\qa\preview.log" -RedirectStandardError "$taskDirectory\qa\preview-error.log" -PassThru
$taskProcess.Id | Set-Content -LiteralPath "$taskDirectory\qa\preview.pid"
Write-Output 'Preview started: http://127.0.0.1:8790/'

