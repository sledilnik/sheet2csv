# sheet2csv

Python package to transform Google Sheet to CSV.

## Install
```
pip install git+https://github.com/slo-covid-19/sheet2csv.git
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