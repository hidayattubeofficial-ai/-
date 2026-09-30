$ErrorActionPreference = "Continue"
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$data = Join-Path $root "data"
$health = Join-Path $data "health"
$logs = Join-Path $data "logs"
New-Item -ItemType Directory -Force -Path $health,$logs | Out-Null

$results = @()
try { Invoke-WebRequest -Uri "http://127.0.0.1:8080/health" -UseBasicParsing -TimeoutSec 5 | Out-Null; $results += "FM Computer: OK" }
catch { $results += "FM Computer: CHECK FAILED ($($_.Exception.Message))" }

try { Invoke-WebRequest -Uri "http://127.0.0.1:11434/api/tags" -UseBasicParsing -TimeoutSec 5 | Out-Null; $results += "Ollama: OK" }
catch { $results += "Ollama: CHECK FAILED ($($_.Exception.Message))" }

$results += "YouTube auto-publish: OFF"
$results += "FM Home approval: REQUIRED"
$results | Set-Content (Join-Path $health "latest.txt")
$results | Add-Content (Join-Path $logs "health.log")
$results | ForEach-Object { Write-Host $_ }
