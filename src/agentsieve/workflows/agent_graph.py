from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    """State carried through the AgentSieve agent workflow."""

    messages: Annotated[list[BaseMessage], add_messages]


def get_model() -> ChatGoogleGenerativeAI:
    """Create the configured Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
    )


def agent_node(state: AgentState) -> dict[str, list[AIMessage]]:
    """Invoke the configured chat model using the current conversation state."""
    response = get_model().invoke(state["messages"])

    return {
        "messages": [response],
    }


def build_agent_graph():
    """Build and compile the AgentSieve LangGraph agent workflow."""
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)

    graph.add_edge(START, "agent")
    graph.add_edge("agent", END)

    return graph.compile()
