# -*- coding: utf-8 -*-
"""
This module inclues methods for replacement of unwanted LCSHs in bibliographic records with local prefered terms
"""

import csv
import logging
from typing import List, Set

from pymarc import Record, Field


def flip_lcsh_fields(record: Record, lcsh4change: Set) -> None:
    """
    Finds pymarc.Field objects in a record with the unwanted LCSH term
    """
    lcsh_tags = lcsh_fields(record.subjects())
    n = 0
    for field in lcsh_tags:
        norm_subfields = normalize_subfields(field.subfields)
        for lcsh_term, local_term in lcsh4change:
            if lcsh_term.lower() in norm_subfields:
                n += 1
                field.subfields = replace_term(
                    field.subfields, norm_subfields.index(lcsh_term.lower()), local_term
                )
    logging.info(f"Replaced {n} LCSH(s) in the record.")


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
    old_value = subfields[position]
    logging.debug(f"Original LCSH term in position {position}: '{old_value}'.")
    lcsh_norm = old_value.replace(".", "")
    logging.debug(f"Normalized LCSH term: '{lcsh_norm}'.")
    new_value = old_value.replace(f"{lcsh_norm}", f"{local_term}")
    logging.debug(f"New replacement term: '{local_term}'")
    new_subfields = subfields[:]
    new_subfields[position] = new_value
    logging.debug(f"{subfields} => {new_subfields}")
    return new_subfields


def save2marc(marc_out: str, record: Record) -> None:
    """
    Saves passed in the argument record to a MARC file
    """
    with open(marc_out, "ab") as out:
        out.write(record.as_marc())
        logging.debug("Manipulated record saved.")
