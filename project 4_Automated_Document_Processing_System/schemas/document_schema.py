from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    type: Literal["person", "organization", "location", "date", "other"]


class DocumentResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_title: str
    document_type: Literal[
        "invoice", "resume", "report", "article", "academic", "other"
    ]
    summary: str
    key_information: list[str] = Field(min_length=1, max_length=8)
    entities: list[Entity]
    dates: list[str]
    confidence: float = Field(ge=0, le=1)
