#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/data/health" "$ROOT/data/logs"

check() {
  local name="$1" url="$2"
  if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
    echo "$name: OK"
  else
    echo "$name: CHECK FAILED"
  fi
}

{
  check "FM Computer" "http://127.0.0.1:8080/health"
  check "Ollama" "http://127.0.0.1:11434/api/tags"
  echo "YouTube auto-publish: OFF"
  echo "FM Home approval: REQUIRED"
} | tee "$ROOT/data/health/latest.txt" >> "$ROOT/data/logs/health.log"
