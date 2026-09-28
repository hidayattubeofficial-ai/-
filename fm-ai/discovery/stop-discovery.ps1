$ErrorActionPreference = "Stop"

$DiscoveryDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PidFile = Join-Path $DiscoveryDir "discovery.pid"

if (-not (Test-Path $PidFile)) {
    Write-Host "FM Computer discovery is not running (no PID file)."
    exit 0
}

$pidValue = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1)
if (-not $pidValue) {
    Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
    Write-Host "FM Computer discovery is not running."
    exit 0
}

$process = Get-Process -Id ([int]$pidValue) -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $process.Id -Force
    Write-Host "FM Computer discovery stopped. PID: $($process.Id)"
} else {
    Write-Host "Discovery process was not found."
}

Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
