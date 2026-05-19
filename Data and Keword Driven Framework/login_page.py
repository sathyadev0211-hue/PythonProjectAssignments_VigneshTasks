# pages/login_page.py
# Page Object Model (POM) for OrangeHRM Login Page
# Encapsulates all login page interactions and locators

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ─── Constants ───────────────────────────────────────────────────────────────
LOGIN_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
DEFAULT_TIMEOUT = 15  # seconds for Explicit Wait


class LoginPage:
    """
    Page Object Model class representing the OrangeHRM Login Page.
    Uses Explicit Wait and Expected Conditions throughout — no sleep().
    """

    # ─── Locators ─────────────────────────────────────────────────────────────
    USERNAME_INPUT   = (By.NAME, "username")
    PASSWORD_INPUT   = (By.NAME, "password")
    LOGIN_BUTTON     = (By.XPATH, "//button[@type='submit']")
    DASHBOARD_HEADER = (By.XPATH, "//h6[contains(@class,'oxd-text') and text()='Dashboard']")
    ERROR_MESSAGE    = (By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")

    def __init__(self, driver):
        """
        Constructor: Accepts the WebDriver instance and sets up Explicit Wait.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ─── Actions ──────────────────────────────────────────────────────────────

    def navigate_to_login(self):
        """Navigate browser to the OrangeHRM login URL."""
        self.driver.get(LOGIN_URL)

    def enter_username(self, username: str):
        """
        Wait for username field and type the given username.

        Args:
            username: Username string to enter
        """
        username_field = self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password: str):
        """
        Wait for password field and type the given password.

        Args:
            password: Password string to enter
        """
        password_field = self.wait.until(
            EC.visibility_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """Wait for the Login button to be clickable, then click it."""
        login_btn = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_btn.click()

    def perform_login(self, username: str, password: str):
        """
        Convenience method: Navigate to login page and perform full login.

        Args:
            username: Username string
            password: Password string
        """
        self.navigate_to_login()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ─── Verification ─────────────────────────────────────────────────────────

    def is_login_successful(self) -> bool:
        """
        Check if login was successful by waiting for the Dashboard header.

        Returns:
            True  — if Dashboard header appears within timeout
            False — if Dashboard does not appear (login failed)
        """
        try:
            self.wait.until(
                EC.visibility_of_element_located(self.DASHBOARD_HEADER)
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        """
        Retrieve the error message text shown on failed login attempts.

        Returns:
            Error message string, or empty string if none found
        """
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_elem.text.strip()
        except Exception:
            return ""
