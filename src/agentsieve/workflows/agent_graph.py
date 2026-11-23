"""LangGraph workflow definitions for the AgentSieve agent runtime."""

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from opentelemetry import trace

from agentsieve.agents.tools import calculator

_TOOLS = (calculator,)
tracer = trace.get_tracer("agentsieve.agent")


class AgentState(TypedDict):
    """State carried through the AgentSieve agent workflow."""

    messages: Annotated[list[BaseMessage], add_messages]


def get_model():
    """Create the configured chat model with AgentSieve tools bound."""
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
    ).bind_tools(_TOOLS)


def agent_node(state: AgentState) -> dict[str, list[AIMessage]]:
    """Invoke the configured chat model using the current conversation state."""
    with tracer.start_as_current_span("agent") as span:
        span.set_attribute("agent.node", "agent")
        span.set_attribute("agent.message_count", len(state["messages"]))

        response = get_model().invoke(state["messages"])

        return {"messages": [response]}


def build_agent_graph():
    """Build and compile the AgentSieve tool-using agent workflow."""
    graph = StateGraph(AgentState)

    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(_TOOLS))

    graph.add_edge(START, "agent")

    graph.add_conditional_edges(
        "agent",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )

    graph.add_edge("tools", "agent")

    return graph.compile()
