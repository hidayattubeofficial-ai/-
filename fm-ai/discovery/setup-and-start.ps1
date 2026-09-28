$ErrorActionPreference = "Stop"

$DiscoveryDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $DiscoveryDir ".venv"
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { throw "Python is required on FM Computer." }

Write-Host "=== FM AI Local Discovery Setup ==="
Write-Host "FM Computer LAN API must be reachable at http://<LAN-IP>:8080"
Write-Host "Required server bind: 0.0.0.0:8080"
Write-Host "YouTube auto-publish: OFF"
Write-Host "FM Home approval: REQUIRED"

if (-not (Test-Path (Join-Path $VenvDir "Scripts/python.exe"))) {
    Write-Host "Creating isolated discovery environment..."
    & $Python.Source -m venv $VenvDir
}
$VenvPython = Join-Path $VenvDir "Scripts/python.exe"
$Advertiser = Join-Path $DiscoveryDir "advertise.py"
$Preflight = Join-Path $DiscoveryDir "preflight.py"
$Requirements = Join-Path $DiscoveryDir "requirements.txt"
$PidFile = Join-Path $DiscoveryDir "discovery.pid"

Write-Host "Installing discovery dependency into isolated environment..."
& $VenvPython -m pip install -r $Requirements
Write-Host "Running LAN preflight..."
& $VenvPython $Preflight
if ($LASTEXITCODE -ne 0) { throw "FM Computer LAN preflight failed. Start the FM Computer API on 0.0.0.0:8080 and allow TCP/8080 on the local firewall." }

$existingPid = $null
if (Test-Path $PidFile) { $existingPid = (Get-Content $PidFile -ErrorAction SilentlyContinue | Select-Object -First 1) }
if ($existingPid -and (Get-Process -Id ([int]$existingPid) -ErrorAction SilentlyContinue)) {
    Write-Host "Discovery already running. PID: $existingPid"
    exit 0
}
Write-Host "Starting local DNS-SD advertisement..."
$process = Start-Process -FilePath $VenvPython -ArgumentList ('"{0}"' -f $Advertiser) -WorkingDirectory $DiscoveryDir -WindowStyle Hidden -PassThru
Set-Content -Path $PidFile -Value $process.Id -Encoding ascii
Write-Host "Discovery started. PID: $($process.Id)"
Write-Host "Service: _fmcomputer._tcp."
Write-Host "Stop with: .\stop-discovery.ps1"
