"""
tests/test_zen_portal.py
------------------------
Pytest test suite for the Zen Portal using Page Object Model (POM).

Test Coverage:
  a) Successful Login
  b) Unsuccessful Login (negative test cases)
  c) Validate Username & Password input box presence
  d) Validate Submit button working
  e) Validate Logout button functionality

Requirements:
  - Python Selenium
  - Pytest + pytest-html (for HTML reports)
  - Page Object Model (POM) with Explicit Waits
  - Python OOP and Selenium Exception handling
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# ──────────────────────────────────────────────────────────────────────────────
# ⚙️  CREDENTIALS — Replace with your actual Zen Portal credentials
# ──────────────────────────────────────────────────────────────────────────────
VALID_USERNAME   = "sathyadev0211@gmail.com"
VALID_PASSWORD   = "P@ssw0rd@1"
INVALID_USERNAME = "invalid_user@test.com"
INVALID_PASSWORD = "WrongPassword123!"
EMPTY_STRING     = ""
# ──────────────────────────────────────────────────────────────────────────────


class TestZenPortalLogin:
    """
    Test class for Zen Portal Login functionality.
    Uses POM (LoginPage, DashboardPage) and Explicit Waits.
    """

    # ──────────────────────────────────────────────
    # a) Successful Login Test
    # ──────────────────────────────────────────────
    def test_successful_login(self, driver):
        """
        TC_001: Verify that a user can login with valid credentials.
        Expected: User is redirected to the dashboard after login.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Navigate to login page
        login_page.navigate_to_login()
        assert login_page.is_login_page(), "FAIL: Not on the login page"

        # Perform login with valid credentials
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        # Verify successful login by checking dashboard is loaded
        assert dashboard_page.is_logged_in(), (
            f"FAIL: Login failed. Current URL: {driver.current_url}"
        )

    # ──────────────────────────────────────────────
    # b) Unsuccessful Login Tests (Negative Cases)
    # ──────────────────────────────────────────────
    def test_login_with_invalid_credentials(self, driver):
        """
        TC_002: Verify that login fails with invalid username and password.
        Expected: Error message is displayed; user stays on login page.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(INVALID_USERNAME, INVALID_PASSWORD)

        # Should remain on login page or show error
        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Expected to stay on login page or see error with invalid credentials"
        )

    def test_login_with_invalid_username_valid_password(self, driver):
        """
        TC_003: Verify login fails with wrong username but correct password.
        Expected: Error message displayed.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(INVALID_USERNAME, VALID_PASSWORD)

        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Expected error for invalid username with valid password"
        )

    def test_login_with_valid_username_invalid_password(self, driver):
        """
        TC_004: Verify login fails with correct username but wrong password.
        Expected: Error message displayed.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(VALID_USERNAME, INVALID_PASSWORD)

        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Expected error for valid username with invalid password"
        )

    def test_login_with_empty_credentials(self, driver):
        """
        TC_005: Verify login fails when both fields are left empty.
        Expected: Validation error or form does not submit.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(EMPTY_STRING, EMPTY_STRING)

        # Form should NOT navigate away from login page
        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Empty credentials should not allow login"
        )

    def test_login_with_empty_username(self, driver):
        """
        TC_006: Verify login fails when username is empty.
        Expected: Validation error shown.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(EMPTY_STRING, VALID_PASSWORD)

        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Empty username should not allow login"
        )

    def test_login_with_empty_password(self, driver):
        """
        TC_007: Verify login fails when password is empty.
        Expected: Validation error shown.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.login(VALID_USERNAME, EMPTY_STRING)

        assert login_page.is_login_page() or login_page.is_error_displayed(), (
            "FAIL: Empty password should not allow login"
        )

    # ──────────────────────────────────────────────
    # c) Validate Username & Password Input Fields
    # ──────────────────────────────────────────────
    def test_username_input_field_is_present(self, driver):
        """
        TC_008: Verify the username input field exists on the login page.
        Expected: Username/email input is visible and present.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()

        assert login_page.is_username_field_present(), (
            "FAIL: Username input field not found on login page"
        )

    def test_password_input_field_is_present(self, driver):
        """
        TC_009: Verify the password input field exists on the login page.
        Expected: Password input is visible and present.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()

        assert login_page.is_password_field_present(), (
            "FAIL: Password input field not found on login page"
        )

    def test_username_field_accepts_text_input(self, driver):
        """
        TC_010: Verify the username input field accepts text.
        Expected: Text typed is reflected in the input field.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.enter_username(VALID_USERNAME)

        username_element = login_page.find_element(LoginPage.USERNAME_INPUT)
        entered_value = username_element.get_attribute("value")

        assert entered_value == VALID_USERNAME, (
            f"FAIL: Username field value mismatch. Got: '{entered_value}'"
        )

    def test_password_field_accepts_text_input(self, driver):
        """
        TC_011: Verify the password input field accepts text (masked input).
        Expected: Text is accepted and field type is 'password'.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()
        login_page.enter_password(VALID_PASSWORD)

        password_element = login_page.find_element(LoginPage.PASSWORD_INPUT)
        field_type  = password_element.get_attribute("type")
        field_value = password_element.get_attribute("value")

        assert field_type == "password", (
            f"FAIL: Password field type should be 'password', got '{field_type}'"
        )
        assert len(field_value) > 0, "FAIL: Password field should not be empty after input"

    # ──────────────────────────────────────────────
    # d) Validate Submit Button
    # ──────────────────────────────────────────────
    def test_submit_button_is_present(self, driver):
        """
        TC_012: Verify the submit/login button is present on the login page.
        Expected: Submit button is found on the page.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()

        assert login_page.is_submit_button_present(), (
            "FAIL: Submit button not found on the login page"
        )

    def test_submit_button_is_enabled(self, driver):
        """
        TC_013: Verify the submit button is enabled and clickable.
        Expected: Button is not disabled.
        """
        login_page = LoginPage(driver)

        login_page.navigate_to_login()

        assert login_page.is_submit_button_enabled(), (
            "FAIL: Submit button is present but not enabled/clickable"
        )

    def test_submit_button_triggers_login(self, driver):
        """
        TC_014: Verify that clicking submit with valid credentials initiates login.
        Expected: Page transitions away from the login page.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.navigate_to_login()
        login_page.enter_username(VALID_USERNAME)
        login_page.enter_password(VALID_PASSWORD)
        login_page.click_submit()  # Click submit button explicitly

        assert dashboard_page.is_logged_in(), (
            "FAIL: Submit button did not trigger navigation to dashboard"
        )

    # ──────────────────────────────────────────────
    # e) Validate Logout Functionality
    # ──────────────────────────────────────────────
    def test_logout_button_is_visible_after_login(self, driver):
        """
        TC_015: Verify that logout option is available after logging in.
        Expected: Logout button/link is visible on the dashboard.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Login first
        login_page.navigate_to_login()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        assert dashboard_page.is_logged_in(), "Prerequisite FAIL: Login did not succeed"

        # Try to open profile menu to reveal logout
        try:
            dashboard_page.click_profile_menu()
        except Exception:
            pass  # Some portals show logout directly

        assert dashboard_page.is_logout_button_visible(), (
            "FAIL: Logout button not visible after login"
        )

    def test_successful_logout(self, driver):
        """
        TC_016: Verify that the user can successfully log out.
        Expected: After logout, user is redirected to the login page.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Step 1: Login
        login_page.navigate_to_login()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)

        assert dashboard_page.is_logged_in(), "Prerequisite FAIL: Login did not succeed"

        # Step 2: Logout
        dashboard_page.logout()

        # Step 3: Verify redirect back to login page
        assert login_page.is_login_page(), (
            f"FAIL: After logout, expected login page. Got URL: {driver.current_url}"
        )

    def test_cannot_access_dashboard_after_logout(self, driver):
        """
        TC_017: Verify user cannot access dashboard after logging out.
        Expected: Dashboard is inaccessible; user redirected to login.
        """
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        # Login
        login_page.navigate_to_login()
        login_page.login(VALID_USERNAME, VALID_PASSWORD)
        assert dashboard_page.is_logged_in(), "Prerequisite FAIL: Login did not succeed"

        dashboard_url = driver.current_url  # Save dashboard URL

        # Logout
        dashboard_page.logout()
        assert login_page.is_login_page(), "FAIL: Did not redirect to login after logout"

        # Attempt to revisit dashboard
        driver.get(dashboard_url)

        # Should be redirected back to login (session expired)
        assert login_page.is_login_page(), (
            "FAIL: User can still access dashboard after logout (session not cleared)"
        )
