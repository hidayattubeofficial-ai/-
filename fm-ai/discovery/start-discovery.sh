#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$ROOT/discovery"

echo "FM Computer LAN Discovery"
echo "Existing API remains on 127.0.0.1:8080"

python3 -m pip install -r "$DISCOVERY_DIR/requirements.txt"
exec python3 "$DISCOVERY_DIR/advertise.py"
