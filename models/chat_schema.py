from enum import StrEnum
from dataclasses import dataclass


class ROLE(StrEnum):
    USER = "User"
    ASSISTANT = "Assistant"


@dataclass
class IChat:
    role: ROLE
    message: str
