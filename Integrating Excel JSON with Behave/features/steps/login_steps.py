"""
login_steps.py
--------------
Step definitions for the Zen Portal Login/Logout BDD scenarios.
Maps Gherkin steps to Python functions using the Behave framework.
Uses the LoginPage Page Object for all browser interactions.
"""

from behave import given, when, then
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
import allure

from pages.login_page import LoginPage


# -----------------------------------------------------------------------
# Background / Precondition Steps
# -----------------------------------------------------------------------

@given('I have navigated to the Zen Portal login page')
@allure.step("Navigate to Zen Portal login page")
def step_navigate_to_zen_portal(context):
    """
    Precondition: Open the Zen Portal login URL in the browser.
    The WebDriver instance is available via context.driver (set in environment.py).
    """
    try:
        context.login_page = LoginPage(context.driver)
        context.login_page.open_zen_portal()
        allure.attach(
            f"URL: {context.driver.current_url}",
            name="Current URL after navigation",
            attachment_type=allure.attachment_type.TEXT
        )
    except WebDriverException as e:
        allure.attach(
            str(e),
            name="Navigation Error",
            attachment_type=allure.attachment_type.TEXT
        )
        raise AssertionError(f"Failed to navigate to Zen Portal: {e}")


# -----------------------------------------------------------------------
# UI Validation Steps
# -----------------------------------------------------------------------

