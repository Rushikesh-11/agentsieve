from datetime import UTC, datetime

from agentsieve.models.trace_record import TraceRecord
from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector


def test_collector_stores_trace_record():
    collector = InMemoryTraceCollector()

    record = TraceRecord(
        trace_id="trace-123",
        span_id="span-456",
        name="llm_call",
        start_time=datetime.now(UTC),
        status="OK",
    )

    collector.collect(record)

    assert collector.records == [record]


def test_collector_stores_multiple_trace_records():
    collector = InMemoryTraceCollector()

    first_record = TraceRecord(
        trace_id="trace-123",
        span_id="span-456",
        name="llm_call",
        start_time=datetime.now(UTC),
        status="OK",
    )
    second_record = TraceRecord(
        trace_id="trace-123",
        span_id="span-789",
        name="tool_call",
        start_time=datetime.now(UTC),
        status="OK",
    )

    collector.collect(first_record)
    collector.collect(second_record)

    assert collector.records == [first_record, second_record]
