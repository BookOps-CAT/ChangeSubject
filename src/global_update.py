"""
This scripts globally updates BPL & NYPL records to convert local Change the Subject headings to
LC terms or older local terms to new local terms.
In particular this script handles split of "undocumented" headings into two "Noncitizens" and "Undocumened immigration"
"""
import sys

from pymarc import MARCReader


from .december_changes import ADOPTED


def change_term_source_coding(field):
    pass


def is_bookops_term(field):
    try:
        if field["2"] == "bookops":
            return True
        else:
            return False
    except KeyError:
        return False


def update_adopted_lc(bib):
    for term in ADOPTED:
        subjects = bib.subjects()
        for subject in subjects:
            # print(type(subject))
            if is_bookops_term(subject) and term[0] in subject.value():
                print(f"{term[0]} found: {subject}")


def update(file_path: str):
    print(f"Processing file: {file_path}")
    with open(file_path, "rb") as marcfile:
        reader = MARCReader(marcfile)
        for bib in reader:
            update_adopted_lc(bib)


if __name__ == "__main__":
    fh = sys.argv[1]
    update(fh)
