# World Population Clock — Selenium POM Scraper

## Project Structure

```
world_population_scraper/
├── pages/
│   ├── __init__.py
│   └── world_population_page.py   # Page Object Model
├── conftest.py                    # Pytest fixtures (WebDriver setup)
├── test_world_population.py       # Pytest test cases
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.9+
- Google Chrome installed
- ChromeDriver matching your Chrome version on `PATH`
  (or install via `pip install webdriver-manager` and adjust `conftest.py`)

## Setup

```bash
pip install -r requirements.txt
```

## Running the Tests

### All tests + HTML report
```bash
pytest test_world_population.py -v --html=report.html --self-contained-html
```

### Continuous live-print test only (stops on CTRL+C)
```bash
pytest test_world_population.py::TestWorldPopulation::test_extract_population_continuously -v -s
```

> The `-s` flag is required to see `print()` output in the terminal.

## What Each Test Does

| Test | Description |
|------|-------------|
| `test_page_title_is_not_empty` | Verifies the page loads by checking the `<title>` |
| `test_population_count_is_numeric` | Extracts a single snapshot and validates it's a 10-digit number > 7 billion |
| `test_extract_population_continuously` | Prints the live count every second until **CTRL+C** |

## Notes

- All element locators use **XPATH only** (no CSS selectors, IDs, or Names).
- Explicit Waits (`WebDriverWait` + `ExpectedConditions`) are used throughout.
- The Page Object Model keeps locators and page interactions in one place.
