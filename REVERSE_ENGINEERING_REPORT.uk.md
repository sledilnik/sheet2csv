# REVERSE_ENGINEERING_REPORT — sheet2csv

## A. Загальний діагноз

### Виявлена архітектура
Бібліотека Python для експорту даних з Google Sheets до CSV через API Google Sheets v4. Проста архітектура:

- `sheet2csv/__init__.py`: головний модуль з функціями `fetch_sheet()`, `sheet2dict()`, `sheet2csv()`, `parse_date()`, `serial2date()`, `decimal2time()`, `find_duplicates()`
- `sheet2csv/__main__.py`: точка входу CLI (був порожнім до виправлення)
- `setup.py`: файл упаковки (був порожнім до виправлення)
- `setup.cfg`: метадані пакету (ім'я, версія, залежності, класифікатори)
- `requirements_dev.txt`: залежності розробки (nose, black, ipython)
- `tests/test_basic.py`: тести, що потребують `GOOGLE_API_KEY` з оточення
- `.github/workflows/test.yml`: CI, що запускає тести при push/PR до master
- `.gitignore`: стандартний шаблон Python

### Технології та залежності
- Python >=3.6
- Залежності виконання: google-api-python-client, google-auth-httplib2, google-auth-oauthlib, python-dateutil
- Залежності розробки: nose (застаріле), black, ipython
- Пакет опубліковано на PyPI (версія 1.0.7)

### Стан підтримки
Активні нещодні коміти. Репозиторій: https://github.com/sledilnik/sheet2csv. Гałтьова гілка: master.

### Існуючі механізми тестування
`tests/test_basic.py` з 4 активними тестами (test_fetch, test_sheet_rows, test_sheet_rows_labels, test_sheet_cols, test_sheet_cols_labels). Усі потребують `GOOGLE_API_KEY` з оточення. Не може бути виконано без дійсного ключа.

### Обмеження дослідження
- Тести не можуть бути виконані без GOOGLE_API_KEY
- Немає прикладових даних у репозиторії

## B. Виявлені проблеми

| ID | Заголовок | Severity | Статус | Локація |
|----|-----------|----------|--------|----------|
| REA-sheet2csv-001 | setup.py порожній (setup() без аргументів) | P3 | CONFIRMED | `setup.py` |
| REA-sheet2csv-002 | __main__.py порожній (без CLI) | P3 | CONFIRMED | `sheet2csv/__main__.py` |
| REA-sheet2csv-003 | test.yml використовує actions/checkout@v6 (неіснуючий) | P2 | CONFIRMED | `.github/workflows/test.yml:20` |
| REA-sheet2csv-004 | requirements_dev.txt використовує nose (застаріле) | P3 | CONFIRMED | `requirements_dev.txt` |

### Деталі підтверджених проблем

**REA-sheet2csv-001 (P3, CONFIRMED)**: `setup.py` містить лише `from setuptools import setup` та `setup()` без аргументів. Це означає, що пакет не має метаданих, версії, залежностей та точок входу, визначених у setup.py (вони є лише у setup.cfg).

Довід: `setup.py` має лише 2 рядки.

**REA-sheet2csv-002 (P3, CONFIRMED)**: `sheet2csv/__main__.py` порожній (0 байт). Не можливо запустити `python -m sheet2csv` як CLI.

Довід: `__main__.py` має 0 рядків вмісту.

**REA-sheet2csv-003 (P2, CONFIRMED)**: `.github/workflows/test.yml:20` використовує `actions/checkout@v6` та `actions/setup-python@v6`, яких не існує (поточний максимум — checkout@v4 та setup-python@v5). CI не вдасться при спробі виконання.

Довід: `test.yml` рядки 20-24.

**REA-sheet2csv-004 (P3, CONFIRMED)**: `requirements_dev.txt` містить `nose`, застарілу та непідтримувану бібліотеку тестів.

Довід: `requirements_dev.txt` рядок 1.

## C. Повторювані проблеми
Повторювалися публічні проблеми не знайдено.

## D. Недокументовані помилки
Усі пункти розділу B — це проблеми, що раніше не були задокументовано.

## E. Продуктивність
Немає операцій, чутливих до продуктивності (експорт даних таблиці через API).

## F. Технічні вдосконалення
- Заповнити setup.py повними метаданими (REA-sheet2csv-001, реалізовано)
- Додати CLI до __main__.py (REA-sheet2csv-002, реалізовано)
- Виправити версії GitHub Actions у test.yml (REA-sheet2csv-003, реалізовано)
- Замінити nose на pytest у requirements_dev.txt (REA-sheet2csv-004, реалізовано)

## G. План виконання
Усі правки є незалежними та низькоризичними, реалізовані в одному PR.

## H. Очікуваний результат
Правильно упакований пакет Python, функціональний CLI, виконуваний CI, оновлені залежності розробки.

**Інструменти:** git, gh, PowerShell, Python 3.12 (py_compile), статичний аналіз коду.  
**Обмеження:** Тести не виконані (потребують GOOGLE_API_KEY).  
**Середовище:** Windows, PowerShell 5.1, `C:\Users\User\audit-repos\sheet2csv` (клон upstream, гілка master).

Переклад технічний, виконаний автоматизовано; рекомендується перегляд носієм мови перед використанням якнормативного посилання.
