from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from agentsieve.models.trace import AgentTrace


def test_agent_trace_creates_with_required_fields():
    started_at = datetime.now(UTC)

    trace = AgentTrace(
        started_at=started_at,
        input="What is FastAPI?",
    )

    assert trace.input == "What is FastAPI?"
    assert trace.output is None
    assert trace.completed_at is None
    assert trace.id is not None
    assert trace.started_at == started_at


def test_agent_trace_requires_input():
    with pytest.raises(ValidationError):
        AgentTrace(
            started_at=datetime.now(UTC),
        )
