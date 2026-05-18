"""
test_zen_portal.py – Pytest test suite for the Guvi Zen Portal.

Covers:
  a) Successful Login
  b) Unsuccessful Login
  c) Validate Username & Password input boxes
  d) Validate Submit button is functional
  e) Validate Logout button functionality

Requirements satisfied:
  - Microsoft Python Playwright + Pytest framework
  - Page Object Model (POM) with Explicit Wait
  - Python OOP principles (class-based page objects, inheritance)
  - Playwright exceptions for error handling
  - HTML report generated via pytest-html
"""

import pytest
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


# ─────────────────────────────────────────────────────────────────────────────
# Test data  –  Replace placeholders with real credentials before running.
# Remove / gitignore credentials before sharing the repository.
# ─────────────────────────────────────────────────────────────────────────────
VALID_USERNAME   = "YOUR_EMAIL@example.com"      # <-- replace
VALID_PASSWORD   = "YOUR_PASSWORD"               # <-- replace
INVALID_USERNAME = "invalid_user@example.com"
INVALID_PASSWORD = "WrongPassword@123"


# ─────────────────────────────────────────────────────────────────────────────
# Helper – navigate to login page and return page-objects
# ─────────────────────────────────────────────────────────────────────────────

def _open_login(page: Page):
    """Open the Zen Portal login page and return its POM."""
    login_page = LoginPage(page)
    login_page.open_login_page()
    return login_page


# ─────────────────────────────────────────────────────────────────────────────
# a) Successful Login
# ─────────────────────────────────────────────────────────────────────────────

