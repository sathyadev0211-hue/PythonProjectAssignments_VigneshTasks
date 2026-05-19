"""
login_page.py
-------------
Login Page class using the Page Object Model (POM) design pattern.
Encapsulates all locators and actions for the Zen Portal login/logout flow.
Inherits from BasePage for shared Selenium utilities.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
import allure

from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the Zen Portal Login / Logout page.

    Responsibilities:
    - Navigate to the portal URL
    - Interact with username, password inputs and the login/logout buttons
    - Validate element presence and page state
    """

    # ------------------------------------------------------------------
    # URL
    # ------------------------------------------------------------------
    ZEN_PORTAL_URL = "https://www.guvi.in/sign-in/"  # Update if different

    # ------------------------------------------------------------------
    # Locators  (CSS selectors / XPath — update to match live portal)
    # ------------------------------------------------------------------

    # Login form elements
    USERNAME_INPUT   = (By.ID,   "email")           # email/username field
    PASSWORD_INPUT   = (By.ID,   "password")         # password field
    SUBMIT_BUTTON    = (By.XPATH, "//button[@type='submit']")  # submit/login btn

    # Post-login elements
    LOGOUT_BUTTON    = (By.XPATH,
                        "//a[contains(text(),'Logout') or "
                        "contains(text(),'Sign Out') or "
                        "contains(@href,'logout') or "
                        "contains(@href,'sign-out')]")

    # Error / validation message shown on failed login
    ERROR_MESSAGE    = (By.XPATH,
                        "//*[contains(@class,'error') or "
                        "contains(@class,'alert') or "
                        "contains(@class,'invalid')]")

    # Element visible only after a successful login (dashboard indicator)
    DASHBOARD_ELEMENT = (By.XPATH,
                         "//*[contains(@class,'dashboard') or "
                         "contains(@class,'home') or "
                         "contains(@href,'dashboard')]")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    @allure.step("Navigate to Zen Portal login page")
    def open_zen_portal(self) -> None:
        """
        Open the Zen Portal login page in the browser.

        Raises:
            WebDriverException: If the URL cannot be loaded.
        """
        self.navigate_to(self.ZEN_PORTAL_URL)
        self.take_screenshot("Zen Portal Opened")

    # ------------------------------------------------------------------
    # Input field validations
    # ------------------------------------------------------------------

    @allure.step("Validate that the Username input field is present")
    def is_username_field_present(self) -> bool:
        """
        Check whether the username input field is visible on the page.

        Returns:
            bool: True if visible, False otherwise.
        """
        result = self.is_element_visible(self.USERNAME_INPUT)
        self.take_screenshot("Username Field Check")
        return result

    @allure.step("Validate that the Password input field is present")
    def is_password_field_present(self) -> bool:
        """
        Check whether the password input field is visible on the page.

        Returns:
            bool: True if visible, False otherwise.
        """
        result = self.is_element_visible(self.PASSWORD_INPUT)
        self.take_screenshot("Password Field Check")
        return result

    @allure.step("Validate that the Submit button is present and clickable")
    def is_submit_button_present(self) -> bool:
        """
        Check whether the submit/login button is present and interactable.

        Returns:
            bool: True if present, False otherwise.
        """
        result = self.is_element_present(self.SUBMIT_BUTTON)
        self.take_screenshot("Submit Button Check")
        return result

    @allure.step("Validate that the Logout button is present")
    def is_logout_button_present(self) -> bool:
        """
        Check whether the logout button is present on the page.

        Returns:
            bool: True if present, False otherwise.
        """
        result = self.is_element_present(self.LOGOUT_BUTTON)
        self.take_screenshot("Logout Button Check")
        return result

    # ------------------------------------------------------------------
    # Login actions
    # ------------------------------------------------------------------

    @allure.step("Enter username: {username}")
    def enter_username(self, username: str) -> None:
        """
        Type the provided username into the username input field.

        Args:
            username (str): The username/email to enter.

        Raises:
            TimeoutException: If the username field is not found.
        """
        self.enter_text(self.USERNAME_INPUT, username)

    @allure.step("Enter password")
    def enter_password(self, password: str) -> None:
        """
        Type the provided password into the password input field.
        (Password value is intentionally not logged for security.)

        Args:
            password (str): The password to enter.

        Raises:
            TimeoutException: If the password field is not found.
        """
        self.enter_text(self.PASSWORD_INPUT, password)

    @allure.step("Click the Submit / Login button")
    def click_submit(self) -> None:
        """
        Click the login/submit button to submit the login form.

        Raises:
            TimeoutException: If the button is not found or not clickable.
        """
        self.click_element(self.SUBMIT_BUTTON)
        self.take_screenshot("After Submit Click")

    @allure.step("Perform login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Full login workflow: enter credentials and submit the form.

        Args:
            username (str): The username/email for login.
            password (str): The password for login.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()

    # ------------------------------------------------------------------
    # Post-login state checks
    # ------------------------------------------------------------------

    @allure.step("Check if login was successful")
    def is_login_successful(self) -> bool:
        """
        Determine whether the login attempt was successful by checking
        for a post-login dashboard element or a URL change.

        Returns:
            bool: True if logged in successfully, False otherwise.
        """
        # Strategy 1: look for a dashboard/home element
        if self.is_element_present(self.DASHBOARD_ELEMENT):
            self.take_screenshot("Login Success - Dashboard Found")
            return True

        # Strategy 2: URL no longer contains 'sign-in' / 'login'
        current_url = self.get_current_url()
        logged_in = (
            "sign-in" not in current_url.lower() and
            "login"   not in current_url.lower()
        )
        self.take_screenshot("Login Success URL Check")
        return logged_in

    @allure.step("Check if login failed (error message displayed)")
    def is_login_failed(self) -> bool:
        """
        Check whether an error/validation message is shown after a
        failed login attempt.

        Returns:
            bool: True if an error message is visible, False otherwise.
        """
        result = self.is_element_visible(self.ERROR_MESSAGE)
        self.take_screenshot("Login Failed Check")
        return result

    # ------------------------------------------------------------------
    # Logout action
    # ------------------------------------------------------------------

    @allure.step("Click the Logout button")
    def click_logout(self) -> None:
        """
        Click the logout button to end the current session.

        Raises:
            NoSuchElementException: If the logout button is not found.
            TimeoutException: If the logout button is not clickable.
        """
        try:
            self.click_element(self.LOGOUT_BUTTON)
            self.take_screenshot("After Logout Click")
        except (NoSuchElementException, TimeoutException) as e:
            self.take_screenshot("Logout Button Not Found")
            raise NoSuchElementException(
                "Logout button could not be found on the page."
            ) from e

    @allure.step("Check if logout was successful")
    def is_logout_successful(self) -> bool:
        """
        Verify that logout succeeded by checking if the login page
        is displayed again or the URL reflects a signed-out state.

        Returns:
            bool: True if logged out successfully, False otherwise.
        """
        current_url = self.get_current_url()
        signed_out = (
            "sign-in" in current_url.lower() or
            "login"   in current_url.lower() or
            self.is_element_visible(self.USERNAME_INPUT)
        )
        self.take_screenshot("Logout Success Check")
        return signed_out
