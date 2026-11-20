from datetime import datetime

from pydantic import BaseModel, Field


class TraceRecord(BaseModel):
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    name: str
    start_time: datetime
    end_time: datetime | None = None
    status: str
    attributes: dict[str, object] = Field(default_factory=dict)
