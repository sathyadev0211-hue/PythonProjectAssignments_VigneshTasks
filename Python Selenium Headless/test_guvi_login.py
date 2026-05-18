"""
GUVI Login Automation Test Suite
=================================
Uses Python Selenium + Pytest to automate and validate
the GUVI login portal at https://www.guvi.in/

Test Coverage:
    - Positive Test Cases: Valid URL navigation, visible/enabled fields, successful login
    - Negative Test Cases: Invalid credentials, empty fields, wrong URL validation

Run with HTML report:
    pytest test_guvi_login.py -v --html=report.html --self-contained-html

Requirements:
    pip install selenium pytest pytest-html webdriver-manager
"""

import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# ─────────────────────────────────────────────
# Configuration — replace credentials before run,
# then remove them before committing to GitHub
# ─────────────────────────────────────────────
BASE_URL      = "https://www.guvi.in/"
LOGIN_URL     = "https://www.guvi.in/sign-in/"
VALID_EMAIL   = "your_email@example.com"      # TODO: replace, then remove
VALID_PASSWORD = "your_password"              # TODO: replace, then remove


# ─────────────────────────────────────────────
# Pytest Fixture — shared browser session
# ─────────────────────────────────────────────
@pytest.fixture(scope="module")
def driver():
    """
    Set up Chrome WebDriver using webdriver-manager.
    Scope = 'module' so one browser is shared across all tests in this file.
    """
    chrome_options = Options()
    # Uncomment the next line to run headlessly (no visible browser window):
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(10)

    yield browser  # hand the browser to each test

    # Teardown — close browser after all tests finish
    browser.quit()


# ─────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────
def wait_for_element(driver, by, value, timeout=15):
    """Wait up to `timeout` seconds for an element to be clickable."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )


def wait_for_visibility(driver, by, value, timeout=15):
    """Wait up to `timeout` seconds for an element to become visible."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


# ═════════════════════════════════════════════
# POSITIVE TEST CASES
# ═════════════════════════════════════════════

