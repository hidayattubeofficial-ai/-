#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DISCOVERY_DIR="$ROOT/discovery"

python3 "$DISCOVERY_DIR/advertise.py"
