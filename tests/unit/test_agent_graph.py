from langchain_core.messages import AIMessage, HumanMessage

from agentsieve.workflows import agent_graph


class FakeChatModel:
    """Deterministic chat model used to test graph behavior without an API call."""

    def invoke(self, messages):
        """Return a predictable response for the supplied messages."""
        return AIMessage(content=f"Fake response to: {messages[-1].content}")


def test_agent_graph_preserves_input_and_adds_model_response(monkeypatch):
    """The graph should preserve the input and append the model response."""
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
    monkeypatch.setattr(agent_graph, "get_model", lambda: fake_model)

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
