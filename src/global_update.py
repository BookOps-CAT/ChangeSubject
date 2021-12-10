"""
This scripts globally updates BPL & NYPL records to convert local 
Change the Subject headings to LC terms or older local terms to new local terms.
In particular this script handles split of "undocumented" headings into two 
"Noncitizens" and "Undocumened immigration"
"""
import sys

from pymarc import MARCReader, Field, Record


from src.december_changes import ADOPTED


def change_term_source_coding(field):
    pass


def is_bookops_term(field: Field) -> bool:
    try:
        if field["2"] == "bookops":
            return True
        else:
            return False
    except KeyError:
        return False


def adopt_lc(bib: Record) -> None:
    """
    Changes local bookops subject fields into LC equivalent.
    Changes indicators coding and removes $2 with bookops
    """
    bibNo = bib["907"]["a"][1:]
    for term in ADOPTED:
        subjects = bib.subjects()
        for subject in subjects:
            # print(type(subject))
            if is_bookops_term(subject) and term in subject.value():
                print(f"Adopting LC term in field: {subject} ({bibNo})")
                bib.add_ordered_field(
                    Field(
                        tag=subject.tag,
                        indicators=[" ", "0"],
                        subfields=subject.subfields[:-2],
                    )
                )
                bib.remove_field(subject)


def save2marc(fh: str, record: Record) -> None:
    with open(fh, "ab") as marcfile:
        marcfile.write(record.as_marc())


def update(file_path: str):
    print(f"Processing file: {file_path}")
    out = f"{file_path[:-4]}-PROC.mrc"
    with open(file_path, "rb") as marcfile:
        reader = MARCReader(marcfile)
        for bib in reader:
            adopt_lc(bib)

            save2marc(out, bib)


if __name__ == "__main__":
    fh = sys.argv[1]
    update(fh)
