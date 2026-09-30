$ErrorActionPreference = "Stop"

$DiscoveryDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "FM Computer Discovery - local setup"
Write-Host "API endpoint remains http://127.0.0.1:8080"

python --version
python -m pip install -r (Join-Path $DiscoveryDir "requirements.txt")

Write-Host ""
Write-Host "Discovery dependency is ready."
Write-Host "Run start-discovery.ps1 to advertise _fmcomputer._tcp."
Write-Host "No GitHub Actions runtime is required."
Write-Host "YouTube publishing remains OFF."
