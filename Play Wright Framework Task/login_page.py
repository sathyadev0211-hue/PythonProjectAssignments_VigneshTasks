"""
Login Page Object Model for the Guvi Zen Portal.
Encapsulates all locators and actions related to the login page.
"""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """
    Page Object for the Zen Portal Login page.
    URL: https://www.guvi.in/sign-in/
    """

    # ── Locators ──────────────────────────────────────────────────────────────
    USERNAME_INPUT   = "input[name='email']"
    PASSWORD_INPUT   = "input[name='password']"
    SUBMIT_BUTTON    = "button[type='submit']"
    ERROR_MESSAGE    = "p.error-msg, .error-message, [class*='error']"
    PAGE_HEADING     = "h1, h2, .login-title"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Navigation ────────────────────────────────────────────────────────────

    def open_login_page(self) -> None:
        """Navigate to the Zen Portal login page."""
        self.navigate("https://www.guvi.in/sign-in/")

    # ── Element accessors (with explicit wait) ────────────────────────────────

    def get_username_input(self):
        """Return the username input element after waiting for it."""
        return self.wait_for_element(self.USERNAME_INPUT)

    def get_password_input(self):
        """Return the password input element after waiting for it."""
        return self.wait_for_element(self.PASSWORD_INPUT)

    def get_submit_button(self):
        """Return the submit button element after waiting for it."""
        return self.wait_for_element(self.SUBMIT_BUTTON)

    # ── Validation helpers ────────────────────────────────────────────────────

    def is_username_input_visible(self) -> bool:
        """Check that the username input box is rendered and visible."""
        return self.is_element_visible(self.USERNAME_INPUT)

    def is_password_input_visible(self) -> bool:
        """Check that the password input box is rendered and visible."""
        return self.is_element_visible(self.PASSWORD_INPUT)

    def is_submit_button_visible(self) -> bool:
        """Check that the submit button is rendered and visible."""
        return self.is_element_visible(self.SUBMIT_BUTTON)

    def is_submit_button_enabled(self) -> bool:
        """Return True if the submit button is enabled (not disabled)."""
        try:
            btn = self.page.locator(self.SUBMIT_BUTTON)
            return btn.is_enabled()
        except Exception:
            return False

    def get_error_message(self) -> str:
        """Return the text of the error message shown after failed login."""
        try:
            self.page.wait_for_selector(self.ERROR_MESSAGE, state="visible", timeout=7000)
            return self.page.locator(self.ERROR_MESSAGE).first.inner_text()
        except Exception:
            return ""

    # ── Actions ───────────────────────────────────────────────────────────────

    def enter_username(self, username: str) -> None:
        """Clear the username field and type the provided value."""
        field = self.get_username_input()
        field.clear()
        field.fill(username)

    def enter_password(self, password: str) -> None:
        """Clear the password field and type the provided value."""
        field = self.get_password_input()
        field.clear()
        field.fill(password)

    def click_submit(self) -> None:
        """Click the login submit button."""
        self.get_submit_button().click()

    def login(self, username: str, password: str) -> None:
        """
        High-level helper: fill in credentials and click submit.

        Args:
            username: Valid or invalid e-mail address.
            password: Corresponding password.
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
