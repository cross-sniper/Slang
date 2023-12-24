import ast
import json
import sys


class MySyntaxVisitor(ast.NodeVisitor):
    def visit_Assign(self, node):
        variable_name = node.targets[0].id
        value = self.visit(node.value)
        return {"type": "variable_assignment", "value_1": variable_name, "value_2": value}

    def visit_Str(self, node):
        return node.s

    def visit_Num(self, node):
        return node.n

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = self.visit(node.op)
        return {"type": "binary_operation", "left": left, "op": op, "right": right}

    def visit_Add(self, node):
        return "+"

    def visit_Sub(self, node):
        return "-"

    def visit_Div(self, node):
        return "/"

    def visit_Mult(self, node):
        return "*"

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Call(self, node):
        function_name = self.visit(node.func)
        args = [self.visit(arg) for arg in node.args]
        return {"type": "function_call", "name": function_name, "args": args}

    def visit_Name(self, node):
        return node.id

    def visit_While(self, node):
        condition = self.visit(node.test)
        body = [self.visit(stmt) for stmt in node.body]
        return {"type": "while_loop", "condition": condition, "body": body}

    def visit_Compare(self, node):
        left = self.visit(node.left)
        op = self.visit(node.ops[0])
        right = self.visit(node.comparators[0])
        return {"type": "comparison", "left": left, "op": op, "right": right}

    def visit_Lt(self, node):
        return "<"
    def visit_Gt(self, node):
        return ">"

    def generic_visit(self, node):
        return super().generic_visit(node)

def parse_custom_syntax(code):
    tree = ast.parse(code)
    visitor = MySyntaxVisitor()
    result = [visitor.visit(stmt) for stmt in tree.body]
    return [stmt for stmt in result if stmt is not None]

if len(sys.argv) < 2:
    print("Usage: python main.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
with open(filename) as f:
    code = f.read()

result = parse_custom_syntax(code)
print(json.dumps(result, indent=4))
