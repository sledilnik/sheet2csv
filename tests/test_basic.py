import os
import sheet2csv

SHEET_ID = "1hnjbVKdon5316fNGtnwzrRYH51fn6JjcOW2lUaKFqTI"
SHEET_ID_PROD = "1N1qLMoWyi3WFGhIpPFzKsFmVE0IwNP3elb_c18t2DwY"

API_KEY = os.environ["GOOGLE_API_KEY"]


def key_mapper_kraji(values):
    def clean(x):
        return x.lower().replace(" - ", "-").replace(" ", "_").split("/")[0]

    keys = list(
        map(
            lambda x: ".".join(["region", clean(x[0]), clean(x[1])]),
            zip(values[1][1:], values[0][1:]),
        )
    )
    keys.insert(0, "date")

    return keys, values[2:]


def test_fetch():
    values = sheet2csv.fetch_sheet(id=SHEET_ID, range="rows!A1:ZZ", api_key=API_KEY)
    assert type(values) is list


def test_sheet_rows():
    values = sheet2csv.sheet2dict(id=SHEET_ID, range="rows!A1:ZZ", api_key=API_KEY)


def test_sheet_rows_labels():
    values = sheet2csv.sheet2dict(
        id=SHEET_ID, range="rows_labels!A2:ZZ", api_key=API_KEY
    )


def test_sheet_cols():
    values = sheet2csv.sheet2dict(
        id=SHEET_ID, range="cols!A1:ZZ", api_key=API_KEY, rotate=True
    )


def test_sheet_cols_labels():
    values = sheet2csv.sheet2dict(
        id=SHEET_ID, range="cols_labels!C1:ZZ", api_key=API_KEY, rotate=True
    )


# def test_prod_podatki():
#   sheet2csv.sheet2csv(id=SHEET_ID_PROD, range='Podatki!A3:ZZ', api_key=API_KEY, filename='stats.csv')

# def test_prod_pacienti():
#   sheet2csv.sheet2csv(id=SHEET_ID_PROD, range='Pacienti!A3:ZZ', api_key=API_KEY, filename='patients.csv')

# def test_prod_kraji():
#   sheet2csv.sheet2csv(id=SHEET_ID_PROD, range='Kraji!A1:ZZ', api_key=API_KEY, rotate=True, key_mapper=key_mapper_kraji, filename='regions.csv')

# def test_prod_zdrsistem():
#   sheet2csv.sheet2csv(id=SHEET_ID_PROD, range='Zdr.sistem!A3:ZZ', api_key=API_KEY, filename='hospitals.csv')

# def test_schools():
#   sheet2csv.sheet2csv(id=SHEET_ID_PROD, range="Šole!A3:NN", api_key=API_KEY, filename='schools.csv')
