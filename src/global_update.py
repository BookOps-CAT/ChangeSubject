"""
This scripts globally updates BPL & NYPL records to convert local 
Change the Subject headings to LC terms or older local terms to new local terms.
In particular this script handles split of "undocumented" headings into two 
"Noncitizens" and "Undocumened immigration"
"""
import sys

from pymarc import MARCReader, Field, Record


from december_changes import ADOPTED, SPLIT, CHANGED


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


def normalize_subfield(value):
    return value.replace(".", "")


def isolate_tail(field: Field) -> list:
    """
    Returns subfields following the main $a term
    """
    return field.subfields[2:-2]


def split_local(bib: Record) -> None:
    """
    Flips local terms that have been changed.
    """
    bibNo = bib["907"]["a"][1:]
    for old_term, new_term in SPLIT:
        subjects = bib.subjects()
        for subject in subjects:
            if is_bookops_term(subject) and old_term in subject["a"]:
                print(f"Spliting field {subject} ({bibNo})")
                tail = isolate_tail(subject)
                if not tail:
                    main_subs = ["a", f"{new_term}."]
                else:
                    main_subs = ["a", new_term]
                    main_subs.extend(tail)
                bib.add_ordered_field(
                    Field(
                        tag=subject.tag,
                        indicators=[" ", "0"],
                        subfields=main_subs,
                    )
                )
                if not tail:
                    extra_subs = ["a", "Undocumented immigration."]
                else:
                    extra_subs = ["a", "Undocumented immigration"]
                    extra_subs.extend(tail)
                extra_subs.extend(["2", "bookops"])
                bib.add_ordered_field(
                    Field(
                        tag="650",
                        indicators=[" ", "7"],
                        subfields=extra_subs,
                    )
                )
                bib.remove_field(subject)


def change_local(bib: Record) -> None:
    """
    Makes one to one local change
    """
    bibNo = bib["907"]["a"][1:]
    for old_term, new_term in CHANGED:
        subjects = bib.subjects()
        for subject in subjects:
            if is_bookops_term(subject) and old_term in subject["a"]:
                print(f"Changing local {subject} ({bibNo})")
                tail = isolate_tail(subject)
                if not tail:
                    subs = ["a", f"{new_term}.", "2", "bookops"]
                else:
                    subs = ["a", new_term]
                    subs.extend(tail)
                    subs.extend(["2", "bookops"])
                bib.add_ordered_field(
                    Field(tag=subject.tag, indicators=[" ", "7"], subfields=subs)
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
            split_local(bib)
            change_local(bib)

            save2marc(out, bib)


if __name__ == "__main__":
    fh = sys.argv[1]
    update(fh)
