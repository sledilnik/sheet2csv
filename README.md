# sheet2csv

[![PyPI version](https://badge.fury.io/py/sheet2csv.svg)](https://badge.fury.io/py/sheet2csv)
[![Test](https://github.com/sledilnik/sheet2csv/actions/workflows/test.yml/badge.svg)](https://github.com/sledilnik/sheet2csv/actions/workflows/test.yml)

Python package to transform Google Sheet to CSV.

## Install

```sh
pip install sheet2csv
```

## Example

```python
import os

import sheet2csv

SHEET_ID = "PUT_ID_OF_SHEET_HERE"
RANGE_STATS = "SheetName!A3:ZZ"
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

# First row of range will be become header row of CSV
sheet2csv.sheet2csv(
    id=SHEET_ID, range=RANGE_STATS, api_key=GOOGLE_API_KEY, filename="export.csv",
)
```

## Development

```sh
git clone https://github.com/sledilnik/sheet2csv
cd sheet2csv
pipenv install
pipenv run pip install -e .
pipenv run test
```
