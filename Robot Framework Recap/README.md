# SauceDemo Robot Framework Automation

Keyword-driven test automation suite for [https://www.saucedemo.com/](https://www.saucedemo.com/) built with **Robot Framework** and **SeleniumLibrary**.

---

## Project Structure

```
saucedemo_rf_project/
├── tests/
│   ├── TC1_valid_login.robot               # Login with valid credentials
│   ├── TC2_invalid_login.robot             # Login with invalid credentials
│   ├── TC3_add_product_to_cart.robot       # Add single product to cart
│   └── TC4_checkout_multiple_products.robot # Add multiple products & checkout
├── resources/
│   ├── keywords.robot                      # Reusable keyword definitions
│   └── variables.robot                     # Centralized variables & locators
├── results/                                # Test execution reports (auto-generated)
├── requirements.txt                        # Python dependencies
└── README.md
```

---

## Test Cases

| # | Test Case | Description |
|---|-----------|-------------|
| TC1 | Valid Login | Login with `standard_user` / `secret_sauce` and verify Products page |
| TC2 | Invalid Login | Attempt login with wrong credentials and verify error message |
| TC3 | Add to Cart | Add a single product and verify it appears in the cart |
| TC4 | Checkout Summary | Add multiple products, proceed to checkout, verify order summary |

---

## Prerequisites

- Python 3.8+
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

---

## Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd saucedemo_rf_project

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Running Tests

```bash
# Run all test cases
robot --outputdir results tests/

# Run a specific test case
robot --outputdir results tests/TC1_valid_login.robot

# Run by tag
robot --outputdir results --include smoke tests/
robot --outputdir results --include login tests/
robot --outputdir results --include e2e tests/
```

---

## Viewing Reports

After execution, open the generated report in your browser:

```bash
# HTML report
open results/report.html

# Detailed log
open results/log.html
```

---

## Tags Reference

| Tag | Test Cases |
|-----|------------|
| `smoke` | TC1, TC3 |
| `login` | TC1, TC2 |
| `negative` | TC2 |
| `cart` | TC3, TC4 |
| `checkout` | TC4 |
| `e2e` | TC4 |

---

## Libraries Used

- **SeleniumLibrary** — Web browser interactions (click, input, navigate)
- **BuiltIn** — Standard Robot Framework operations (assertions, logging)
