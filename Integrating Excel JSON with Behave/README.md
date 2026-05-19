# Zen Portal BDD Automation — Task 18

Automated login/logout tests for the **Zen Portal** (GUVI) using:
- **Python BDD Behave Framework** (feature files + step definitions)
- **Page Object Model (POM)** design pattern
- **Allure Report Generation** (HTML + JSON)
- **Selenium WebDriver** with Python OOP & exception handling

---

## Project Structure

```
zen_portal_bdd/
├── features/
│   ├── login.feature          # BDD Gherkin scenarios
│   ├── environment.py         # Behave hooks (browser setup/teardown)
│   └── steps/
│       └── login_steps.py     # Step definitions
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # BasePage — shared Selenium utilities
│   └── login_page.py          # LoginPage — POM for login/logout
├── allure-results/            # Allure JSON output (auto-generated)
├── allure-report/             # Allure HTML output (after generate step)
├── behave.ini                 # Behave + Allure formatter config
└── requirements.txt
```

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.8+ |
| Google Chrome | Latest |
| ChromeDriver | Match Chrome version |
| Java (for Allure CLI) | 8+ |

---

## Setup

### 1. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Update credentials in the feature file
Open `features/login.feature` and replace the placeholders:
```gherkin
When I enter a valid username "<your_email@example.com>"
And I enter a valid password "<your_password>"
```

### 4. (Optional) Install Allure CLI
```bash
# macOS
brew install allure

# Windows (via Scoop)
scoop install allure

# Manual: https://allurereport.org/docs/gettingstarted-installation/
```

---

## Running Tests

### Run all scenarios (outputs Allure JSON results)
```bash
behave -f allure_behave.formatter:AllureFormatter -o allure-results
```

### Run by tag
```bash
# Only successful login tests
behave --tags=@successful_login -f allure_behave.formatter:AllureFormatter -o allure-results

# Only UI validation tests
behave --tags=@validate_ui -f allure_behave.formatter:AllureFormatter -o allure-results

# Only logout tests
behave --tags=@logout -f allure_behave.formatter:AllureFormatter -o allure-results
```

### Run in headless mode (CI)
Uncomment this line in `features/environment.py`:
```python
chrome_options.add_argument("--headless=new")
```

---

## Generating Allure Reports

### Generate HTML report from JSON results
```bash
allure generate allure-results --clean -o allure-report
```

### Open HTML report in browser
```bash
allure open allure-report
```

### Serve report live (generates + opens in one step)
```bash
allure serve allure-results
```

---

## Test Scenarios Covered

| # | Scenario | Tag |
|---|----------|-----|
| 1 | Validate Username & Password input fields | `@validate_ui` |
| 2 | Validate Submit button present | `@validate_ui` |
| 3 | Successful login with valid credentials | `@successful_login` |
| 4 | Unsuccessful login with invalid credentials | `@unsuccessful_login` |
| 5 | Logout after successful login | `@logout` |
| 6 | Validate Logout button visible after login | `@validate_ui` |

---

## Allure Report Features

- ✅ **HTML Report** — Visual, interactive test results
- ✅ **JSON Results** — Machine-readable output in `allure-results/`
- ✅ **Screenshots** — Auto-captured on every step & on failure
- ✅ **Step Descriptions** — Each `@allure.step` annotated method is logged
- ✅ **Attachments** — URL, status text, and failure details embedded

---

## Customising Locators

If the portal's HTML changes, update the locators in `pages/login_page.py`:

```python
USERNAME_INPUT  = (By.ID,    "email")
PASSWORD_INPUT  = (By.ID,    "password")
SUBMIT_BUTTON   = (By.XPATH, "//button[@type='submit']")
LOGOUT_BUTTON   = (By.XPATH, "//a[contains(text(),'Logout')]")
```

Use Chrome DevTools (`F12 → Elements`) to inspect and update selectors.
