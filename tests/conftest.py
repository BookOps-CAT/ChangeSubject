# -*- coding: utf-8 -*-

import pytest


from pymarc import Field, Record


@pytest.fixture
def fake_subfields():
    return ["a", "subA", "x", "subX1", "x", "subX2", "z", "subZ."]


@pytest.fixture
def fake_subjects(fake_subfields):
    return [
        Field(tag="600", indicators=["1", "0"], subfields=fake_subfields),
        Field(tag="650", indicators=[" ", "7"], subfields=fake_subfields),
        Field(tag="650", indicators=[" ", "0"], subfields=fake_subfields),
        Field(tag="653", indicators=[" ", " "], subfields=fake_subfields),
    ]


@pytest.fixture
def stub_bib():
    record = Record()
    record.add_field(
        Field(tag="650", indicators=[" ", "0"], subfields=["a", "LCSH sub A."])
    )
    record.add_field(
        Field(
            tag="650",
            indicators=[" ", "7"],
            subfields=["a", "Unwanted FAST.", "2", "fast"],
        )
    )
    record.add_field(
        Field(
            tag="650",
            indicators=[" ", "7"],
            subfields=["a", "neutral FAST.", "2", "fast"],
        )
    )
    record.add_field(
        Field(tag="907", indicators=[" ", " "], subfields=["a", ".b111111111"])
    )
    return record
