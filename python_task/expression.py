import ast

from ast import Expr, Call, BoolOp, And, Or, Not, Compare, Name, Gt, Lt, GtE, LtE, Eq, NotEq, Constant, Subscript, Index, \
    BinOp, Add, Sub, Mult, Mod, Div, FloorDiv, Attribute
from addict import Dict


class DictNoDefault(Dict):
    def __missing__(self, key):
        raise KeyError(key)


class ForbiddenASTException(Exception):
    pass


class ASTPreparer(ast.NodeTransformer):
    def generic_visit(self, node):
        print(f"visiting {node}")
        if node.__class__ in [Expr, Call, Attribute, BoolOp, And, Or, Not, Compare, Name, Gt, Lt, GtE,
                              LtE, Eq, NotEq, Constant, Subscript, Index, BinOp, Add, Sub, Mult, Mod,
                              Div, FloorDiv]:
            return node

        raise ForbiddenASTException(node.__class__.__name__)

    def visit_Module(self, node):
        print(f"visiting odule {node}")
        assert len(node.body) == 1, "Cannot have more than 1 expression"
        assert isinstance(node.body[0], Expr), "Expression needs to be of type ast.Expr"
        return ast.Expression(body=self.visit(node.body[0].value))


class DynamicExprFunction:
    def __init__(self, expr):
        self.expr = compile(ASTPreparer().visit((ast.parse(expr))), "<string>", "eval")

    def __call__(self, data):
        return eval(self.expr, {}, DictNoDefault(data))
