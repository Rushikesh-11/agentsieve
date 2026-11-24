"""OpenTelemetry tracing wrapper for LangGraph tool execution."""

from collections.abc import Callable

from langchain_core.messages import ToolMessage
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command
from opentelemetry import trace

tracer = trace.get_tracer("agentsieve.tool")


def trace_tool_call(
    request: ToolCallRequest,
    execute: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    """Trace a LangGraph tool execution with an OpenTelemetry span."""
    tool_name = request.tool_call["name"]

    with tracer.start_as_current_span(f"tool:{tool_name}") as span:
        span.set_attribute("tool.name", tool_name)

        try:
            result = execute(request)
            span.set_attribute("tool.status", "success")
            return result
        except Exception as exc:
            span.set_attribute("tool.status", "error")
            span.record_exception(exc)
            raise
