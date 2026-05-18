# GUVI Login Automation — Selenium + Pytest

Automates and validates the GUVI portal login flow using **Python Selenium**, **Pytest**, and generates an **HTML test report**.

---

## Project Structure

```
├── test_guvi_login.py   # All test cases (positive + negative)
├── conftest.py          # Pytest config + HTML report metadata
├── requirements.txt     # Python dependencies
└── README.md
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your credentials
Open `test_guvi_login.py` and replace the placeholders near the top:
```python
VALID_EMAIL    = "your_email@example.com"
VALID_PASSWORD = "your_password"
```

> **Important:** Remove credentials before pushing to GitHub.

---

## Run Tests + Generate HTML Report

```bash
pytest test_guvi_login.py -v --html=report.html --self-contained-html
```

Open `report.html` in any browser to view the full test report.

---

## Test Cases

| # | Class | Test Name | Type |
|---|-------|-----------|------|
| 1 | Positive | `test_visit_guvi_homepage` | Positive |
| 2 | Positive | `test_login_button_navigates_to_signin_url` | Positive |
| 3 | Positive | `test_signin_page_url_is_correct` | Positive |
| 4 | Positive | `test_username_field_visible_and_enabled` | Positive |
| 5 | Positive | `test_password_field_visible_and_enabled` | Positive |
| 6 | Positive | `test_submit_button_visible_and_clickable` | Positive |
| 7 | Positive | `test_successful_login_with_valid_credentials` | Positive |
| 8 | Negative | `test_login_with_invalid_email_and_password` | Negative |
| 9 | Negative | `test_login_with_empty_email` | Negative |
| 10 | Negative | `test_login_with_empty_password` | Negative |
| 11 | Negative | `test_login_with_invalid_email_format` | Negative |
| 12 | Negative | `test_signin_url_is_not_wrong_url` | Negative |

---

## Notes

- Chrome browser is required; `webdriver-manager` auto-downloads the matching ChromeDriver.
- To run headlessly, uncomment `chrome_options.add_argument("--headless")` in the fixture.
- The browser is opened once per module and closed after all tests complete.
