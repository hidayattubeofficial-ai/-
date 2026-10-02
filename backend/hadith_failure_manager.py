from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

FailureStatus = Literal["failed", "clearing", "cleared", "blocked"]


@dataclass(frozen=True)
class FailureRecord:
    job_id: str
    status: FailureStatus
    reason: str


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    detail: str


def clear_failure_after_validation(
    failure: FailureRecord,
    validation: ValidationResult,
) -> FailureRecord:
    """A failure is cleared only after a successful post-failure validation."""
    if failure.status != "failed":
        raise ValueError("only a failed job can be cleared")
    if not validation.ok:
        return failure
    return FailureRecord(
        job_id=failure.job_id,
        status="cleared",
        reason=f"cleared after validation: {validation.detail}",
    )


def retry_is_unlocked(failure: FailureRecord) -> bool:
    return failure.status == "cleared"