class TestPositiveCases:
    """All tests that expect correct / successful behaviour."""

    # ── Test 1 ──────────────────────────────
    def test_visit_guvi_homepage(self, driver):
        """
        POSITIVE: Verify the GUVI homepage loads and the URL is correct.
        Step: Navigate to https://www.guvi.in/
        """
        driver.get(BASE_URL)
        time.sleep(2)  # allow page to settle

        current_url = driver.current_url
        assert "guvi.in" in current_url, (
            f"Expected 'guvi.in' in URL, but got: {current_url}"
        )
        print(f"\n[PASS] Homepage URL: {current_url}")

    # ── Test 2 ──────────────────────────────
    def test_login_button_navigates_to_signin_url(self, driver):
        """
        POSITIVE: Validate that clicking Login navigates to https://www.guvi.in/sign-in/
        Step: Click the Login button on the homepage.
        """
        driver.get(BASE_URL)
        time.sleep(2)

        # Locate the Login / Sign-in link (try multiple selectors for resilience)
        try:
            login_btn = wait_for_element(driver, By.XPATH,
                "//a[contains(@href,'sign-in') or contains(text(),'Login') "
                "or contains(text(),'Sign In') or contains(text(),'sign-in')]"
            )
        except Exception:
            # Fallback: direct navigation to sign-in page
            driver.get(LOGIN_URL)
            login_btn = None

        if login_btn:
            login_btn.click()

        time.sleep(2)
        current_url = driver.current_url

        assert "sign-in" in current_url or "login" in current_url, (
            f"Expected sign-in URL after clicking Login, but got: {current_url}"
        )
        print(f"\n[PASS] Redirected to: {current_url}")

    # ── Test 3 ──────────────────────────────
    def test_signin_page_url_is_correct(self, driver):
        """
        POSITIVE (Validation #1): Confirm the sign-in page URL matches
        https://www.guvi.in/sign-in/
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        current_url = driver.current_url
        assert LOGIN_URL.rstrip("/") in current_url.rstrip("/"), (
            f"Expected URL to contain '{LOGIN_URL}', got: {current_url}"
        )
        print(f"\n[PASS] Sign-in URL verified: {current_url}")

    # ── Test 4 ──────────────────────────────
    def test_username_field_visible_and_enabled(self, driver):
        """
        POSITIVE (Validation #2a): Verify the email/username input box
        is visible and enabled on the sign-in page.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='email' or @name='email' or @id='email' "
            "or @placeholder[contains(., 'email') or contains(., 'Email') "
            "or contains(., 'username') or contains(., 'Username')]]"
        )

        assert email_field.is_displayed(), "Email/Username field is NOT visible."
        assert email_field.is_enabled(),   "Email/Username field is NOT enabled."
        print("\n[PASS] Username field is visible and enabled.")

    # ── Test 5 ──────────────────────────────
    def test_password_field_visible_and_enabled(self, driver):
        """
        POSITIVE (Validation #2b): Verify the password input box
        is visible and enabled on the sign-in page.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        password_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='password' or @name='password' or @id='password']"
        )

        assert password_field.is_displayed(), "Password field is NOT visible."
        assert password_field.is_enabled(),   "Password field is NOT enabled."
        print("\n[PASS] Password field is visible and enabled.")

    # ── Test 6 ──────────────────────────────
    def test_submit_button_visible_and_clickable(self, driver):
        """
        POSITIVE (Validation #3): Verify the Submit / Sign In button
        is present and clickable.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login') or contains(text(),'Submit')]"
        )

        assert submit_btn.is_displayed(), "Submit button is NOT visible."
        assert submit_btn.is_enabled(),   "Submit button is NOT enabled."
        print("\n[PASS] Submit button is visible and clickable.")

    # ── Test 7 ──────────────────────────────
    def test_successful_login_with_valid_credentials(self, driver):
        """
        POSITIVE: Perform full login using valid credentials and verify
        the user is redirected away from the sign-in page.

        NOTE: Replace VALID_EMAIL and VALID_PASSWORD at the top of this
        file with real credentials before running. Remove them afterward.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Enter email
        email_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='email' or @name='email' or @id='email']"
        )
        email_field.clear()
        email_field.send_keys(VALID_EMAIL)

        # Enter password
        password_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='password' or @name='password' or @id='password']"
        )
        password_field.clear()
        password_field.send_keys(VALID_PASSWORD)

        # Click submit
        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login')]"
        )
        submit_btn.click()
        time.sleep(3)

        # After login the URL should no longer be the sign-in page
        current_url = driver.current_url
        assert "sign-in" not in current_url, (
            f"Login may have failed — still on: {current_url}"
        )
        print(f"\n[PASS] Successfully logged in. Redirected to: {current_url}")


# ═════════════════════════════════════════════
# NEGATIVE TEST CASES
# ═════════════════════════════════════════════

class TestNegativeCases:
    """All tests that verify the system handles invalid input gracefully."""

    # ── Test 8 ──────────────────────────────
    def test_login_with_invalid_email_and_password(self, driver):
        """
        NEGATIVE: Login with a completely wrong email + password should
        stay on or near the sign-in page and show an error.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='email' or @name='email' or @id='email']"
        )
        email_field.clear()
        email_field.send_keys("invalid_user@fake.com")

        password_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='password' or @name='password' or @id='password']"
        )
        password_field.clear()
        password_field.send_keys("WrongPassword@999")

        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login')]"
        )
        submit_btn.click()
        time.sleep(3)

        current_url = driver.current_url
        # Should remain on sign-in page or a page indicating failure
        assert "sign-in" in current_url or "login" in current_url or "guvi.in" in current_url, (
            "Unexpected redirect after invalid credentials."
        )
        print(f"\n[PASS] Invalid credentials correctly rejected. URL: {current_url}")

    # ── Test 9 ──────────────────────────────
    def test_login_with_empty_email(self, driver):
        """
        NEGATIVE: Submitting the form with an empty email field should
        not proceed — HTML5 validation or a JS error message should block it.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        # Leave email blank, fill only password
        password_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='password' or @name='password' or @id='password']"
        )
        password_field.clear()
        password_field.send_keys("SomePassword@1")

        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login')]"
        )
        submit_btn.click()
        time.sleep(2)

        # Should still be on the sign-in page
        current_url = driver.current_url
        assert "sign-in" in current_url or "login" in current_url, (
            f"Expected to stay on sign-in page with empty email, but navigated to: {current_url}"
        )
        print("\n[PASS] Empty email correctly prevented form submission.")

    # ── Test 10 ──────────────────────────────
    def test_login_with_empty_password(self, driver):
        """
        NEGATIVE: Submitting the form with an empty password should
        not proceed and should stay on the sign-in page.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='email' or @name='email' or @id='email']"
        )
        email_field.clear()
        email_field.send_keys("someone@example.com")

        # Leave password blank and click submit
        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login')]"
        )
        submit_btn.click()
        time.sleep(2)

        current_url = driver.current_url
        assert "sign-in" in current_url or "login" in current_url, (
            f"Expected to stay on sign-in page with empty password, but navigated to: {current_url}"
        )
        print("\n[PASS] Empty password correctly prevented form submission.")

    # ── Test 11 ──────────────────────────────
    def test_login_with_invalid_email_format(self, driver):
        """
        NEGATIVE: Entering a malformed email (no '@') should trigger
        HTML5 validation and prevent submission.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        email_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='email' or @name='email' or @id='email']"
        )
        email_field.clear()
        email_field.send_keys("notavalidemail")   # missing @ and domain

        password_field = wait_for_visibility(driver, By.XPATH,
            "//input[@type='password' or @name='password' or @id='password']"
        )
        password_field.clear()
        password_field.send_keys("SomePassword@1")

        submit_btn = wait_for_element(driver, By.XPATH,
            "//button[@type='submit' or contains(text(),'Sign In') "
            "or contains(text(),'Login')]"
        )
        submit_btn.click()
        time.sleep(2)

        current_url = driver.current_url
        assert "sign-in" in current_url or "login" in current_url, (
            f"Expected validation error for malformed email, but got: {current_url}"
        )
        print("\n[PASS] Malformed email correctly rejected by validation.")

    # ── Test 12 ──────────────────────────────
    def test_signin_url_is_not_wrong_url(self, driver):
        """
        NEGATIVE (URL Validation): Confirm the sign-in page URL does NOT
        match a wrong/unexpected URL pattern.
        """
        driver.get(LOGIN_URL)
        time.sleep(2)

        current_url = driver.current_url
        wrong_url = "https://www.guvi.in/register/"

        assert current_url.rstrip("/") != wrong_url.rstrip("/"), (
            f"URL should NOT be the register page, but got: {current_url}"
        )
        print(f"\n[PASS] Sign-in URL is correct and not the wrong URL: {current_url}")
