from datetime import UTC, datetime

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import SpanContext, Status, StatusCode

from agentsieve.telemetry.otel_adapter import to_trace_record


def test_to_trace_record_converts_span():
    context = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x1234567890ABCDEF,
        is_remote=False,
    )

    span = ReadableSpan(
        name="llm_call",
        context=context,
        start_time=1_700_000_000_000_000_000,
        end_time=1_700_000_001_000_000_000,
        status=Status(StatusCode.OK),
        attributes={
            "model": "test-model",
            "tokens": 100,
        },
    )

    record = to_trace_record(span)

    assert record.trace_id == "1234567890abcdef1234567890abcdef"
    assert record.span_id == "1234567890abcdef"
    assert record.name == "llm_call"
    assert record.start_time == datetime.fromtimestamp(
        1_700_000_000,
        tz=UTC,
    )
    assert record.end_time == datetime.fromtimestamp(
        1_700_000_001,
        tz=UTC,
    )
    assert record.status == "OK"
    assert record.attributes == {
        "model": "test-model",
        "tokens": 100,
    }


def test_to_trace_record_converts_parent_span():
    context = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x1111111111111111,
        is_remote=False,
    )

    parent = SpanContext(
        trace_id=0x1234567890ABCDEF1234567890ABCDEF,
        span_id=0x2222222222222222,
        is_remote=False,
    )

    span = ReadableSpan(
        name="tool_call",
        context=context,
        parent=parent,
        start_time=1_700_000_000_000_000_000,
        status=Status(StatusCode.ERROR),
    )

    record = to_trace_record(span)

    assert record.span_id == "1111111111111111"
    assert record.parent_span_id == "2222222222222222"
    assert record.status == "ERROR"
    assert record.end_time is None
