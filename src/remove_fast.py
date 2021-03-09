# -*- coding: utf-8 -*-
"""
This module inclues methods for removal of FAST MARC tags based on a csv list of unwanted terms
"""

from typing import List


from pymarc import MARCReader, Record, Field


from utils import csv2list


def normalize_field(field: Field) -> str:
    """
    Normalizes value of a MARC field
    """
    norm_field = field.value().lower()
    norm_field = norm_field.replace(".", "")
    return norm_field


def fast_subjects(fields: List[Field]) -> List[Field]:
    fast_fields = []
    for field in fields:
        try:
            if "fast" in field["2"].lower():
                fast_fields.append(field)
        except AttributeError:
            pass
    return fast_fields


def fast4deletion(terms_for_deletion: List[str], record: Record) -> List[Field]:
    """
    Based on a list of FAST terms identifies MARC fields that one of them can be found.

    Returns:
            list of pymarc.Field objects
    """
    fields_for_deletion = set()
    fast_fields = fast_subjects(record.subjects())
    for field in fast_fields:
        norm_field = normalize_field(field)
        for term in terms_for_deletion:
            if term in norm_field:
                fields_for_deletion.add(field)
    return fields_for_deletion


def remove_terms(terms_for_deletion: List[str], record: Record) -> None:
    """
    Deletes MARC fields with indicated FAST terms from the bib.
    """
    fields_for_deletion = fast4deletion(terms_for_deletion, record)
    fields_for_deletion = [field for field in fields_for_deletion]
    if fields_for_deletion:
        for f in fields_for_deletion:
            record.remove_field(f)


if __name__ == "__main__":
    fast_fh = "..\\files\\fast4deletion.csv"
    marc_file = "..\\files\\bpl-aliens.mrc"
    terms_for_deletion = [term.lower() for term in csv2list(fast_fh)]
    with open(marc_file, "rb") as file:
        reader = MARCReader(file)
        n = 0
        for record in reader:
            n += 1
            print(f"analyzing record {n}")
            remove_terms(terms_for_deletion, record)
            # print(record)
            # print()
