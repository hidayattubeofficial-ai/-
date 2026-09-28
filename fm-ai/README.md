# FM AI - Survival Computer AI

FM AI is the local survival-computer layer. It is not Ollama and it does not replace the existing FM Computer API.

Architecture:
- FM Computer API: http://127.0.0.1:8080 (preserved)
- Ollama: local model/runtime component at http://127.0.0.1:11434
- FM Home: approval/governance layer
- FM AI: local memory, logs, health and recovery orchestration
- YouTube auto-publish: OFF
- Human approval: REQUIRED

Run the health check from the FM Computer itself. Do not run the 127.0.0.1 check from a remote CI runner and assume it represents the user's computer.

PowerShell:
  powershell -ExecutionPolicy Bypass -File .\fm-ai\scripts\health-check.ps1

Linux/macOS:
  bash ./fm-ai/scripts/health-check.sh

CodeMagic is an isolated build/package helper here. It is not the FM AI runtime and must not replace the FM Computer API.

No YouTube publishing step is included.
