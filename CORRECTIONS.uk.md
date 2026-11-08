# CORRECTIONS.md — sheet2csv

Project: sledilnik/sheet2csv
Base branch analyzed: master
Destination fork: https://github.com/admeduardovieira/sheet2csv

## Corrections implemented

| ID | Title | Severity | Status | Risk | Files involved |
|----|-------|----------|--------|------|----------------|
| REA-sheet2csv-001 | setup.py empty (setup() with no arguments) | P3 | IMPLEMENTED | Low | `setup.py` |
| REA-sheet2csv-002 | __main__.py empty (no CLI entry point) | P3 | IMPLEMENTED | Low | `sheet2csv/__main__.py` |
| REA-sheet2csv-003 | test.yml uses actions/checkout@v6 (nonexistent) | P2 | IMPLEMENTED | Low | `.github/workflows/test.yml` |
| REA-sheet2csv-004 | requirements_dev.txt uses nose (deprecated) | P3 | IMPLEMENTED | Low | `requirements_dev.txt` |

## Details of implemented corrections

### REA-sheet2csv-001 — Empty setup.py
**Problem:** `setup.py` contained only `from setuptools import setup` followed by `setup()` with no arguments.
**Fix:** Added complete package metadata, version, author, description, long_description, URL, project_urls, classifiers, packages, python_requires, and install_requires with pinned versions.
**Validation:** `py_compile` passes.

### REA-sheet2csv-002 — Empty __main__.py
**Problem:** `sheet2csv/__main__.py` was empty (0 bytes), making `python -m sheet2csv` unusable.
**Fix:** Added CLI entry point that parses command-line arguments (SHEET_ID, RANGE, API_KEY, optional filename) and calls `sheet2csv()`.
**Validation:** `py_compile` passes.

### REA-sheet2csv-003 — Nonexistent GitHub Actions versions
**Problem:** `test.yml` used `actions/checkout@v6` and `actions/setup-python@v6`, which do not exist.
**Fix:** Changed to `actions/checkout@v4` and `actions/setup-python@v5`.
**Validation:** File syntax verified.

### REA-sheet2csv-004 — Deprecated nose in dev requirements
**Problem:** `requirements_dev.txt` listed `nose`, a deprecated/unmaintained test framework.
**Fix:** Replaced `nose` with `pytest`.
**Validation:** File content verified.

## Not implemented
None — all identified problems were implemented.

## Publication plan
- Fork: `admeduardovieira/sheet2csv` (created).
- Branch `fix/rea-sheet2csv-001-004` for all corrections.
- Commit identity: `admeduardovieira <admeduardovieira@users.noreply.github.com>`.
- PR #101: https://github.com/sledilnik/sheet2csv/pull/101 (open, base master).

Переклад технічний, виконаний автоматизовано; рекомендується перегляд носієм мови перед використанням якнормативного посилання.
