"""OpenTelemetry span exporter that converts spans into AgentSieve trace records."""

from collections.abc import Sequence

from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.telemetry.otel_adapter import to_trace_record


class AgentSieveSpanExporter(SpanExporter):
    """Export OpenTelemetry spans into an AgentSieve trace collector."""

    def __init__(self, collector: InMemoryTraceCollector) -> None:
        self.collector = collector

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        for span in spans:
            record = to_trace_record(span)
            self.collector.collect(record)

        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        """Release exporter resources."""
