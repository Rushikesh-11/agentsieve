from datetime import UTC, datetime

from agentsieve.models.trace_record import TraceRecord


def test_trace_record_creates_with_required_fields():
    started_at = datetime.now(UTC)

    record = TraceRecord(
        trace_id="trace-123",
        span_id="span-456",
        name="llm_call",
        start_time=started_at,
        status="OK",
    )

    assert record.trace_id == "trace-123"
    assert record.span_id == "span-456"
    assert record.parent_span_id is None
    assert record.name == "llm_call"
    assert record.start_time == started_at
    assert record.end_time is None
    assert record.status == "OK"
    assert record.attributes == {}


def test_trace_record_supports_parent_span_and_attributes():
    record = TraceRecord(
        trace_id="trace-123",
        span_id="span-789",
        parent_span_id="span-456",
        name="tool_call",
        start_time=datetime.now(UTC),
        status="ERROR",
        attributes={
            "tool.name": "search",
            "retry_count": 2,
        },
    )

    assert record.parent_span_id == "span-456"
    assert record.status == "ERROR"
    assert record.attributes["tool.name"] == "search"
    assert record.attributes["retry_count"] == 2
