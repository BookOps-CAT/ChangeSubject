from pymarc import Field
import pytest

from src.global_update import is_bookops_term


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (["a", "foo", "b", "bar", "2", "bookops"], True),
        (["a", "foo", "2", "fast"], False),
        (["a", "foo"], False),
    ],
)
def test_is_bookops_term(arg, expectation):
    field = Field(tag="650", subfields=arg)
    assert is_bookops_term(field) == expectation
