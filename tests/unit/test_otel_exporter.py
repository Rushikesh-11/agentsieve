"""Unit tests for the AgentSieve OpenTelemetry span exporter."""

from datetime import UTC, datetime

from opentelemetry.sdk.trace import ReadableSpan, SpanContext
from opentelemetry.trace import SpanKind
from opentelemetry.trace.status import Status, StatusCode

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.telemetry.otel_exporter import AgentSieveSpanExporter


def test_export_converts_spans_and_collects_records() -> None:
    collector = InMemoryTraceCollector()
    exporter = AgentSieveSpanExporter(collector)

    context = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x1234567890ABCDEF,
        is_remote=False,
    )

    span = ReadableSpan(
        name="agent",
        context=context,
        parent=None,
        resource=None,
        attributes={"component": "agent"},
        events=(),
        links=(),
        start_time=1_000_000_000,
        end_time=2_000_000_000,
        status=Status(StatusCode.OK),
        kind=SpanKind.INTERNAL,
    )

    result = exporter.export([span])

    assert result.name == "SUCCESS"
    assert len(collector.records) == 1

    record = collector.records[0]

    assert record.trace_id == "1234567890abcdef1234567890abcdef"
    assert record.span_id == "1234567890abcdef"
    assert record.name == "agent"
    assert record.status == "OK"
    assert record.attributes == {"component": "agent"}
    assert record.start_time == datetime.fromtimestamp(1, tz=UTC)
    assert record.end_time == datetime.fromtimestamp(2, tz=UTC)


def test_export_handles_multiple_spans() -> None:
    collector = InMemoryTraceCollector()
    exporter = AgentSieveSpanExporter(collector)

    context = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x1234567890ABCDEF,
        is_remote=False,
    )

    spans = [
        ReadableSpan(
            name="agent",
            context=context,
            parent=None,
            resource=None,
            attributes={},
            events=(),
            links=(),
            start_time=1_000_000_000,
            end_time=2_000_000_000,
            status=Status(StatusCode.OK),
            kind=SpanKind.INTERNAL,
        ),
        ReadableSpan(
            name="tool",
            context=context,
            parent=None,
            resource=None,
            attributes={},
            events=(),
            links=(),
            start_time=2_000_000_000,
            end_time=3_000_000_000,
            status=Status(StatusCode.OK),
            kind=SpanKind.INTERNAL,
        ),
    ]

    result = exporter.export(spans)

    assert result.name == "SUCCESS"
    assert len(collector.records) == 2
    assert [record.name for record in collector.records] == ["agent", "tool"]
