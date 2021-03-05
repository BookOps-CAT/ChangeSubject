# -*- coding: utf-8 -*-

"""
Makes requests to id.loc.gov for given authority record (LC control number) in a MARC XML format and converts it to MARC21
"""

import csv
from io import BytesIO
from typing import Iterator

import requests
from pymarc import MARCWriter, Record, XmlHandler, parse_xml


class AuthHandler(XmlHandler):
    """
    Subclass of pymarc's XmlHandler that deals with single record only.
    """

    def __init__(self, strict=False, normalize_form=None):

        super().__init__(strict, normalize_form)

    def process_record(self, record):
        self.records = record


def controlNos(fh: str) -> Iterator[str]:
    with open(fh, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row[0].replace(" ", "")


def make_request(session, controlNo):
    url = f"https://id.loc.gov/authorities/subjects/{controlNo}.marcxml.xml"
    response = session.get(url)
    print(f"{response.request.url} = {response.status_code}")
    if response.status_code == requests.codes.ok:
        return response


def xml2marc(response: bytes) -> Record:
    handler = AuthHandler()
    record = BytesIO(response)
    parse_xml(record, handler)
    return handler.records


def save2marc(fh: str, record: Record) -> None:
    with open(fh, "ab") as marcfile:
        marcfile.write(record.as_marc())


def run(fh_in: str, fh_out: str) -> None:
    with requests.Session() as session:
        for controlNo in controlNos(fh_in):
            response = make_request(session, controlNo)
            record = xml2marc(response.content)
            save2marc(fh_out, record)


if __name__ == "__main__":
    fh_in = "LCSHcontrolNos.csv"
    fh_out = "LCauths.mrc"
    run(fh_in, fh_out)
