# -*- coding: utf-8 -*-
"""
This module inclues methods for replacement of unwanted LCSHs in bibliographic records with local prefered terms
"""

import csv
from typing import List, Set

from pymarc import MARCReader, Record, Field


def lcsh2list(lcsh_fh: str) -> List[Set]:
    lcsh4change = []
    with open(lcsh_fh, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lcsh4change.append((row[0], row[2]))
    return lcsh4change


def lcsh_fields(subject_fields: List[Field]) -> List[Field]:
    """
    Identifies fields that are codes as LCSH
    """
    lcsh_tags = []
    for tag in subject_fields:
        if tag.indicator2 == "0":
            lcsh_tags.append(tag)
    return lcsh_tags


def normalize_subfields(subfields: List[str]):
    return [s.lower().replace(".", "") for s in subfields]


def replace_term(subfields: List[str], position, local_term: str) -> List[str]:
    new_subfields = subfields[:]
    new_subfields[position] = local_term
    return new_subfields


def find_impacted_fields(record: Record, lcsh4change: List[str]) -> List[Field]:
    """
    Finds pymarc.Field objects in a record with the unwanted LCSH term
    """
    lcsh_tags = lcsh_fields(record.subjects())
    for field in lcsh_tags:
        norm_subfields = normalize_subfields(field.subfields)
        pos = 0
        for lcsh_term, local_term in lcsh4change:
            if lcsh_term.lower() in norm_subfields:
                field.subfields = replace_term(field, pos, local_term)
            pos += 1


def process_file(marc_fh, lcsh_fh):
    lcsh4change = lcsh2list(lcsh_fh)
    with open(marc_fh, "rb") as marcfile:
        reader = MARCReader(marcfile)
        n = 0
        for record in reader:
            n += 1
            print(f"Analyzing record #: {n}")
            find_impacted_fields(record, lcsh4change)


if __name__ == "__main__":
    marc_fh = "..\\files\\bpl-aliens.mrc"
    lcsh_fh = "..\\files\\lcsh4change.csv"
    process_file(marc_fh, lcsh_fh)
