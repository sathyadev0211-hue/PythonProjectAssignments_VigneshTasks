# Zen Portal Automation – Task 17

Playwright + Pytest automation suite for the **Guvi Zen Portal** login/logout flow.

---

## Project Structure

```
zen_portal_automation/
├── pages/
│   ├── __init__.py
│   ├── base_page.py        ← BasePage (explicit wait helpers)
│   ├── login_page.py       ← LoginPage POM
│   └── dashboard_page.py   ← DashboardPage POM
├── tests/
│   ├── __init__.py
│   └── test_zen_portal.py  ← All 12 test cases
├── reports/                ← Auto-created; HTML report lands here
├── conftest.py             ← Pytest fixtures (browser / context / page)
├── pytest.ini              ← Pytest settings + HTML report config
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Playwright browsers
playwright install chromium
```

---

## Add Your Credentials

Open `tests/test_zen_portal.py` and update the two constants at the top:

```python
VALID_USERNAME = "your_registered_email@example.com"
VALID_PASSWORD = "your_password"
```

> ⚠️ **Remove credentials before pushing to GitHub.**

---

## Run Tests

```bash
# Run all tests and generate the HTML report
pytest

# The report is saved to:  reports/test_report.html
```

---

## Test Cases

| ID    | Class                      | Description                                  |
|-------|----------------------------|----------------------------------------------|
| TC-01 | TestSuccessfulLogin        | Valid credentials → dashboard loads          |
| TC-02 | TestUnsuccessfulLogin      | Invalid credentials → error shown            |
| TC-03 | TestUnsuccessfulLogin      | Empty credentials → stays on login page      |
| TC-04 | TestInputBoxValidation     | Username input is visible                    |
| TC-05 | TestInputBoxValidation     | Password input is visible                    |
| TC-06 | TestInputBoxValidation     | Username input accepts typed text            |
| TC-07 | TestInputBoxValidation     | Password input accepts typed text            |
| TC-08 | TestSubmitButtonValidation | Submit button is visible                     |
| TC-09 | TestSubmitButtonValidation | Submit button is enabled                     |
| TC-10 | TestSubmitButtonValidation | Submit button triggers a page action         |
| TC-11 | TestLogoutFunctionality    | Logout button visible after login            |
| TC-12 | TestLogoutFunctionality    | Logout redirects back to login/home page     |

---

## Key Design Decisions

- **Page Object Model (POM)** – Each page is a class; tests only call high-level methods.
- **Explicit Waits** – `wait_for_selector` / `wait_for_load_state` used everywhere; no `time.sleep`.
- **Python OOP** – `BasePage` parent class with shared helpers; `LoginPage` and `DashboardPage` inherit from it.
- **Exception Handling** – `PlaywrightTimeoutError` caught in every test for clean failure messages.
- **HTML Report** – Generated automatically by `pytest-html` into `reports/test_report.html`.
