# sheet2csv

Python package to transform Google Sheet to CSV.

## Install
```
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

## Devlopment
git clone https://github.com/sledilnik/sheet2csv
cd sheet2csv
pipenv install
pipenv run pip install -e .
pipenv run test