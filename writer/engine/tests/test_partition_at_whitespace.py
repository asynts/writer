import dataclasses
import typing
import pytest

import writer.engine.converter

@dataclasses.dataclass(kw_only=True, frozen=True)
class Case:
    input_: str
    expected: typing.Tuple[str, str, str]

cases = [
    Case(
        input_="hello world",
        expected=("hello", " ", "world")
    ),
    Case(
        input_="hello  world",
        expected=("hello", "  ", "world")
    ),
    Case(
        input_=" hello world",
        expected=("", " ", "hello world")
    ),
    Case(
        input_="  hello world",
        expected=("", "  ", "hello world")
    ),
    Case(
        input_="hello\t world",
        expected=("hello", "\t ", "world")
    ),
    Case(
        input_=" \nhello\t world",
        expected=("", " \n", "hello\t world")
    ),
]

@pytest.fixture(params=cases)
def case(request):
    return request.param

def test_partition_remaining_text(case):
    assert writer.engine.converter.partition_at_whitespace(case.input_) == case.expected
