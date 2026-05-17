# Zen Portal - Selenium Pytest Automation (Task 14)

## Project Structure

```
zen_portal_tests/
├── pages/
│   ├── __init__.py
│   ├── base_page.py        # Base class with Explicit Wait utilities
│   ├── login_page.py       # Login Page Object
│   └── dashboard_page.py   # Dashboard/Home Page Object (post-login)
├── tests/
│   ├── __init__.py
│   └── test_zen_portal.py  # All 17 test cases
├── reports/                # HTML reports generated here
├── conftest.py             # Pytest fixtures (WebDriver setup/teardown)
├── pytest.ini              # Pytest config (HTML report settings)
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your Credentials
Open `tests/test_zen_portal.py` and update:
```python
VALID_USERNAME = "your_email@example.com"   # ← Your Zen Portal email
VALID_PASSWORD = "your_password"            # ← Your Zen Portal password
```

### 3. Run Tests + Generate HTML Report
```bash
cd zen_portal_tests
pytest
```

The HTML report will be saved at: `reports/zen_portal_report.html`

### Run with extra verbosity
```bash
pytest -v
```

### Run a single test
```bash
pytest tests/test_zen_portal.py::TestZenPortalLogin::test_successful_login -v
```

---

## Test Cases Covered

| TC # | Category | Description |
|------|----------|-------------|
| TC_001 | Positive | Successful login with valid credentials |
| TC_002 | Negative | Login with invalid username & password |
| TC_003 | Negative | Login with invalid username, valid password |
| TC_004 | Negative | Login with valid username, invalid password |
| TC_005 | Negative | Login with both fields empty |
| TC_006 | Negative | Login with empty username |
| TC_007 | Negative | Login with empty password |
| TC_008 | Validation | Username input field is present |
| TC_009 | Validation | Password input field is present |
| TC_010 | Validation | Username field accepts text input |
| TC_011 | Validation | Password field accepts input (type=password) |
| TC_012 | Validation | Submit button is present |
| TC_013 | Validation | Submit button is enabled |
| TC_014 | Validation | Submit button triggers login |
| TC_015 | Logout | Logout button visible after login |
| TC_016 | Logout | Successful logout redirects to login page |
| TC_017 | Logout | Dashboard inaccessible after logout |

---

## Key Design Patterns Used

- **Page Object Model (POM)**: Each page is a separate class in `pages/`
- **Explicit Waits**: All interactions use `WebDriverWait` with `expected_conditions`
- **Python OOP**: Inheritance (`LoginPage → BasePage`, `DashboardPage → BasePage`)
- **Selenium Exception Handling**: `TimeoutException`, `NoSuchElementException`, `ElementNotInteractableException`
- **pytest-html**: Generates a self-contained HTML test report
