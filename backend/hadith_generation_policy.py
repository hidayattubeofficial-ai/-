from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from hadith_identity import HadithIdentity, action_allowed, make_identity

Action = Literal["generate", "recreate", "duplicate", "edit"]


@dataclass(frozen=True)
class GenerationRequest:
    identity: HadithIdentity
    action: Action
    explicit_request: bool = False
    revision: int = 1

    def validate(self) -> None:
        if not action_allowed(self.action, explicit_request=self.explicit_request):
            raise PermissionError(
                f"{self.action} is on-demand only for {self.identity.sequence_key}"
            )
        if self.revision < 1:
            raise ValueError("revision must be >= 1")
        if self.action == "generate" and self.revision != 1:
            raise ValueError("new generation must start at revision 1")


def build_request(
    book: str,
    hadith_number: int,
    *,
    action: Action = "generate",
    explicit_request: bool = False,
    revision: int = 1,
) -> GenerationRequest:
    request = GenerationRequest(
        identity=make_identity(book, hadith_number),
        action=action,
        explicit_request=explicit_request,
        revision=revision,
    )
    request.validate()
    return request
