"""A simple command-line calculator.

Type a math expression and press Enter to see the result.
Supports + - * / // % ** (or ^), parentheses, and a few functions.
"""

import ast
import math
import operator

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log10,
    "ln": math.log,
}

CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

HELP_TEXT = """
Operators:  +  -  *  /  //  %  ** (or ^)  and parentheses ( )
Functions:  sqrt(x)  abs(x)  round(x)  sin(x)  cos(x)  tan(x)  log(x)  ln(x)
Constants:  pi  e
Memory:     ans  (the result of your last calculation)
Commands:   help  quit
Examples:   2 + 3 * 4     (2 + 3) * 4     2 ^ 10     sqrt(16) + ans
"""


def evaluate(expression, ans=0):
    """Safely calculate a math expression given as text and return the number."""
    expression = expression.replace("^", "**")
    tree = ast.parse(expression, mode="eval")
    return _evaluate_node(tree.body, ans)


def _evaluate_node(node, ans):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in BINARY_OPERATORS:
        left = _evaluate_node(node.left, ans)
        right = _evaluate_node(node.right, ans)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("Exponent is too large")
        return BINARY_OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY_OPERATORS:
        return UNARY_OPERATORS[type(node.op)](_evaluate_node(node.operand, ans))

    if isinstance(node, ast.Name):
        if node.id == "ans":
            return ans
        if node.id in CONSTANTS:
            return CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")

    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in FUNCTIONS
        and len(node.args) == 1
        and not node.keywords
    ):
        return FUNCTIONS[node.func.id](_evaluate_node(node.args[0], ans))

    raise ValueError("Invalid expression")


def format_result(value):
    """Show whole numbers without a trailing .0 and trim float noise."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.10g}"
    return str(value)


def main():
    print("Calculator - type 'help' for instructions, 'quit' to exit.")
    ans = 0
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue
        if line.lower() in ("quit", "exit", "q"):
            break
        if line.lower() == "help":
            print(HELP_TEXT)
            continue

        try:
            ans = evaluate(line, ans)
            print(format_result(ans))
        except ZeroDivisionError:
            print("Error: cannot divide by zero")
        except SyntaxError:
            print("Error: that doesn't look like a valid expression")
        except (ValueError, TypeError, OverflowError) as error:
            print(f"Error: {error}")

    print("Goodbye!")


if __name__ == "__main__":
    main()
