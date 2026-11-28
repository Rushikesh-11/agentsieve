"""Domain models for document ingestion."""

from pydantic import BaseModel, Field


class Document(BaseModel):
    """A source document used by AgentSieve's retrieval pipeline."""

    id: str
    content: str
    source: str
    metadata: dict[str, object] = Field(default_factory=dict)
