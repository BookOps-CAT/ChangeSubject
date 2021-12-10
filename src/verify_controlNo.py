from io import BytesIO
import csv

import requests
from pymarc import Record, XmlHandler, parse_xml


class AuthHandler(XmlHandler):
    """
    Subclass of pymarc's XmlHandler that deals with single record only.
    """

    def __init__(self, strict=False, normalize_form=None):

        super().__init__(strict, normalize_form)

    def process_record(self, record):
        self.records = record


def xml2marc(response: bytes) -> Record:
    handler = AuthHandler()
    record = BytesIO(response)
    parse_xml(record, handler)
    return handler.records


def make_request(session: requests.Session, controlNo: str) -> requests.Response:
    url = f"https://id.loc.gov/authorities/subjects/{controlNo}.marcxml.xml"
    response = session.get(url)
    print(f"{response.request.url} = {response.status_code}")
    if response.status_code == requests.codes.ok:
        return response


def verify(src_fh):
    with open(src_fh, "r") as csvfile:
        reader = csv.reader(csvfile)
        with requests.Session() as session:
            session.headers.update({"User-Agent": "tomaszkalata@bookops.org"})
            n = 0
            for row in reader:
                n += 1
                local_term = row[0]
                local_controlNo = row[1].replace(" ", "")
                response = make_request(session, local_controlNo)
                record = xml2marc(response.content)
                try:
                    lc_term = record["150"].value()
                except AttributeError:
                    lc_term = record["151"].value()
                if local_term != lc_term:
                    print(local_controlNo, local_term)
                    print(record)

                # if n >= 3:
                #     break


if __name__ == "__main__":
    src_fh = "LCterm-controlNo-old-ref.csv"
    verify(src_fh)
