from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from hadith_identity import HadithIdentity


@dataclass(frozen=True)
class HadithRevision:
    identity: HadithIdentity
    revision: int

    @property
    def key(self) -> str:
        return f"{self.identity.sequence_key}/v{self.revision}"


def revision_dir(root: str | Path, item: HadithRevision) -> Path:
    return Path(root) / item.identity.book / str(item.identity.hadith_number) / f"v{item.revision}"


def next_revision(existing: list[int]) -> int:
    valid = [n for n in existing if n >= 1]
    return max(valid, default=0) + 1


def create_revision(
    root: str | Path,
    identity: HadithIdentity,
    existing: list[int],
    *,
    explicit_request: bool,
) -> HadithRevision:
    if not explicit_request:
        raise PermissionError(
            f"revision is on-demand only for {identity.sequence_key}"
        )
    revision = HadithRevision(identity=identity, revision=next_revision(existing))
    revision_dir(root, revision).mkdir(parents=True, exist_ok=True)
    return revision
