import pytest
from pymarc import Field, Record


from src.remove_fast import (
    normalize_field,
    fast_subjects,
    fast4deletion,
    remove_fast_terms,
)


@pytest.mark.parametrize(
    "subfields,expectation",
    [
        (["a", "Subfield A."], "subfield a"),
        (["a", "Subfield A", "x", "Subfield X."], "subfield a subfield x"),
        (["a", "Subfield A"], "subfield a"),
        (["a", "Subfield A.with.extra.periods."], "subfield awithextraperiods"),
    ],
)
def test_normalize_field(subfields, expectation):
    field = Field(tag="650", indicators=[" ", "0"], subfields=subfields)
    assert normalize_field(field) == expectation


@pytest.mark.parametrize(
    "subfields,expectation",
    [
        ([["a", "sub A"]], []),
        ([["a", "sub A"], ["a", "sub A", "2", "gsafd"]], []),
        ([["a", "sub A"], ["a", "sub A", "2", "fast"]], [["a", "sub A", "2", "fast"]]),
        (
            [["a", "sub A"], ["a", "sub A", "2", "fast"], ["a", "sub A", "2", "FAST"]],
            [["a", "sub A", "2", "fast"], ["a", "sub A", "2", "FAST"]],
        ),
    ],
)
def test_fast_subjects(subfields, expectation):
    fields = [Field(tag="650", indicators=[" ", " "], subfields=s) for s in subfields]
    assert [f.subfields for f in fast_subjects(fields)] == expectation


def test_fast4deletion(fake_fast_bib):
    terms_for_deletion = ["Unwanted FAST"]
    [f.subfields for f in fast4deletion(terms_for_deletion, fake_fast_bib)] == [
        ["a", "Unwanted FAST.", "2", "fast"]
    ]


def test_remove_fast_terms(fake_fast_bib):
    terms_for_deletion = ["Unwanted FAST"]
    remove_fast_terms(fake_fast_bib, terms_for_deletion)
    subjects = fake_fast_bib.subjects()
    assert [s.subfields for s in subjects] == [
        ["a", "LCSH sub A."],
        ["a", "neutral FAST.", "2", "fast"],
    ]
