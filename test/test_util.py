import pytest
from   email2dict import takes_argument

def simple(foo):
    return foo

def defaulting(foo=None):
    return foo

def kwarged(**kwargs):
    return kwargs

def arged(*foo):
    return foo

@pytest.mark.parametrize("func,arg,result", [
    (simple, "foo", True),
    (simple, "bar", False),
    (defaulting, "foo", True),
    (defaulting, "bar", False),
    (kwarged, "foo", True),
    (kwarged, "kwargs", True),
    (arged, "foo", False),
])
def test_takes_argument(func, arg, result):
    assert takes_argument(func, arg) is result
