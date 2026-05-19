*** Settings ***
# ============================================================
# TC3_add_product_to_cart.robot
# Test Case 3: After logging in with valid credentials, add
# a product to the cart and verify it is correctly listed.
# ============================================================

Library     SeleniumLibrary
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

Suite Setup       Open Browser And Navigate To SauceDemo
Suite Teardown    Close Test Browser


*** Test Cases ***

TC3 - Add Single Product To Cart And Verify
    [Documentation]    Verify that after a successful login, adding a single product
    ...                to the cart updates the cart badge and the product appears in the cart.
    [Tags]    cart    smoke    add-to-cart

    # Step 1: Log in with valid credentials
    Login With Valid Credentials

    # Step 2: Confirm landing on the Products page
    Verify User Is On Products Page

    # Step 3: Add the first product (Sauce Labs Backpack) to the cart
    Add Single Product To Cart

    # Step 4: Verify the cart badge shows count of 1
    Verify Cart Badge Count    1

    # Step 5: Navigate to the Cart page and confirm the product is listed
    Verify Product Is In Cart    ${PRODUCT_1_NAME}
