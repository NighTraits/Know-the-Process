from datetime import date
from dataclasses import dataclass
from uuid import UUID


@dataclass
class IContent:
    id: UUID
    title: str
    description: str
    location: str
    keywords: list[str]
    content: dict[str, list[str]]
    extra_content: list[str]
    source: str
    updated_at: date
    created_at: date
    approved_by: str
