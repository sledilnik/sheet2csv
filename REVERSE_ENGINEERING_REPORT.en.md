# REVERSE_ENGINEERING_REPORT — sheet2csv

## A. General diagnosis

### Architecture identified
Python library for exporting data from Google Sheets to CSV via Google Sheets v4 API. Simple architecture:

- `sheet2csv/__init__.py`: main module with functions `fetch_sheet()`, `sheet2dict()`, `sheet2csv()`, `parse_date()`, `serial2date()`, `decimal2time()`, `find_duplicates()`
- `sheet2csv/__main__.py`: CLI entry point (was empty before the fix)
- `setup.py`: packaging file (was empty before the fix)
- `setup.cfg`: package metadata (name, version, dependencies, classifiers)
- `requirements_dev.txt`: development dependencies (nose, black, ipython)
- `tests/test_basic.py`: tests requiring `GOOGLE_API_KEY` from environment
- `.github/workflows/test.yml`: CI running tests on push/PR to master
- `.gitignore`: standard Python template

### Technologies and dependencies
- Python >=3.6
- Runtime dependencies: google-api-python-client, google-auth-httplib2, google-auth-oauthlib, python-dateutil
- Dev dependencies: nose (deprecated), black, ipython
- Package published on PyPI (version 1.0.7)

### Maintenance state
Active recent commits. Repository: https://github.com/sledilnik/sheet2csv. Default branch: master.

### Existing testing mechanisms
`tests/test_basic.py` with 4 active tests (test_fetch, test_sheet_rows, test_sheet_rows_labels, test_sheet_cols, test_sheet_cols_labels). All require `GOOGLE_API_KEY` from environment. Cannot be executed without a valid key.

### Investigation limitations
- Tests cannot be executed without GOOGLE_API_KEY
- No sample data included in repository

## B. Problems found

| ID | Title | Severity | Status | Location |
|----|-------|----------|--------|----------|
| REA-sheet2csv-001 | setup.py empty (setup() with no arguments) | P3 | CONFIRMED | `setup.py` |
| REA-sheet2csv-002 | __main__.py empty (no CLI) | P3 | CONFIRMED | `sheet2csv/__main__.py` |
| REA-sheet2csv-003 | test.yml uses actions/checkout@v6 (nonexistent) | P2 | CONFIRMED | `.github/workflows/test.yml:20` |
| REA-sheet2csv-004 | requirements_dev.txt uses nose (deprecated) | P3 | CONFIRMED | `requirements_dev.txt` |

### Details of confirmed problems

**REA-sheet2csv-001 (P3, CONFIRMED)**: `setup.py` contains only `from setuptools import setup` followed by `setup()` with no arguments. This means the package has no metadata, version, dependencies, or entry points defined in setup.py (they are only in setup.cfg).

Evidence: `setup.py` has only 2 lines.

**REA-sheet2csv-002 (P3, CONFIRMED)**: `sheet2csv/__main__.py` is empty (0 bytes). It is not possible to run `python -m sheet2csv` as CLI.

Evidence: `__main__.py` has 0 lines of content.

**REA-sheet2csv-003 (P2, CONFIRMED)**: `.github/workflows/test.yml:20` uses `actions/checkout@v6` and `actions/setup-python@v6`, which do not exist (current maximum is checkout@v4 and setup-python@v5). CI would fail when trying to execute.

Evidence: `test.yml` lines 20-24.

**REA-sheet2csv-004 (P3, CONFIRMED)**: `requirements_dev.txt` lists `nose`, a deprecated and unmaintained test library.

Evidence: `requirements_dev.txt` line 1.

## C. Recurring problems
No recurring public issues found.

## D. Undocumented errors
All items in section B are problems not previously documented.

## E. Performance
No performance-sensitive operations (sheet data export via API).

## F. Technical improvements
- Fill setup.py with complete metadata (REA-sheet2csv-001, implemented)
- Add CLI to __main__.py (REA-sheet2csv-002, implemented)
- Fix GitHub Actions versions in test.yml (REA-sheet2csv-003, implemented)
- Replace nose with pytest in requirements_dev.txt (REA-sheet2csv-004, implemented)

## G. Execution plan
All corrections are independent and low risk, implemented in a single PR.

## H. Expected outcome
Correctly packaged Python package, functional CLI, executable CI, updated dev dependencies.

**Tools used:** git, gh, PowerShell, Python 3.12 (py_compile), static code inspection.  
**Limitation:** Tests not executed (require GOOGLE_API_KEY).  
**Environment:** Windows, PowerShell 5.1, `C:\Users\User\audit-repos\sheet2csv` (clone of upstream, branch master).
