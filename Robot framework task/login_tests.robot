*** Settings ***
# ---------------------------------------------------------
# Test Suite  : login_tests.robot
# Description : Verifies the login functionality of the
#               Robot Spare Bin Industries web application
#               (https://robotsparebinindustries.com).
#
# Keywords    : Defined in resources/keywords.robot
# Libraries   : SeleniumLibrary (via keywords resource)
# Tags        : login, smoke, regression
# ---------------------------------------------------------
Resource    ../resources/keywords.robot

# Suite-level setup and teardown
# Setup  : Opens browser once before ALL tests in this suite
# Teardown: Closes browser after ALL tests in this suite
Suite Setup       Open Browser And Navigate To Application
Suite Teardown    Close Browser Session


*** Test Cases ***

# ---------------------------------------------------------
# Test Case : TC_001 - Valid User Login And Logout
# Description: End-to-end login flow using valid credentials.
#   Steps:
#     1. Input valid credentials and submit the login form.
#     2. Verify the user is redirected to the landing page
#        by confirming the logout button is visible.
#     3. Log out and confirm return to the login page.
# Expected  : Login succeeds and logout returns to login page.
# ---------------------------------------------------------
TC_001 - Valid User Login And Logout
    [Documentation]    Verifies that a valid user can log in
    ...                successfully and then log out cleanly.
    [Tags]    login    smoke

    # Step 1: Input credentials and submit the form
    Login To Application    ${USERNAME}    ${PASSWORD}

    # Step 2: Confirm the login was successful
    Verify Login Is Successful

    # Step 3: Log out of the application
    Logout From Application
