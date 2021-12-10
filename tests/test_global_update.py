from pymarc import Field, Record
import pytest

from src.global_update import (
    adopt_lc,
    change_local,
    is_bookops_term,
    isolate_tail,
    normalize_subfield,
    split_local,
)


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


@pytest.mark.parametrize("arg,expectation", [("Foo", "Foo"), ("Foo.", "Foo")])
def test_normalize_subfield(arg, expectation):
    assert normalize_subfield(arg) == expectation


def test_isolate_tail():
    field = Field(
        tag="650",
        indicators=[" ", "7"],
        subfields=["a", "Foo", "x", "Bar.", "2", "bookops"],
    )
    assert isolate_tail(field) == ["x", "Bar."]


@pytest.mark.parametrize(
    "arg",
    [
        ["a", "Noncitizens."],
        ["a", "Noncitizen criminals."],
        ["a", "Noncitizens (Greek law)."],
        ["a", "Noncitizens in art."],
        ["a", "Noncitizens", "x", "Care", "z", "United States."],
        ["a", "Church work with noncitizens."],
        ["a", "Corporations, Foreign."],
    ],
)
def test_adopt_lc(stub_bib, arg):
    subfields = arg[:]
    subfields.extend(["2", "bookops"])
    stub_bib.add_field(
        Field(
            tag="650",
            indicators=[" ", "7"],
            subfields=subfields,
        )
    )
    adopt_lc(stub_bib)
    fields = stub_bib.subjects()
    assert len(fields) == 4
    changed = fields[-1]
    assert changed.indicators == [" ", "0"]
    assert changed.subfields == subfields[:-2]


@pytest.mark.parametrize(
    "arg,expectation1,expectation2",
    [
        (
            ["a", "Children of undocumented immigrants.", "2", "bookops"],
            ["a", "Children of noncitizens."],
            ["a", "Undocumented immigration.", "2", "bookops"],
        ),
        (
            [
                "a",
                "Undocumented children",
                "x",
                "Government policy",
                "z",
                "United States.",
                "2",
                "bookops",
            ],
            [
                "a",
                "Noncitizen children",
                "x",
                "Government policy",
                "z",
                "United States.",
            ],
            [
                "a",
                "Undocumented immigration",
                "x",
                "Government policy",
                "z",
                "United States.",
                "2",
                "bookops",
            ],
        ),
        (
            ["a", "Undocumented immigrants", "z", "United States.", "2", "bookops"],
            ["a", "Noncitizens", "z", "United States."],
            ["a", "Undocumented immigration", "z", "United States.", "2", "bookops"],
        ),
        (
            ["a", "Women undocumented immigrants.", "2", "bookops"],
            ["a", "Women noncitizens."],
            ["a", "Undocumented immigration.", "2", "bookops"],
        ),
    ],
)
def test_split_local(stub_bib, arg, expectation1, expectation2):
    subfields = arg[:]
    stub_bib.add_field(Field(tag="650", indicators=[" ", "7"], subfields=subfields))
    # print(stub_bib)
    assert len(stub_bib.subjects()) == 4
    split_local(stub_bib)

    fields = stub_bib.subjects()
    assert len(fields) == 5
    changedA = fields[-2]
    changedB = fields[-1]

    assert changedA.indicators == [" ", "0"]
    assert changedA.subfields == expectation1

    assert changedB.indicators == [" ", "7"]
    assert changedB.subfields == expectation2


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (
            ["a", "Undocumented immigrants in literature.", "2", "bookops"],
            ["a", "Undocumented immigration in literature.", "2", "bookops"],
        ),
        (
            [
                "a",
                "Undocumented immigrants in literature",
                "v",
                "Juvenile literature.",
                "2",
                "bookops",
            ],
            [
                "a",
                "Undocumented immigration in literature",
                "v",
                "Juvenile literature.",
                "2",
                "bookops",
            ],
        ),
    ],
)
def test_change_local(stub_bib, arg, expectation):
    stub_bib.add_field(Field(tag="650", indicators=[" ", "7"], subfields=arg))
    assert len(stub_bib.subjects()) == 4

    change_local(stub_bib)

    fields = stub_bib.subjects()
    assert len(fields) == 4
    changed = fields[-1]
    assert changed.indicators == [" ", "7"]
    assert changed.subfields == expectation
