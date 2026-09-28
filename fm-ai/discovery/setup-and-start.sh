#!/usr/bin/env bash
set -euo pipefail
DISCOVERY_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$DISCOVERY_DIR/.venv"
PYTHON="${PYTHON:-python3}"
echo "=== FM AI Local Discovery Setup ==="
echo "FM Computer LAN API must be reachable at http://<LAN-IP>:8080"
echo "Required server bind: 0.0.0.0:8080"
echo "YouTube auto-publish: OFF"
echo "FM Home approval: REQUIRED"
if [ ! -x "$VENV_DIR/bin/python" ]; then
  echo "Creating isolated discovery environment..."
  "$PYTHON" -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/python" -m pip install -r "$DISCOVERY_DIR/requirements.txt"
if ! "$VENV_DIR/bin/python" "$DISCOVERY_DIR/preflight.py"; then
  echo "FM Computer LAN preflight failed. Start the FM Computer API on 0.0.0.0:8080 and allow TCP/8080." >&2
  exit 1
fi
PID_FILE="$DISCOVERY_DIR/discovery.pid"
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "Discovery already running. PID: $(cat "$PID_FILE")"
  exit 0
fi
echo "Starting local DNS-SD advertisement..."
nohup "$VENV_DIR/bin/python" "$DISCOVERY_DIR/advertise.py" > "$DISCOVERY_DIR/discovery.log" 2>&1 &
echo $! > "$PID_FILE"
echo "Discovery started. PID: $(cat "$PID_FILE")"
echo "Service: _fmcomputer._tcp."
echo "Stop with: ./stop-discovery.sh"
