"""Unit tests for the AgentSieve agent workflow."""

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from agentsieve.workflows import agent_graph


class FakeChatModel:
    """Deterministic chat model used to test graph behavior without an API call."""

    def invoke(self, messages):
        """Return a predictable response for the supplied messages."""
        return AIMessage(content=f"Fake response to: {messages[-1].content}")


def test_agent_graph_returns_model_response(monkeypatch):
    """The graph should return the model response when no tool is requested."""
    monkeypatch.setattr(agent_graph, "get_model", lambda: FakeChatModel())

    graph = agent_graph.build_agent_graph()

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="Hello AgentSieve"),
            ]
        }
    )

    messages = result["messages"]

    assert len(messages) == 2
    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert messages[0].content == "Hello AgentSieve"
    assert messages[1].content == "Fake response to: Hello AgentSieve"


def test_agent_graph_passes_full_message_history_to_model(monkeypatch):
    """The graph should provide the accumulated conversation to the model."""

    class RecordingChatModel:
        """Fake model that records the messages it receives."""

        def __init__(self):
            self.received_messages = None

        def invoke(self, messages):
            """Record the conversation history and return a deterministic response."""
            self.received_messages = messages
            return AIMessage(content="Recorded response")

    fake_model = RecordingChatModel()

    monkeypatch.setattr(
        agent_graph,
        "get_model",
        lambda: fake_model,
    )

    graph = agent_graph.build_agent_graph()

    graph.invoke(
        {
            "messages": [
                HumanMessage(content="First message"),
                HumanMessage(content="Latest message"),
            ]
        }
    )

    assert fake_model.received_messages is not None
    assert len(fake_model.received_messages) == 2
    assert fake_model.received_messages[0].content == "First message"
    assert fake_model.received_messages[1].content == "Latest message"


def test_agent_graph_executes_requested_tool(monkeypatch):
    """The graph should execute a requested tool and return to the agent."""

    class ToolCallingChatModel:
        """Fake model that requests a calculator tool before answering."""

        def __init__(self):
            self.calls = 0

        def invoke(self, messages):
            """Return a tool call first, then a final response."""
            self.calls += 1

            if self.calls == 1:
                return AIMessage(
                    content="",
                    tool_calls=[
                        {
                            "name": "calculator",
                            "args": {"expression": "25 * 4"},
                            "id": "call_1",
                            "type": "tool_call",
                        }
                    ],
                )

            return AIMessage(content="The result is 100.")

    fake_model = ToolCallingChatModel()

    monkeypatch.setattr(
        agent_graph,
        "get_model",
        lambda: fake_model,
    )

    graph = agent_graph.build_agent_graph()

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="What is 25 * 4?"),
            ]
        }
    )

    messages = result["messages"]

    assert isinstance(messages[0], HumanMessage)
    assert isinstance(messages[1], AIMessage)
    assert isinstance(messages[2], ToolMessage)
    assert isinstance(messages[3], AIMessage)

    assert messages[2].content == "100.0"
    assert messages[3].content == "The result is 100."
    assert fake_model.calls == 2
