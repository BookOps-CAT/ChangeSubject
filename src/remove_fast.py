# -*- coding: utf-8 -*-
from typing import List


from pymarc import MARCReader, Record


from utils import csv2list


# def


def remove_terms(terms_for_deletion: List[str], bib: Record) -> Record:
    subjects = bib.subjects()
    for s in subjects:
        print(type(s), s)


if __name__ == "__main__":
    fast_fh = "FAST-alien-terms.csv"
    marc_file = "..\\files\\bpl-aliens.mrc"
    terms_for_deletion = csv2list(fast_fh)
    with open(marc_file, "rb") as file:
        reader = MARCReader(file)
        for bib in reader:
            remove_terms(terms_for_deletion, bib)
            break
