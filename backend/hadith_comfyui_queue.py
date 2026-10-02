from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from hadith_generation_guard import PreparedHadithGeneration, prepare_generation
from comfyui import queue_prompt


@dataclass(frozen=True)
class GuardedQueueResult:
    prepared: PreparedHadithGeneration
    response: dict[str, Any]


def queue_hadith_video(
    root: str | Path,
    workflow: dict[str, Any],
    book: str,
    hadith_number: int,
    *,
    action: str = "generate",
    explicit_request: bool = False,
    revision: int = 1,
    existing_revisions: list[int] | None = None,
) -> GuardedQueueResult:
    """Queue only after Hadith identity/revision policy has approved the request."""
    prepared = prepare_generation(
        root,
        book,
        hadith_number,
        action=action,
        explicit_request=explicit_request,
        revision=revision,
        existing_revisions=existing_revisions,
    )

    # No publish step exists here. ComfyUI only receives the approved local job.
    response = queue_prompt(workflow)
    return GuardedQueueResult(prepared=prepared, response=response)
