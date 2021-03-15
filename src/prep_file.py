# -*- coding: utf-8 -*-

import logging

from pymarc import MARCReader

from remove_fast import fast2list, remove_fast_terms
from replace_lcsh import flip_lcsh_fields, lcsh2list, save2marc


def run_manipulation(marc_src: str, fast_fh: str, lcsh_fh: str) -> None:
    """
    A wrapper function that combines removal of indicated FAST MARC tags
    and replacement of unwanted LCSH terms.

    Args:
        marc_src:       path to a MARC file to be processed
        fast_fh:        path to a list of FAST terms to be deleted
        lcsh_fh:        path to a list of LCSH terms and their local
                            equivalents for replacement
    """
    # setup logging
    logging.basicConfig(
        filename="../files/processing.log",
        filemode="w",
        level=logging.DEBUG,
    )

    logging.info("Init.Begining manipulation.")
    fast_terms_for_deletion = fast2list(fast_fh)
    logging.info(
        f"Init. List of FAST terms for removal includes {len(fast_terms_for_deletion)} entries."
    )
    lcsh_for_change = lcsh2list(lcsh_fh)
    logging.info(
        f"Init. List of LCSH terms for change inclues {len(lcsh_for_change)} entries."
    )
    with open(marc_src, "rb") as marcfile:
        reader = MARCReader(marcfile)
        n = 0
        for record in reader:
            n += 1
            logging.info(f"Processing record #: {n}")
            flip_lcsh_fields(record, lcsh_for_change)
            remove_fast_terms(record, fast_terms_for_deletion)
            marc_out = f"{marc_src[:-4]}-CHANGED.mrc"
            save2marc(marc_out, record)


if __name__ == "__main__":
    marc = "../files/bpl-aliens.mrc"
    fast = "../files/fast4deletion.csv"
    lcsh = "../files/lcsh4change.csv"
    run_manipulation(marc, fast, lcsh)
