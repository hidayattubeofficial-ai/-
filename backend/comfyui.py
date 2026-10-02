"""Local ComfyUI video connector for Hidayat AI.

This module never calls a paid cloud video API. It talks to a user-hosted
ComfyUI HTTP endpoint and submits a workflow JSON supplied by the local
deployment.

Environment:
- COMFYUI_BASE_URL (default: http://127.0.0.1:8188)
- COMFYUI_CLIENT_ID (optional)
"""

import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json


def _base_url():
    return os.environ.get("COMFYUI_BASE_URL", "http://127.0.0.1:8188").rstrip("/")


def health() -> dict:
    req = Request(f"{_base_url()}/system_stats", method="GET")
    try:
        with urlopen(req, timeout=5) as response:
            return {"ok": response.status == 200}
    except (HTTPError, URLError, TimeoutError):
        return {"ok": False}


def queue_prompt(workflow: dict) -> dict:
    if not isinstance(workflow, dict) or not workflow:
        raise ValueError("workflow must be a non-empty JSON object")

    payload = {"prompt": workflow}
    client_id = os.environ.get("COMFYUI_CLIENT_ID")
    if client_id:
        payload["client_id"] = client_id

    data = json.dumps(payload).encode("utf-8")
    req = Request(
        f"{_base_url()}/prompt",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError("local ComfyUI request failed") from exc
