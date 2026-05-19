*** Settings ***
# ============================================================
# TC4_checkout_multiple_products.robot
# Test Case 4: Log in with valid credentials, add multiple
# products to the cart, proceed to checkout, and verify that
# the correct items and quantities appear in the checkout summary.
# ============================================================

Library     SeleniumLibrary
Resource    ../resources/keywords.robot
Resource    ../resources/variables.robot

Suite Setup       Open Browser And Navigate To SauceDemo
Suite Teardown    Close Test Browser


*** Test Cases ***

TC4 - Add Multiple Products And Verify Checkout Summary
    [Documentation]    Verify that adding multiple products to the cart and proceeding
    ...                through checkout correctly displays all items in the order summary.
    [Tags]    cart    checkout    e2e

    # Step 1: Log in with valid credentials
    Login With Valid Credentials

    # Step 2: Confirm landing on the Products page
    Verify User Is On Products Page

    # Step 3: Add three products to the cart
    Add Multiple Products To Cart

    # Step 4: Verify the cart badge reflects 3 items
    Verify Cart Badge Count    3

    # Step 5: Open the cart and confirm all three products are listed
    Verify Multiple Products In Cart
    ...    ${PRODUCT_1_NAME}
    ...    ${PRODUCT_2_NAME}
    ...    ${PRODUCT_3_NAME}

    # Step 6: Click the Checkout button to begin the checkout flow
    Proceed To Checkout

    # Step 7: Fill in the required shipping / contact information
    Fill Checkout Information    John    Doe    600001

    # Step 8: Verify the checkout overview page lists all added products
    Verify Checkout Summary Contains Products
    ...    ${PRODUCT_1_NAME}
    ...    ${PRODUCT_2_NAME}
    ...    ${PRODUCT_3_NAME}
