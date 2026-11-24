"""Integration tests for OpenTelemetry tracing of LangGraph tool execution."""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableLambda

from agentsieve.telemetry.in_memory_collector import InMemoryTraceCollector
from agentsieve.workflows.agent_graph import build_agent_graph


def test_tool_execution_creates_tool_trace_record(
    monkeypatch,
    trace_collector: InMemoryTraceCollector,
) -> None:
    """Tool execution should produce a normalized tool trace record."""
    collector = trace_collector

    responses = iter(
        [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "calculator",
                        "args": {"expression": "2 + 3"},
                        "id": "call_1",
                    }
                ],
            ),
            AIMessage(content="The result is 5."),
        ]
    )

    fake_model = RunnableLambda(lambda _: next(responses))

    monkeypatch.setattr(
        "agentsieve.workflows.agent_graph.get_model",
        lambda: fake_model,
    )

    graph = build_agent_graph()

    result = graph.invoke({"messages": [HumanMessage(content="What is 2 + 3?")]})

    assert result["messages"][-1].content == "The result is 5."

    tool_records = [record for record in collector.records if record.name == "tool:calculator"]

    assert len(tool_records) == 1

    record = tool_records[0]

    assert record.status == "UNSET"
    assert record.attributes["tool.name"] == "calculator"
    assert record.attributes["tool.status"] == "success"
