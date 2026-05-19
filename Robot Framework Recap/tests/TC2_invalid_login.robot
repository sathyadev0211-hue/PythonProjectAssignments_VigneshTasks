*** Settings ***
# ============================================================
# TC2_invalid_login.robot
# Test Case 2: Attempt login with invalid credentials and
# verify the appropriate error message is displayed.
# ============================================================

Library     SeleniumLibrary
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

Suite Setup       Open Browser And Navigate To SauceDemo
Suite Teardown    Close Test Browser


*** Test Cases ***

TC2 - Invalid Login Displays Error Message
    [Documentation]    Verify that submitting incorrect credentials prevents login
    ...                and shows the correct error message to the user.
    [Tags]    login    negative    error-handling

    # Step 1: Attempt login with invalid username and password
    Login With Invalid Credentials

    # Step 2: Verify the error message container is visible with correct text
    Verify Error Message Is Displayed    ${INVALID_CREDS_ERROR}

    # Step 3: Confirm the user has NOT been redirected (still on login page)
    Location Should Be    ${BASE_URL}
    Element Should Be Visible    ${LOGIN_BUTTON}
