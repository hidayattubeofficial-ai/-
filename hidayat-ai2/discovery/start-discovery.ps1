$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$DiscoveryDir = Join-Path $Root "discovery"
Write-Host "FM Computer LAN Discovery"
Write-Host "FM Computer API must listen on 0.0.0.0:8080"
Write-Host "Installing/using zeroconf in the active local Python environment..."
python -m pip install -r (Join-Path $DiscoveryDir "requirements.txt")
python (Join-Path $DiscoveryDir "preflight.py")
if ($LASTEXITCODE -ne 0) { throw "FM Computer LAN preflight failed." }
python (Join-Path $DiscoveryDir "advertise.py")