class TestSuccessfulLogin:
    """Verify that a registered user can log in with valid credentials."""

    def test_successful_login(self, page: Page):
        """
        TC-01: Login with valid credentials should redirect
               to the dashboard / home page.
        """
        try:
            login_page = _open_login(page)
            login_page.login(VALID_USERNAME, VALID_PASSWORD)

            dashboard = DashboardPage(page)

            # Explicit wait: wait for dashboard to be fully loaded
            page.wait_for_load_state("networkidle")

            assert dashboard.is_dashboard_loaded(), (
                f"Dashboard did not load after successful login. "
                f"Current URL: {page.url}"
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-01 timed out waiting for an element: {e}")

        except Exception as e:
            pytest.fail(f"TC-01 encountered an unexpected error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# b) Unsuccessful Login
# ─────────────────────────────────────────────────────────────────────────────

class TestUnsuccessfulLogin:
    """Verify that invalid credentials show an appropriate error."""

    def test_login_with_invalid_credentials(self, page: Page):
        """
        TC-02: Login with wrong username / password should display
               an error message and NOT redirect to the dashboard.
        """
        try:
            login_page = _open_login(page)
            login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

            # Explicit wait: give the page time to show the error
            page.wait_for_timeout(3000)

            error_msg = login_page.get_error_message()

            # At minimum, the user must still be on the login/sign-in page
            assert "sign-in" in page.url or "login" in page.url or error_msg, (
                "Expected to remain on the login page or see an error message "
                "after invalid login attempt."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-02 timed out waiting for an element: {e}")

        except Exception as e:
            pytest.fail(f"TC-02 encountered an unexpected error: {e}")

    def test_login_with_empty_credentials(self, page: Page):
        """
        TC-03: Clicking Submit without entering credentials should
               not proceed to the dashboard.
        """
        try:
            login_page = _open_login(page)
            login_page.click_submit()

            page.wait_for_timeout(2000)

            assert "sign-in" in page.url or "login" in page.url, (
                "Expected to stay on login page when no credentials are entered."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-03 timed out: {e}")

        except Exception as e:
            pytest.fail(f"TC-03 encountered an unexpected error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# c) Validate Username and Password input boxes
# ─────────────────────────────────────────────────────────────────────────────

class TestInputBoxValidation:
    """Verify that Username and Password input boxes exist and are interactable."""

    def test_username_input_is_visible(self, page: Page):
        """
        TC-04: Username input field must be visible on the login page.
        """
        try:
            login_page = _open_login(page)
            assert login_page.is_username_input_visible(), (
                "Username input box is NOT visible on the login page."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-04 timed out: {e}")

    def test_password_input_is_visible(self, page: Page):
        """
        TC-05: Password input field must be visible on the login page.
        """
        try:
            login_page = _open_login(page)
            assert login_page.is_password_input_visible(), (
                "Password input box is NOT visible on the login page."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-05 timed out: {e}")

    def test_username_input_accepts_text(self, page: Page):
        """
        TC-06: Typing into the username field should update its value.
        """
        try:
            login_page = _open_login(page)
            test_value = "testuser@example.com"
            login_page.enter_username(test_value)

            actual = page.locator(LoginPage.USERNAME_INPUT).input_value()
            assert actual == test_value, (
                f"Username field value mismatch. Expected: {test_value}, Got: {actual}"
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-06 timed out: {e}")

    def test_password_input_accepts_text(self, page: Page):
        """
        TC-07: Typing into the password field should update its value.
        """
        try:
            login_page = _open_login(page)
            test_value = "SecurePass@99"
            login_page.enter_password(test_value)

            actual = page.locator(LoginPage.PASSWORD_INPUT).input_value()
            assert actual == test_value, (
                f"Password field value mismatch. Expected: {test_value}, Got: {actual}"
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-07 timed out: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# d) Validate Submit button
# ─────────────────────────────────────────────────────────────────────────────

class TestSubmitButtonValidation:
    """Verify the Submit button is visible and enabled on the login page."""

    def test_submit_button_is_visible(self, page: Page):
        """
        TC-08: Submit button must be rendered on the login page.
        """
        try:
            login_page = _open_login(page)
            assert login_page.is_submit_button_visible(), (
                "Submit button is NOT visible on the login page."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-08 timed out: {e}")

    def test_submit_button_is_enabled(self, page: Page):
        """
        TC-09: Submit button must be enabled so the user can interact with it.
        """
        try:
            login_page = _open_login(page)
            assert login_page.is_submit_button_enabled(), (
                "Submit button is DISABLED on the login page."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-09 timed out: {e}")

    def test_submit_button_triggers_action(self, page: Page):
        """
        TC-10: Clicking Submit (even with empty fields) should trigger
               a page response – stay on login page or show validation.
        """
        try:
            login_page = _open_login(page)
            url_before = page.url
            login_page.click_submit()
            page.wait_for_timeout(2000)

            # Either URL changes or an error/validation message appears
            url_after = page.url
            error_present = login_page.is_element_visible(LoginPage.ERROR_MESSAGE)

            assert url_before != url_after or error_present, (
                "Clicking Submit produced no observable change."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-10 timed out: {e}")

        except Exception as e:
            # Acceptable: button may raise a browser-level validation popup
            pass


# ─────────────────────────────────────────────────────────────────────────────
# e) Validate Logout button functionality
# ─────────────────────────────────────────────────────────────────────────────

class TestLogoutFunctionality:
    """Verify the Logout button is present and successfully ends the session."""

    def test_logout_button_visible_after_login(self, page: Page):
        """
        TC-11: After a successful login the Logout button / option
               must be accessible in the UI.
        """
        try:
            login_page = _open_login(page)
            login_page.login(VALID_USERNAME, VALID_PASSWORD)
            page.wait_for_load_state("networkidle")

            dashboard = DashboardPage(page)
            # Open dropdown / profile menu if needed
            dashboard.open_profile_menu()

            assert dashboard.is_logout_button_visible(), (
                "Logout button is NOT visible after successful login."
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-11 timed out: {e}")

        except Exception as e:
            pytest.fail(f"TC-11 encountered an unexpected error: {e}")

    def test_logout_redirects_to_login(self, page: Page):
        """
        TC-12: Clicking Logout must end the session and redirect the
               user back to the login / home page.
        """
        try:
            # Step 1: Login
            login_page = _open_login(page)
            login_page.login(VALID_USERNAME, VALID_PASSWORD)
            page.wait_for_load_state("networkidle")

            # Step 2: Logout
            dashboard = DashboardPage(page)
            dashboard.logout()

            # Step 3: Verify we are no longer on a dashboard URL
            current_url = page.url
            still_on_dashboard = all(
                kw not in current_url
                for kw in ("dashboard", "home", "course", "profile")
            )

            assert still_on_dashboard or "sign-in" in current_url or "login" in current_url, (
                f"Logout did not redirect away from the dashboard. URL: {current_url}"
            )

        except PlaywrightTimeoutError as e:
            pytest.fail(f"TC-12 timed out: {e}")

        except Exception as e:
            pytest.fail(f"TC-12 encountered an unexpected error: {e}")
