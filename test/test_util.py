from typing import Any, Callable, Dict
import pytest
from mailbits.email2dict import takes_argument


def simple(foo: Any) -> Any:
    return foo


def defaulting(foo: Any = None) -> Any:
    return foo


def kwarged(**kwargs: Any) -> Dict[str, Any]:
    return kwargs


def arged(*foo: Any) -> tuple:
    return foo


@pytest.mark.parametrize(
    "func,arg,result",
    [
        (simple, "foo", True),
        (simple, "bar", False),
        (defaulting, "foo", True),
        (defaulting, "bar", False),
        (kwarged, "foo", True),
        (kwarged, "kwargs", True),
        (arged, "foo", False),
    ],
)
def test_takes_argument(func: Callable, arg: str, result: bool) -> None:
    assert takes_argument(func, arg) is result
