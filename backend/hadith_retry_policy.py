from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Action = Literal["generate", "retry", "edit", "duplicate", "recreate"]


@dataclass(frozen=True)
class RetryState:
    failed: bool
    failure_cleared: bool = False


def retry_allowed(state: RetryState) -> bool:
    """Retry is allowed only after the previous failure has been cleared."""
    return state.failed and state.failure_cleared


def recreate_allowed() -> bool:
    """Recreate remains disabled by policy."""
    return False


def action_allowed(
    action: str,
    *,
    explicit_request: bool,
    retry_state: RetryState | None = None,
) -> bool:
    action = action.strip().lower()

    if action == "generate":
        return True

    if action == "retry":
        return retry_state is not None and retry_allowed(retry_state)

    if action == "recreate":
        return False

    if action in {"duplicate", "edit"}:
        return explicit_request

    raise ValueError(f"unsupported action: {action}")
