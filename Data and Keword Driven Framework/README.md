# OrangeHRM Login Automation — DDTF + POM + Explicit Wait + Pytest

## Project Structure

```
orangehrm_ddtf/
├── conftest.py             # Pytest fixtures (WebDriver setup/teardown)
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Python dependencies
├── test_data.xlsx          # Excel file with test data + results (DDTF)
│
├── pages/
│   ├── __init__.py
│   └── login_page.py       # Page Object Model for OrangeHRM Login Page
│
├── tests/
│   ├── __init__.py
│   └── test_login.py       # Main test file (parametrized with Excel data)
│
├── utils/
│   ├── __init__.py
│   └── excel_utils.py      # Read/write Excel helpers
│
└── reports/
    └── report.html         # Auto-generated Pytest HTML report (after run)
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Ensure ChromeDriver matches your Chrome version and is in PATH
#    Download: https://chromedriver.chromium.org/downloads
```

## Run Tests

```bash
# Run all login tests (HTML report auto-generated in reports/)
pytest

# Run with explicit verbose output
pytest -v

# Run only passing-credential tests
pytest -m login -v
```

## Excel File (test_data.xlsx)

| Column        | Description                          |
|---------------|--------------------------------------|
| Test ID       | Unique test case identifier          |
| Username      | Login username to test               |
| Password      | Login password to test               |
| Date          | Date of test execution               |
| Time of Test  | Time of test execution               |
| Name of Tester| Tester name                          |
| Test Result   | Auto-filled: **Passed** or **Failed**|

## Framework Notes

- **No `sleep()`** — Explicit Wait (`WebDriverWait` + `expected_conditions`) used throughout
- **DDTF** — 5 username/password combinations driven from Excel
- **POM** — `LoginPage` class separates page logic from test logic
- **Pytest HTML** — `reports/report.html` generated after each run
