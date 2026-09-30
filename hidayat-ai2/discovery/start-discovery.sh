#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$ROOT/discovery"
echo "FM Computer LAN Discovery"
echo "FM Computer API must listen on 0.0.0.0:8080"
python3 -m pip install -r "$DISCOVERY_DIR/requirements.txt"
python3 "$DISCOVERY_DIR/preflight.py"
exec python3 "$DISCOVERY_DIR/advertise.py"
