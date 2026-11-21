from datetime import UTC, datetime

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.trace import format_span_id, format_trace_id

from agentsieve.models.trace_record import TraceRecord


def to_trace_record(span: ReadableSpan) -> TraceRecord:
    context = span.context

    if context is None:
        raise ValueError("ReadableSpan must have a span context")

    if span.start_time is None:
        raise ValueError("ReadableSpan must have a start time")

    return TraceRecord(
        trace_id=format_trace_id(context.trace_id),
        span_id=format_span_id(context.span_id),
        parent_span_id=(format_span_id(span.parent.span_id) if span.parent is not None else None),
        name=span.name,
        start_time=datetime.fromtimestamp(span.start_time / 1_000_000_000, tz=UTC),
        end_time=(
            datetime.fromtimestamp(span.end_time / 1_000_000_000, tz=UTC)
            if span.end_time is not None
            else None
        ),
        status=span.status.status_code.name,
        attributes=dict(span.attributes),
    )
