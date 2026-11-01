from datetime import date
from dataclasses import dataclass


@dataclass
class IContent:
    id: str
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
