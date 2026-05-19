# Robot Framework - Login Test Automation
### Application Under Test: [robotsparebinindustries.com](https://robotsparebinindustries.com)

---

## Project Structure

```
robot_framework_project/
│
├── tests/
│   └── login_tests.robot       # Test suite: login test cases
│
├── resources/
│   └── keywords.robot          # Reusable keywords + variables
│
├── results/                    # Test execution output (auto-generated)
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## Prerequisites

- Python 3.8+
- Google Chrome browser installed
- ChromeDriver matching your Chrome version (or use `webdriver-manager`)

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd robot_framework_project
```

### 2. Create and activate a virtual environment (recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Tests

### Run all tests and save results to `results/`
```bash
robot --outputdir results tests/login_tests.robot
```

### Run with a specific tag
```bash
robot --outputdir results --include smoke tests/login_tests.robot
```

### Run with headless Chrome (CI/CD environments)
```bash
robot --outputdir results -v BROWSER:headlesschrome tests/login_tests.robot
```

---

## Test Cases

| ID       | Test Case Name                   | Description                                      | Tags         |
|----------|----------------------------------|--------------------------------------------------|--------------|
| TC_001   | Valid User Login And Logout      | Login with valid credentials, verify success, logout | login, smoke |

---

## Keywords

| Keyword                                  | Description                                                  |
|------------------------------------------|--------------------------------------------------------------|
| `Open Browser And Navigate To Application` | Opens Chrome and loads the application URL                |
| `Login To Application`                   | Inputs credentials and submits the login form                |
| `Verify Login Is Successful`             | Asserts the logout button is visible post-login              |
| `Logout From Application`                | Clicks logout and confirms return to the login page          |
| `Close Browser Session`                  | Closes all open browser windows                              |

---

## Libraries Used

- **SeleniumLibrary** — Browser/UI interactions (clicks, input, assertions)
- **BuiltIn** — Standard Robot Framework operations (Log, etc.) — included by default
