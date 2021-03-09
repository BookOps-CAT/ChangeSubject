# -*- coding: utf-8 -*-

import pytest


from pymarc import Field


@pytest.fixture
def fake_subfields():
    return ["a", "subA", "x", "subX1", "x", "subX2", "z", "subZ."]
