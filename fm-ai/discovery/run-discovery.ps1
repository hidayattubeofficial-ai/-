$ErrorActionPreference = "Stop"

$DiscoveryDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StatusScript = Join-Path $DiscoveryDir "discovery-status.ps1"
$Advertiser = Join-Path $DiscoveryDir "advertise.py"

Write-Host "=== FM AI Discovery Preflight ==="
& $StatusScript
Write-Host ""
Write-Host "Starting local DNS-SD advertisement..."
python $Advertiser
