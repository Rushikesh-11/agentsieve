"""Tools available to the AgentSieve agent runtime."""

import ast
import operator
from typing import Final

from langchain_core.tools import tool

_ALLOWED_OPERATORS: Final = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> float:
    """Evaluate a restricted arithmetic expression safely.

    Args:
        expression: Arithmetic expression containing supported numeric
            operators.

    Returns:
        The numeric result of the expression.

    Raises:
        ValueError: If the expression is empty, invalid, or contains
            unsupported syntax.
        ZeroDivisionError: If the expression attempts division by zero.
    """
    if not expression.strip():
        raise ValueError("Expression cannot be empty.")

    try:
        tree = ast.parse(expression, mode="eval")
        return float(_evaluate_node(tree.body))
    except SyntaxError as exc:
        raise ValueError("Invalid arithmetic expression.") from exc


def _evaluate_node(node: ast.AST) -> float:
    """Recursively evaluate a supported arithmetic AST node."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        operation = _ALLOWED_OPERATORS[type(node.op)]
        return float(operation(left, right))

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _evaluate_node(node.operand)
        operation = _ALLOWED_OPERATORS[type(node.op)]
        return float(operation(operand))

    raise ValueError("Expression contains unsupported syntax.")


@tool
def calculator(expression: str) -> float:
    """Calculate the result of a supported arithmetic expression.

    Args:
        expression: Arithmetic expression to evaluate.

    Returns:
        The calculated numeric result.
    """
    return calculate(expression)