@then('the Username input field should be visible')
@allure.step("Assert Username input field is visible")
def step_validate_username_field(context):
    """Verify that the username/email input field is displayed on the login page."""
    try:
        assert context.login_page.is_username_field_present(), \
            "Username input field is NOT visible on the login page."
        allure.attach(
            "Username input field validation: PASSED",
            name="Username Field Validation",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Username Field Missing")
        raise


@then('the Password input field should be visible')
@allure.step("Assert Password input field is visible")
def step_validate_password_field(context):
    """Verify that the password input field is displayed on the login page."""
    try:
        assert context.login_page.is_password_field_present(), \
            "Password input field is NOT visible on the login page."
        allure.attach(
            "Password input field validation: PASSED",
            name="Password Field Validation",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Password Field Missing")
        raise


@then('the Submit button should be present on the login page')
@allure.step("Assert Submit button is present")
def step_validate_submit_button(context):
    """Verify that the submit/login button is present and interactable."""
    try:
        assert context.login_page.is_submit_button_present(), \
            "Submit button is NOT present on the login page."
        allure.attach(
            "Submit button validation: PASSED",
            name="Submit Button Validation",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Submit Button Missing")
        raise


@then('the Logout button should be visible on the page')
@allure.step("Assert Logout button is visible")
def step_validate_logout_button(context):
    """Verify that the logout button is present on the authenticated page."""
    try:
        assert context.login_page.is_logout_button_present(), \
            "Logout button is NOT visible after login."
        allure.attach(
            "Logout button validation: PASSED",
            name="Logout Button Validation",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Logout Button Missing")
        raise


# -----------------------------------------------------------------------
# Login Action Steps
# -----------------------------------------------------------------------

@when('I enter a valid username "{username}"')
@allure.step("Enter valid username: {username}")
def step_enter_valid_username(context, username):
    """
    Enter a valid username into the username input field.

    Args:
        username (str): The valid email/username to type.
    """
    try:
        context.login_page.enter_username(username)
        allure.attach(
            f"Entered username: {username}",
            name="Username Input",
            attachment_type=allure.attachment_type.TEXT
        )
    except (TimeoutException, NoSuchElementException) as e:
        context.login_page.take_screenshot("Username Input Error")
        raise AssertionError(f"Could not enter username: {e}")


@when('I enter a valid password "{password}"')
@allure.step("Enter valid password")
def step_enter_valid_password(context, password):
    """
    Enter a valid password into the password input field.

    Args:
        password (str): The valid password to type.
    """
    try:
        context.login_page.enter_password(password)
        allure.attach(
            "Password entered (value hidden for security)",
            name="Password Input",
            attachment_type=allure.attachment_type.TEXT
        )
    except (TimeoutException, NoSuchElementException) as e:
        context.login_page.take_screenshot("Password Input Error")
        raise AssertionError(f"Could not enter password: {e}")


@when('I enter an invalid username "{username}"')
@allure.step("Enter invalid username: {username}")
def step_enter_invalid_username(context, username):
    """
    Enter an invalid/non-existent username to trigger login failure.

    Args:
        username (str): The invalid username to type.
    """
    try:
        context.login_page.enter_username(username)
        allure.attach(
            f"Entered invalid username: {username}",
            name="Invalid Username Input",
            attachment_type=allure.attachment_type.TEXT
        )
    except (TimeoutException, NoSuchElementException) as e:
        context.login_page.take_screenshot("Invalid Username Input Error")
        raise AssertionError(f"Could not enter invalid username: {e}")


@when('I enter an invalid password "{password}"')
@allure.step("Enter invalid password")
def step_enter_invalid_password(context, password):
    """
    Enter an incorrect password to trigger login failure.

    Args:
        password (str): The wrong password to type.
    """
    try:
        context.login_page.enter_password(password)
        allure.attach(
            "Invalid password entered",
            name="Invalid Password Input",
            attachment_type=allure.attachment_type.TEXT
        )
    except (TimeoutException, NoSuchElementException) as e:
        context.login_page.take_screenshot("Invalid Password Input Error")
        raise AssertionError(f"Could not enter invalid password: {e}")


@when('I click the Submit button')
@allure.step("Click Submit / Login button")
def step_click_submit_button(context):
    """Click the submit/login button to submit the credentials."""
    try:
        context.login_page.click_submit()
    except (TimeoutException, NoSuchElementException) as e:
        context.login_page.take_screenshot("Submit Click Error")
        raise AssertionError(f"Could not click Submit button: {e}")


# -----------------------------------------------------------------------
# Login Outcome Steps
# -----------------------------------------------------------------------

@then('I should be logged in successfully')
@allure.step("Assert successful login")
def step_verify_successful_login(context):
    """Assert that the user is now logged in (dashboard/home is shown)."""
    try:
        assert context.login_page.is_login_successful(), \
            "Login was NOT successful — dashboard/home page not detected."
        allure.attach(
            f"Login successful. Current URL: {context.driver.current_url}",
            name="Successful Login Verification",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Login Failure")
        raise


@then('I should see a login error message')
@allure.step("Assert login error message is displayed")
def step_verify_login_error(context):
    """Assert that an error/validation message is shown after failed login."""
    try:
        assert context.login_page.is_login_failed(), \
            "Expected a login error message, but none was displayed."
        allure.attach(
            "Login error message displayed as expected.",
            name="Failed Login Verification",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Error Message Missing")
        raise


# -----------------------------------------------------------------------
# Logout Steps
# -----------------------------------------------------------------------

@when('I click the Logout button')
@allure.step("Click the Logout button")
def step_click_logout_button(context):
    """Click the logout button to end the current session."""
    try:
        context.login_page.click_logout()
    except (NoSuchElementException, TimeoutException) as e:
        context.login_page.take_screenshot("Logout Click Error")
        raise AssertionError(f"Could not click Logout button: {e}")


@then('I should be logged out successfully')
@allure.step("Assert successful logout")
def step_verify_successful_logout(context):
    """Assert that the user has been successfully logged out."""
    try:
        assert context.login_page.is_logout_successful(), \
            "Logout was NOT successful — login page not detected after logout."
        allure.attach(
            f"Logout successful. Current URL: {context.driver.current_url}",
            name="Successful Logout Verification",
            attachment_type=allure.attachment_type.TEXT
        )
    except AssertionError as e:
        context.login_page.take_screenshot("Logout Failure")
        raise
