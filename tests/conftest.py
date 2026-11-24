"""Shared pytest fixtures for AgentSieve tests."""

import pytest

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.telemetry.tracer import configure_tracing


@pytest.fixture(scope="session")
def tracing_collector() -> InMemoryTraceCollector:
    """Configure OpenTelemetry once for the entire test session."""
    collector = InMemoryTraceCollector()
    configure_tracing(collector)
    return collector


@pytest.fixture
def trace_collector(
    tracing_collector: InMemoryTraceCollector,
) -> InMemoryTraceCollector:
    """Provide a clean trace collector for each test."""
    tracing_collector.records.clear()
    return tracing_collector
