"""Validation-only check for the local ComfyUI video engine.

This script deliberately does NOT queue a generation job. It only checks the
local ComfyUI health endpoint so CI/local verification cannot accidentally
consume compute.
"""

from comfyui import health


if __name__ == "__main__":
    result = health()
    if result["ok"]:
        print("COMFYUI_OK")
        raise SystemExit(0)
    print("COMFYUI_NOT_REACHABLE")
    raise SystemExit(1)
