from sheet2csv import sheet2csv
import os
import sys

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python -m sheet2csv <SHEET_ID> <RANGE> <API_KEY> [filename]")
        sys.exit(1)
    sheet_id = sys.argv[1]
    sheet_range = sys.argv[2]
    api_key = sys.argv[3]
    filename = sys.argv[4] if len(sys.argv) > 4 else "export.csv"
    sheet2csv(id=sheet_id, range=sheet_range, api_key=api_key, filename=filename)
    print(f"Exported to {filename}")
