# -*- coding: utf-8 -*-
"""
This module inclues methods for removal of FAST MARC tags based on a csv list of unwanted terms
"""

import csv
import logging
from typing import List, Set


from pymarc import MARCReader, Record, Field


def fast2list(src_fh: str) -> List[List]:
    """
    Assumes the csv file has a header, first column includes terms with subdivisions,
    second column may include control nubmer
    """
    fast_terms = []
    with open(src_fh, "r") as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        reader.__next__()

        for row in reader:
            fast_terms.append(row[0])
    return fast_terms


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


def fast4deletion(terms_for_deletion: List[str], record: Record) -> Set:
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
            if term.lower() in norm_field:
                fields_for_deletion.add(field)
    return fields_for_deletion


def remove_fast_terms(record: Record, terms_for_deletion: List[str]) -> None:
    """
    Deletes MARC fields with indicated FAST terms from the bib.
    """
    fields_for_deletion = fast4deletion(terms_for_deletion, record)
    fields_for_deletion = [field for field in fields_for_deletion]
    n = 0
    if fields_for_deletion:
        for f in fields_for_deletion:
            n += 1
            logging.debug(f"Removing tag: {f}")
            record.remove_field(f)
    logging.debug(f"Removed {n} tags with FAST term(s).")
