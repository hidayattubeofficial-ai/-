$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$DiscoveryDir = Join-Path $Root "discovery"

Write-Host "FM Computer LAN Discovery"
Write-Host "Existing API remains on 127.0.0.1:8080"
Write-Host "Installing/using zeroconf in the active local Python environment..."

python -m pip install -r (Join-Path $DiscoveryDir "requirements.txt")
python (Join-Path $DiscoveryDir "advertise.py")
