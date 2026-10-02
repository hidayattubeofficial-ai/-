from __future__ import annotations

import re
from dataclasses import dataclass


_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


@dataclass(frozen=True)
class HadithIdentity:
    book: str
    hadith_number: int

    @property
    def sequence_key(self) -> str:
        return f"{self.book}/{self.hadith_number}"


def make_identity(book: str, hadith_number: int) -> HadithIdentity:
    book = book.strip().lower()
    if not _SLUG.fullmatch(book):
        raise ValueError("book must be a lowercase slug")
    if hadith_number < 1:
        raise ValueError("hadith_number must be >= 1")
    return HadithIdentity(book=book, hadith_number=hadith_number)


def action_allowed(action: str, *, explicit_request: bool) -> bool:
    """Only user-requested recreate/duplicate/edit actions are allowed."""
    action = action.strip().lower()
    if action == "generate":
        return True
    if action in {"recreate", "duplicate", "edit"}:
        return explicit_request
    raise ValueError(f"unsupported action: {action}")
