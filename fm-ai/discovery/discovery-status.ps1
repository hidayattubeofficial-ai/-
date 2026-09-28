$ErrorActionPreference = "SilentlyContinue"

$port = 8080
$listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue

if ($listener) {
    Write-Output "FM Computer API: LISTENING on local port $port"
} else {
    Write-Output "FM Computer API: NOT LISTENING on local port $port"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $zeroconf = python -c "import zeroconf; print(zeroconf.__version__)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Output "zeroconf: INSTALLED ($zeroconf)"
    } else {
        Write-Output "zeroconf: NOT INSTALLED"
    }
} else {
    Write-Output "Python: NOT FOUND"
}

Write-Output "Service type: _fmcomputer._tcp."
Write-Output "YouTube publishing: OFF"
Write-Output "FM Home approval: REQUIRED"
