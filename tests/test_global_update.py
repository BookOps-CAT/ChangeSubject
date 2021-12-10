from pymarc import Field, Record
import pytest

from src.global_update import adopt_lc, is_bookops_term


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


def test_adopt_lc(stub_bib):
    stub_bib.add_field(
        Field(
            tag="650",
            indicators=[" ", "7"],
            subfields=[
                "a",
                "Noncitizen criminals",
                "z",
                "United States.",
                "2",
                "bookops",
            ],
        )
    )
    adopt_lc(stub_bib)
    fields = stub_bib.subjects()
    assert len(fields) == 4
    for field in fields:
        assert "bookops" not in field.subfields

    changed = fields[-1]
    assert changed.indicators == [" ", "0"]
    assert changed.subfields == ["a", "Noncitizen criminals", "z", "United States."]
