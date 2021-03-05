# -*- coding: utf-8 -*-

"""
Shared utilities
"""

import csv
from typing import List


def csv2list(src_fh: str) -> List[List]:
    """
    Assumes the csv file has a header, first column includes terms with subdivisions,
    second column may include control nubmer
    """

    with open(src_fh, "r") as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        reader.__next__()

        for row in reader:
            yield row[0]
