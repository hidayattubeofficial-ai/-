from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hadith_generation_policy import Action, GenerationRequest, build_request
from hadith_output_registry import canonical_exists, ensure_generation_slot
from hadith_revision_registry import HadithRevision, create_revision


@dataclass(frozen=True)
class PreparedHadithGeneration:
    request: GenerationRequest
    output_path: Path
    revision: HadithRevision | None = None


def prepare_generation(
    root: str | Path,
    book: str,
    hadith_number: int,
    *,
    action: Action = "generate",
    explicit_request: bool = False,
    revision: int = 1,
    existing_revisions: list[int] | None = None,
) -> PreparedHadithGeneration:
    request = build_request(
        book,
        hadith_number,
        action=action,
        explicit_request=explicit_request,
        revision=revision,
    )

    if action == "generate":
        if canonical_exists(root, request.identity):
            raise FileExistsError(
                f"Hadith already exists: {request.identity.sequence_key}; "
                "use an explicit recreate, duplicate, or edit request."
            )
        output_path = ensure_generation_slot(
            root, request.identity, explicit_request=False
        )
        return PreparedHadithGeneration(request=request, output_path=output_path)

    if not explicit_request:
        raise PermissionError(
            f"{action} requires an explicit request: {request.identity.sequence_key}"
        )

    revisions = existing_revisions or []
    new_revision = create_revision(
        root,
        request.identity,
        revisions,
        explicit_request=True,
    )
    return PreparedHadithGeneration(
        request=request,
        output_path=new_revision_dir(root, new_revision),
        revision=new_revision,
    )


def new_revision_dir(root: str | Path, revision: HadithRevision) -> Path:
    return Path(root) / revision.identity.book / str(revision.identity.hadith_number) / f"v{revision.revision}"
