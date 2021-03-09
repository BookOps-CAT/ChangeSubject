# -*- coding: utf-8 -*-

import pytest

from src.replace_lcsh import replace_term


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


# def test_replace_term(fake_field_1):
#     position = 1
#     local_term = "Undocumented immigrants"
#     assert replace_term(fake_field_1, position, local_term).subfields == [
#         "a",
#         "Undocumented immigrants",
#         "x",
#         "Government policy",
#         "z",
#         "United States.",
#     ]
