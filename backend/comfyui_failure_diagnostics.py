from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DiagnosticResult:
    ok: bool
    code: str
    detail: str


def diagnose_comfyui_response(response: dict[str, Any]) -> DiagnosticResult:
    """Classify a local ComfyUI queue response without clearing the failure."""
    if not response:
        return DiagnosticResult(False, "empty_response", "ComfyUI returned no response")

    if response.get("error"):
        return DiagnosticResult(
            False,
            "queue_error",
            str(response["error"]),
        )

    prompt_id = response.get("prompt_id")
    if not prompt_id:
        return DiagnosticResult(
            False,
            "missing_prompt_id",
            "ComfyUI response did not include prompt_id",
        )

    return DiagnosticResult(
        True,
        "queued",
        f"ComfyUI accepted local job {prompt_id}",
    )


def diagnose_health_response(health: dict[str, Any] | None) -> DiagnosticResult:
    if not health:
        return DiagnosticResult(False, "health_unavailable", "ComfyUI health data unavailable")
    if health.get("error"):
        return DiagnosticResult(False, "health_error", str(health["error"]))
    return DiagnosticResult(True, "healthy", "ComfyUI health check returned data")
