#!/usr/bin/env bash
set -euo pipefail

DISCOVERY_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DISCOVERY_DIR/discovery.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "FM Computer discovery is not running (no PID file)."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "FM Computer discovery stopped. PID: $PID"
else
  echo "Discovery process was not found."
fi

rm -f "$PID_FILE"
