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

name="sheet2csv/sheet2csv"
__version__ = "1.0.0"

class DuplicateColException(Exception):
    def __init__(self, col):
        message = "Duplicate column: {}".format(col)
        super().__init__(message)

class ParseDateException(Exception):
    def __init__(self, datestr):
        message = "Failed to parse date: {}".format(datestr)
        super().__init__(message)


def parse_date(datestr):
    try:
        return parser.isoparse(datestr[0:10]).date()
    except Exception as e:
        raise ParseDateException(datestr) from e

def serial2date(datestr):
    try:
        datestr = int(datestr)
        d = datetime.datetime(1899, 12, 30)+datetime.timedelta(days=datestr)
        return d.date()
    except Exception as e:
        raise ParseDateException(datestr) from e

def find_duplicates(l):
    # stupid but simple
    return set([x for x in l if l.count(x) > 1])


def fetch_sheet(id, range, api_key, majorDimension='ROWS'):

    service = build("sheets", "v4", developerKey=api_key)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=id, range=range, valueRenderOption='UNFORMATTED_VALUE', majorDimension=majorDimension).execute()
    values = result.get("values", [])
    if not values:
        raise Exception("No data in sheet")
    return values

def get_keys(key_mapper, values):

    if callable(key_mapper):
        return key_mapper(values)
    else:
        return values[0], values[1:]

def sheet2dict(id, range, api_key, rotate=False, key_mapper=None):

    if rotate:
        majorDimension = 'COLUMNS'
    else:
        majorDimension = 'ROWS'
        
        
    values = fetch_sheet(id=id, range=range, api_key=api_key, majorDimension=majorDimension)

    keys, data = get_keys(key_mapper, values)

    dicts = []

    for row in data:
        if len(row) == 0 or len(str(row[0])) == 0:
            break
        x = dict(filter(lambda x: len(str(x[0])) > 0, zip(keys, row)))
        if 'date' in x:
            try:
                x['date'] = serial2date(x['date'])
            except ParseDateException as e:
                print("Faield to parse date", x)
                raise e
        dicts.append(x)

    return list(filter(lambda val: len(str(val)) > 0, keys)), dicts

def sheet2csv2(id, range, api_key, rotate=False, key_mapper=None, filename="export.csv"):

    fieldnames, csvdata = sheet2dict(id, range, api_key, rotate, key_mapper)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csvdata)


def sheet2csv_rotate(id, range, api_key, key_prefix="", key_cols=[1], filename="export.csv"):

    service = build("sheets", "v4", developerKey=api_key)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=id, range=range, valueRenderOption='UNFORMATTED_VALUE').execute()
    values = result.get("values", [])

    if not values:
        raise Exception("No data found.")

    key_set = set()

    def row2key(row):
        key_parts = []
        if key_prefix:
            key_parts.append(key_prefix)

        for idx in key_cols:
            town = row[idx].lower().replace(" - ", "-").replace(" ", "_").split('/')[0]
            key_parts.append(town)
        
        return '.'.join(key_parts)

    # fetch all fields
    try:
        for row in values:
            key_set.add(row2key(row))
    except IndexError as e:
        print("Failed to convert row {} to key", row)
        raise e

    keys = list(key_set)
    keys.sort()

    # find which date in which column
    dates = {}
    for idx, col in enumerate(values[0]):
        try:
            date = serial2date(col)
            dates[idx] = date
        except ParseDateException:
            pass

    csvdata = []

    for idx, date in dates.items():
        dateline = {
            'date': date,
        }
        for row in values[1:]:
            key = row2key(row)
            try:
                dateline[key] = row[idx]
            except IndexError:
                dateline[key] = None
        csvdata.append(dateline)

    fieldnames = ['date'] + keys

    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        writer.writerows(csvdata)


def sheet2csv(id, range, api_key, filename="export.csv"):
    # api_key = os.environ["GOOGLE_API_KEY"]

    service = build("sheets", "v4", developerKey=api_key)
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=id, range=range, valueRenderOption='UNFORMATTED_VALUE').execute()
    values = result.get("values", [])

    if not values:
        raise Exception("No data found.")

    headers = values[0]

    cols = []
    col_map = {}

    for col_idx, col_name in enumerate(headers):
        if col_name:
            cols.append(col_name)
            col_map[col_name] = col_idx

    if len(cols) > len(set(cols)):
        dupe_cols = find_duplicates(cols)
        raise DuplicateColException(dupe_cols)

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(cols)

        for row in values[1:]:

            # pad each row with empty values
            row += [""] * (len(cols) - len(row))

            if len(str(row[0])) == 0:
                break

            csvrow = []
            for col in cols:
                idx = col_map[col]
                try:
                    if col == "date":
                        cell = serial2date(row[idx])
                    else:
                        cell = row[idx]
                except IndexError:
                    cell = None
                except ValueError as e:
                    print(row)
                    raise e

                csvrow.append(cell)
            writer.writerow(csvrow)

