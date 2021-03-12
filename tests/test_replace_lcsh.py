# -*- coding: utf-8 -*-

import pytest

from src.replace_lcsh import replace_term, lcsh_fields, normalize_subfields


# def test_flip_impacted_fields(fake_bib):
#     pass


@pytest.mark.parametrize(
    "arg,expectation",
    [
        (1, ["a", "local term", "x", "subX1", "x", "subX2", "z", "subZ."]),
        (3, ["a", "subA", "x", "local term", "x", "subX2", "z", "subZ."]),
        (5, ["a", "subA", "x", "subX1", "x", "local term", "z", "subZ."]),
        (7, ["a", "subA", "x", "subX1", "x", "subX2", "z", "local term."]),
    ],
)
def test_replace_term(fake_subfields, arg, expectation):
    assert replace_term(fake_subfields, arg, "local term") == expectation


def test_lcsh_fields(fake_subjects):
    assert len(lcsh_fields(fake_subjects)) == 2


def test_normalize_subields(fake_subfields):
    assert normalize_subfields(fake_subfields) == [
        "a",
        "suba",
        "x",
        "subx1",
        "x",
        "subx2",
        "z",
        "subz",
    ]
