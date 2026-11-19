from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentTrace(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    started_at: datetime
    completed_at: datetime | None = None
    input: str
    output: str | None = None
