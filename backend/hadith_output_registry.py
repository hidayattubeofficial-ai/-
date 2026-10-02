from __future__ import annotations

from pathlib import Path

from hadith_identity import HadithIdentity


def canonical_output_dir(root: str | Path, identity: HadithIdentity) -> Path:
    """Return the canonical local review directory for one Hadith identity."""
    return Path(root) / identity.book / str(identity.hadith_number)


def canonical_exists(root: str | Path, identity: HadithIdentity) -> bool:
    return canonical_output_dir(root, identity).exists()


def ensure_generation_slot(
    root: str | Path,
    identity: HadithIdentity,
    *,
    explicit_request: bool,
) -> Path:
    """Block silent duplicates; explicit recreate/duplicate may reuse the identity."""
    target = canonical_output_dir(root, identity)
    if target.exists() and not explicit_request:
        raise FileExistsError(
            f"canonical Hadith output already exists: {identity.sequence_key}"
        )
    return target
