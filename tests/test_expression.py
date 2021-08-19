import pytest

from python_task.expression import DynamicExprFunction, ForbiddenASTException

simple_expressions = [
    ("1", {}, 1),
    ("'hello'", {}, "hello"),
    ("True", {}, True),
    ("x", {"x": True}, True),
    ("x", {"x": "y"}, "y"),
]

complex_expressions = [
    ("1+1", {}, 2),
    ("'hello'<'goodbye'", {}, False),
    ("x+y > 3", {"x": 1, "y": 2}, False),
    ("x+y >= 3", {"x": 1, "y": 2}, True),
    ("(x + y + 'z').upper() == 'XXTWOZ'", {"x": "xx", "y": "two"}, True),
]


failed_expressions = [
    ("1+", {}, SyntaxError("invalid syntax (<unknown>, line 1)")),
    ("'hello'-'goodbye'", {}, TypeError("unsupported operand type(s) for -: 'str' and 'str'")),
    ("x+y > 3", {"x": 1}, NameError("name 'y' is not defined")),
    ("def x():\n  pass", {}, AssertionError("Expression needs to be of type ast.Expr")),
    ("lambda x: x", {}, ForbiddenASTException('Lambda')),
    ("1+1; 2+3", {}, AssertionError("Cannot have more than 1 expression")),
]


@pytest.mark.parametrize("expression,inp,expected", simple_expressions)
def test_simple_expressions(expression, inp, expected):
    assert DynamicExprFunction(expression)(inp) == expected


@pytest.mark.parametrize("expression,inp,expected", complex_expressions)
def test_complex_expressions(expression, inp, expected):
    assert DynamicExprFunction(expression)(inp) == expected


@pytest.mark.parametrize("expression,inp,expected", failed_expressions)
def test_failed_expressions(expression, inp, expected):
    with pytest.raises(expected.__class__) as exc_info:
        DynamicExprFunction(expression)(inp)
    assert str(expected) == str(exc_info.value)