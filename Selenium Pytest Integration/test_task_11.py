"""
test_task_11.py
---------------
Pytest-based positive and negative test cases for the saucedemo automation.

Run with HTML report:
    pytest test_task_11.py --html=report.html --self-contained-html -v
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# --------------------------------------------------------------------------- #
#  Constants
# --------------------------------------------------------------------------- #
BASE_URL              = "https://www.saucedemo.com/"
VALID_USERNAME        = "standard_user"
VALID_PASSWORD        = "secret_sauce"
INVALID_USERNAME      = "wrong_user"
INVALID_PASSWORD      = "wrong_pass"
EXPECTED_HOME_TITLE   = "Swag Labs"
EXPECTED_HOME_URL     = "https://www.saucedemo.com/"
EXPECTED_DASH_URL     = "https://www.saucedemo.com/inventory.html"


# --------------------------------------------------------------------------- #
#  Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="function")
def driver():
    """Provide a headless Chrome driver; quit after each test."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


# --------------------------------------------------------------------------- #
#  Helper
# --------------------------------------------------------------------------- #
def do_login(driver, username: str, password: str) -> None:
    """Navigate to base URL and attempt a login."""
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# =========================================================================== #
#  1.  TITLE OF THE WEB APPLICATION
# =========================================================================== #

class TestAppTitle:
    """Test cases for the title of the web application."""

    # ---- Positive --------------------------------------------------------- #
    def test_title_positive(self, driver):
        """
        Positive: The homepage title must equal 'Swag Labs'.
        """
        driver.get(BASE_URL)
        actual_title = driver.title
        assert actual_title == EXPECTED_HOME_TITLE, (
            f"Expected title '{EXPECTED_HOME_TITLE}', got '{actual_title}'"
        )

    # ---- Negative --------------------------------------------------------- #
    def test_title_negative(self, driver):
        """
        Negative: The homepage title must NOT be an empty string or
        an arbitrary wrong value like 'Google'.
        """
        driver.get(BASE_URL)
        actual_title = driver.title
        wrong_title  = "Google"
        assert actual_title != "", \
            "Title should not be an empty string."
        assert actual_title != wrong_title, (
            f"Title should not equal '{wrong_title}'."
        )


# =========================================================================== #
#  2.  URL OF THE HOMEPAGE
# =========================================================================== #

class TestHomepageURL:
    """Test cases for the URL of the homepage."""

    # ---- Positive --------------------------------------------------------- #
    def test_homepage_url_positive(self, driver):
        """
        Positive: After navigating to BASE_URL the current URL must
        match the expected homepage URL exactly.
        """
        driver.get(BASE_URL)
        actual_url = driver.current_url
        assert actual_url == EXPECTED_HOME_URL, (
            f"Expected URL '{EXPECTED_HOME_URL}', got '{actual_url}'"
        )

    # ---- Negative --------------------------------------------------------- #
    def test_homepage_url_negative(self, driver):
        """
        Negative: The homepage URL must not be a completely different domain.
        """
        driver.get(BASE_URL)
        actual_url = driver.current_url
        assert "saucedemo.com" in actual_url, (
            f"URL '{actual_url}' does not contain 'saucedemo.com'."
        )
        assert actual_url != "https://www.google.com/", \
            "Homepage URL should not be google.com."


# =========================================================================== #
#  3.  URL OF THE DASHBOARD AFTER LOGIN
# =========================================================================== #

class TestDashboardURL:
    """Test cases for the dashboard URL after login."""

    # ---- Positive --------------------------------------------------------- #
    def test_dashboard_url_positive(self, driver):
        """
        Positive: After a successful login with valid credentials the URL
        must redirect to the inventory/dashboard page.
        """
        do_login(driver, VALID_USERNAME, VALID_PASSWORD)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains("inventory"))
        actual_url = driver.current_url
        assert actual_url == EXPECTED_DASH_URL, (
            f"Expected dashboard URL '{EXPECTED_DASH_URL}', got '{actual_url}'"
        )

    # ---- Negative --------------------------------------------------------- #
    def test_dashboard_url_negative_invalid_credentials(self, driver):
        """
        Negative: Login with invalid credentials must NOT redirect to the
        dashboard; the user should remain on the login page.
        """
        do_login(driver, INVALID_USERNAME, INVALID_PASSWORD)
        actual_url = driver.current_url
        # Should still be on the login page, not the inventory page
        assert "inventory" not in actual_url, (
            f"Invalid credentials should not reach inventory page. "
            f"Current URL: '{actual_url}'"
        )

    # ---- Negative --------------------------------------------------------- #
    def test_dashboard_url_negative_empty_credentials(self, driver):
        """
        Negative: Login with empty username and password must NOT
        redirect to the dashboard.
        """
        do_login(driver, "", "")
        actual_url = driver.current_url
        assert "inventory" not in actual_url, (
            f"Empty credentials should not reach inventory page. "
            f"Current URL: '{actual_url}'"
        )
