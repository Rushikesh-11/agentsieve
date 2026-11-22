"""Unit tests for AgentSieve runtime tools."""

import pytest
from langchain_core.tools import BaseTool

from agentsieve.agents.tools import calculate, calculator


def test_calculate_addition():
    """Calculate should evaluate addition correctly."""
    assert calculate("10 + 5") == 15.0


def test_calculate_operator_precedence():
    """Calculate should respect standard operator precedence."""
    assert calculate("10 + 5 * 2") == 20.0


def test_calculate_power():
    """Calculate should support exponentiation."""
    assert calculate("2 ** 3") == 8.0


def test_calculate_rejects_unsupported_syntax():
    """Calculate should reject expressions outside the supported syntax."""
    with pytest.raises(ValueError, match="unsupported syntax"):
        calculate("__import__('os').system('echo unsafe')")


def test_calculate_rejects_empty_expression():
    """Calculate should reject an empty expression."""
    with pytest.raises(ValueError, match="cannot be empty"):
        calculate("")


def test_calculate_zero_division():
    """Calculate should propagate division-by-zero errors."""
    with pytest.raises(ZeroDivisionError):
        calculate("10 / 0")


def test_calculator_is_a_langchain_tool():
    """Calculator should expose the expected LangChain tool interface."""
    assert isinstance(calculator, BaseTool)
    assert calculator.name == "calculator"
    assert "arithmetic" in calculator.description.lower()


def test_calculator_tool_invocation():
    """Calculator tool should invoke the underlying calculation logic."""
    assert calculator.invoke({"expression": "25 * 4"}) == 100.0
