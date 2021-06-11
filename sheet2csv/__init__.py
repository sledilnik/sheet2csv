from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil import parser
import datetime
import csv
import os
import os.path
import sys

name = "sheet2csv/sheet2csv"
__version__ = "1.0.6"


class DuplicateColException(Exception):
    def __init__(self, col):
        message = "Duplicate column: {}".format(col)
        super().__init__(message)


class ParseDateException(Exception):
    def __init__(self, datestr):
        message = "Failed to parse date: {}".format(datestr)
        super().__init__(message)


def parse_date(datestr):
    if not datestr:
        return None
    try:
        return parser.isoparse(datestr[0:10]).date()
    except Exception as e:
        raise ParseDateException(datestr) from e


def serial2date(datestr):
    if not datestr:
        return None
    try:
        datestr = int(datestr)
        d = datetime.datetime(1899, 12, 30) + datetime.timedelta(days=datestr)
        return d.date()
    except Exception as e:
        raise ParseDateException(datestr) from e


def decimal2time(timedec):
    if timedec:
        sec = int(timedec * 86400)

        hours = int(sec / 3600)
        minutes = int((sec % 3600) / 60)
        seconds = sec % 60

        return datetime.time(hours, minutes, seconds)
    else:
        return None


def find_duplicates(l):
    # stupid but simple
    return set([x for x in l if l.count(x) > 1])


def fetch_sheet(id, range, api_key, majorDimension="ROWS"):

    service = build("sheets", "v4", developerKey=api_key)
    sheet = service.spreadsheets()

    result = (
        sheet.values()
        .get(
            spreadsheetId=id,
            range=range,
            valueRenderOption="UNFORMATTED_VALUE",
            majorDimension=majorDimension,
        )
        .execute()
    )
    values = result.get("values", [])
    if not values:
        raise Exception("No data in sheet")
    return values


def get_keys(key_mapper, values):

    if callable(key_mapper):
        return key_mapper(values)
    else:
        return values[0], values[1:]


def sheet2dict(id, range, api_key, rotate=False, key_mapper=None, sort_keys=False):

    if rotate:
        majorDimension = "COLUMNS"
    else:
        majorDimension = "ROWS"

    values = fetch_sheet(
        id=id, range=range, api_key=api_key, majorDimension=majorDimension
    )

    keys, data = get_keys(key_mapper, values)

    dicts = []

    for i, row in enumerate(data):
        if len(row) == 0 or len(str(row[0])) == 0:
            break
        x = dict(filter(lambda x: len(str(x[0])) > 0, zip(keys, row)))

        for k, v in x.items():
            if k.startswith("date"):
                try:
                    x[k] = serial2date(v)
                except ParseDateException as e:
                    print(
                        "Row {}: Failed to parse date in field {}: {}".format(i, k, v)
                    )
                    raise e
            if k.startswith("time"):
                try:
                    x[k] = decimal2time(v)
                except ParseDateException as e:
                    print(
                        "Row {}: Failed to parse time in field {}: {}".format(i, k, v)
                    )
                    raise e
        dicts.append(x)

    keys_sorted = list(filter(lambda val: len(str(val)) > 0, keys))
    if sort_keys:
        keys_sorted.sort()

    return keys_sorted, dicts


def sheet2csv(
    id,
    range,
    api_key,
    rotate=False,
    key_mapper=None,
    sort_keys=False,
    filename="export.csv",
):

    fieldnames, csvdata = sheet2dict(
        id=id,
        range=range,
        api_key=api_key,
        rotate=rotate,
        key_mapper=key_mapper,
        sort_keys=sort_keys,
    )

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csvdata)
