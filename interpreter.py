import json
import sys
import re

class MyInterpreter:
    def __init__(self):
        self.variables = {}

    def interpret(self, statement):
        if statement["type"] == "variable_assignment":
            self.variables[statement["value_1"]] = self.evaluate(statement["value_2"])
        elif statement["type"] == "binary_operation":
            return self.evaluate_binary_operation(statement)
        elif statement["type"] == "function_call":
            return self.execute_function_call(statement)
        elif statement["type"] == "while_loop":
            return self.execute_while_loop(statement)
        elif statement["type"] == "comparison":
            return self.evaluate_comparison(statement)
        else:
            raise NotImplementedError(f"Interpreter does not support statements of type {statement['type']}")

    def evaluate(self, expression):
        if isinstance(expression, dict):
            return self.interpret(expression)
        elif isinstance(expression, str) and expression in self.variables:
            return self.variables[expression]
        else:
            return expression

    def evaluate_binary_operation(self, binary_op):
        left = self.evaluate(binary_op["left"])
        right = self.evaluate(binary_op["right"])
        op = binary_op["op"]

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        else:
            raise ValueError(f"Unsupported binary operation: {op}")

    def execute_function_call(self, func_call):
        func_name = func_call["name"]
        args = [self.evaluate(arg) for arg in func_call["args"]]

        if func_name == "print":
            print(*args)
        elif func_name == "input":
            return input(*args)
        elif func_name == "Format":
            return self.format_string(args)
        else:
            raise ValueError(f"Unsupported function call: {func_name}")

    def format_string(self, args):
        def replace_match(match):
            index = int(match.group(1))
            return str(args[index - 1])

        pattern = re.compile(r'\$(\d+)')
        return pattern.sub(replace_match, args[0])

    def execute_while_loop(self, while_loop):
        result = None
        while self.evaluate(while_loop["condition"]):
            for stmt in while_loop["body"]:
                result = self.interpret(stmt)
        return result

    def evaluate_comparison(self, comparison):
        left = self.evaluate(comparison["left"])
        right = self.evaluate(comparison["right"])
        op = comparison["op"]

        if op == "<":
            return left < right
        elif op == ">":
            return left > right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        else:
            raise ValueError(f"Unsupported comparison operation: {op}")

def interpret_custom_syntax(statements):
    interpreter = MyInterpreter()
    for statement in statements:
        interpreter.interpret(statement)

# Example usage
with open(sys.argv[1]) as f:
    code = json.loads(f.read())
interpret_custom_syntax(code)
