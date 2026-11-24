"""Integration tests for OpenTelemetry tracing of the AgentSieve agent runtime."""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.workflows.agent_graph import build_agent_graph


def test_agent_execution_creates_trace_record(
    monkeypatch,
    trace_collector: InMemoryTraceCollector,
) -> None:
    """Agent execution should produce a normalized trace record."""
    collector = trace_collector

    fake_model = RunnableLambda(lambda _: AIMessage(content="Hello from the test agent."))

    monkeypatch.setattr(
        "agentsieve.workflows.agent_graph.get_model",
        lambda: fake_model,
    )

    graph = build_agent_graph()

    result = graph.invoke({"messages": [HumanMessage(content="Hello")]})

    assert result["messages"][-1].content == "Hello from the test agent."

    assert len(collector.records) == 1

    record = collector.records[0]

    assert record.name == "agent"
    assert record.status == "UNSET"
    assert record.attributes["agent.node"] == "agent"
    assert record.attributes["agent.message_count"] == 1
