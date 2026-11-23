"""OpenTelemetry tracer configuration for the AgentSieve runtime."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.telemetry.otel_exporter import AgentSieveSpanExporter


def create_tracer_provider(collector: InMemoryTraceCollector) -> TracerProvider:
    """Create an OpenTelemetry tracer provider for AgentSieve."""
    provider = TracerProvider()
    exporter = AgentSieveSpanExporter(collector)
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)

    return provider


def configure_tracing(collector: InMemoryTraceCollector) -> trace.Tracer:
    """Configure OpenTelemetry and return an AgentSieve tracer."""
    provider = create_tracer_provider(collector)
    trace.set_tracer_provider(provider)

    return trace.get_tracer("agentsieve")
