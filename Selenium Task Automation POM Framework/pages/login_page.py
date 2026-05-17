"""
pages/login_page.py
-------------------
Page Object Model for the Zen Portal Login Page (https://v2.zenclass.in/login).
Contains all locators and actions related to login functionality.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the Zen Portal login page.
    Inherits common wait utilities from BasePage.
    """

    # ──────────────────────────────────────────────
    # URL
    # ──────────────────────────────────────────────
    URL = "https://v2.zenclass.in/login"

    # ──────────────────────────────────────────────
    # Locators  (v2.zenclass.in React app)
    # ──────────────────────────────────────────────

    # Username / email field — covers id, name, type, placeholder variants
    USERNAME_INPUT = (By.XPATH,
        "//input[@id='email' or @name='email' or @type='email' "
        "or contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'email') "
        "or contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'username')]"
    )

    # Password field
    PASSWORD_INPUT = (By.XPATH,
        "//input[@id='password' or @name='password' or @type='password']"
    )

    # Submit / Login button
    SUBMIT_BUTTON = (By.XPATH,
        "//button[@type='submit'] | "
        "//button[contains(translate(normalize-space(.),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'LOGIN')] | "
        "//button[contains(translate(normalize-space(.),'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'SIGN IN')]"
    )

    # Error / validation message locators
    ERROR_MESSAGE = (By.XPATH,
        "//*[contains(@class,'error') or contains(@class,'alert') "
        "or contains(@class,'invalid') or contains(@class,'danger') "
        "or contains(@class,'toast') or contains(@class,'notification') "
        "or contains(@class,'Toastify')]"
    )

    def __init__(self, driver):
        """Initialize LoginPage; does NOT auto-navigate."""
        super().__init__(driver)

    # ──────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────
    def navigate_to_login(self):
        """Open the Zen Portal login page."""
        self.open_url(self.URL)

    def enter_username(self, username: str):
        """Type username/email into the username input field."""
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password(self, password: str):
        """Type password into the password input field."""
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click the login/submit button."""
        self.click_element(self.SUBMIT_BUTTON)

    def login(self, username: str, password: str):
        """
        Full login flow: enter credentials and submit.
        :param username: User's email/username
        :param password: User's password
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()

    # ──────────────────────────────────────────────
    # Validations
    # ──────────────────────────────────────────────
    def is_username_field_present(self) -> bool:
        """Check if the username input field exists on the page."""
        return self.is_element_present(self.USERNAME_INPUT)

    def is_password_field_present(self) -> bool:
        """Check if the password input field exists on the page."""
        return self.is_element_present(self.PASSWORD_INPUT)

    def is_submit_button_present(self) -> bool:
        """Check if the submit/login button is present on the page."""
        return self.is_element_present(self.SUBMIT_BUTTON)

    def is_submit_button_enabled(self) -> bool:
        """Check if the submit button is clickable/enabled."""
        try:
            btn = self.find_element(self.SUBMIT_BUTTON)
            return btn.is_enabled()
        except (TimeoutException, NoSuchElementException):
            return False

    def get_error_message(self) -> str:
        """
        Return the error message text displayed after a failed login.
        Returns an empty string if no error message is found.
        """
        if self.is_element_visible(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return ""

    def is_error_displayed(self) -> bool:
        """Return True if any error/alert message is visible on the page."""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def is_login_page(self) -> bool:
        """Return True if the browser is currently on the login page."""
        url = self.get_current_url()
        return "login" in url or "sign-in" in url
