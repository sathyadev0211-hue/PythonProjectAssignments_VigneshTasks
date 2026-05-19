*** Settings ***
# ============================================================
# TC1_valid_login.robot
# Test Case 1: Login with valid credentials and verify the
# user is redirected to the Products page.
#
# Credentials used:
#   Username : standard_user
#   Password : secret_sauce
# ============================================================

Library     SeleniumLibrary
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

Suite Setup       Open Browser And Navigate To SauceDemo
Suite Teardown    Close Test Browser


*** Test Cases ***

TC1 - Valid Login Redirects To Products Page
    [Documentation]    Verify that logging in with valid credentials (standard_user / secret_sauce)
    ...                successfully authenticates the user and redirects them to the Products page.
    [Tags]    login    smoke    valid

    # Step 1: Perform login with valid credentials
    Login With Valid Credentials

    # Step 2: Confirm the user has landed on the Products page
    Verify User Is On Products Page

    # Step 3: Confirm at least one product item is rendered on the page
    Page Should Contain Element    ${PRODUCT_ITEM}
