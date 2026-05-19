*** Settings ***
# ============================================================
# keywords.robot
# Reusable keyword definitions for SauceDemo automation.
# Contains all action keywords grouped by functionality:
#   - Browser Setup / Teardown
#   - Login Actions
#   - Product / Cart Actions
#   - Checkout Actions
#   - Verification Keywords
# ============================================================

Library     SeleniumLibrary
Resource    variables.robot


*** Keywords ***

# -------------------------------------------------------
# BROWSER SETUP / TEARDOWN
# -------------------------------------------------------

Open Browser And Navigate To SauceDemo
    [Documentation]    Opens the configured browser, maximizes the window,
    ...                sets implicit wait, and navigates to the SauceDemo URL.
    Open Browser        ${BASE_URL}     ${BROWSER}
    Maximize Browser Window
    Set Selenium Implicit Wait    ${IMPLICIT_WAIT}
    Wait Until Page Contains Element    ${USERNAME_FIELD}    timeout=${TIMEOUT}

Close Test Browser
    [Documentation]    Captures a screenshot for evidence and closes the browser.
    Capture Page Screenshot
    Close Browser


# -------------------------------------------------------
# LOGIN ACTIONS
# -------------------------------------------------------

Enter Username
    [Documentation]    Clears the username field and types the provided username.
    [Arguments]    ${username}
    Clear Element Text    ${USERNAME_FIELD}
    Input Text    ${USERNAME_FIELD}    ${username}

Enter Password
    [Documentation]    Clears the password field and types the provided password.
    [Arguments]    ${password}
    Clear Element Text    ${PASSWORD_FIELD}
    Input Text    ${PASSWORD_FIELD}    ${password}

Click Login Button
    [Documentation]    Clicks the login submit button.
    Click Button    ${LOGIN_BUTTON}

Login With Credentials
    [Documentation]    Performs a full login action using the supplied username and password.
    ...                Enters credentials and submits the login form.
    [Arguments]    ${username}    ${password}
    Enter Username    ${username}
    Enter Password    ${password}
    Click Login Button

Login With Valid Credentials
    [Documentation]    Logs in using the predefined valid (standard_user) credentials.
    Login With Credentials    ${VALID_USERNAME}    ${VALID_PASSWORD}

Login With Invalid Credentials
    [Documentation]    Attempts login using predefined invalid credentials to trigger an error.
    Login With Credentials    ${INVALID_USERNAME}    ${INVALID_PASSWORD}

Logout From Application
    [Documentation]    Opens the burger menu and clicks Logout to end the session.
    Click Element       id=react-burger-menu-btn
    Wait Until Element Is Visible    id=logout_sidebar_link    timeout=${TIMEOUT}
    Click Element       id=logout_sidebar_link
    Wait Until Page Contains Element    ${USERNAME_FIELD}    timeout=${TIMEOUT}


# -------------------------------------------------------
# VERIFICATION KEYWORDS
# -------------------------------------------------------

Verify User Is On Products Page
    [Documentation]    Asserts that the Products page header is visible,
    ...                confirming a successful login redirect.
    Wait Until Page Contains Element    ${PRODUCTS_HEADER}    timeout=${TIMEOUT}
    Element Text Should Be    ${PRODUCTS_HEADER}    Products
    Location Should Be    ${PRODUCTS_URL}

Verify Error Message Is Displayed
    [Documentation]    Asserts that the login error container is visible
    ...                and contains the expected error text.
    [Arguments]    ${expected_message}
    Wait Until Element Is Visible    ${ERROR_MESSAGE}    timeout=${TIMEOUT}
    Element Text Should Be    ${ERROR_MESSAGE}    ${expected_message}

Verify Cart Badge Count
    [Documentation]    Checks that the cart badge displays the expected item count.
    [Arguments]    ${expected_count}
    Wait Until Element Is Visible    ${CART_BADGE}    timeout=${TIMEOUT}
    Element Text Should Be    ${CART_BADGE}    ${expected_count}

Verify Product Is In Cart
    [Documentation]    Navigates to the Cart page and confirms the given product name is listed.
    [Arguments]    ${product_name}
    Go To    ${CART_URL}
    Wait Until Page Contains Element    ${CART_ITEM}    timeout=${TIMEOUT}
    Page Should Contain    ${product_name}

Verify Multiple Products In Cart
    [Documentation]    Navigates to the Cart page and confirms each product in the supplied list is present.
    [Arguments]    @{product_names}
    Go To    ${CART_URL}
    Wait Until Page Contains Element    ${CART_ITEM}    timeout=${TIMEOUT}
    FOR    ${product}    IN    @{product_names}
        Page Should Contain    ${product}
    END

Verify Checkout Summary Contains Products
    [Documentation]    On the checkout overview page, asserts each product in the list is displayed.
    [Arguments]    @{product_names}
    Wait Until Page Contains Element    ${SUMMARY_ITEM}    timeout=${TIMEOUT}
    FOR    ${product}    IN    @{product_names}
        Page Should Contain    ${product}
    END


# -------------------------------------------------------
# PRODUCT / CART ACTIONS
# -------------------------------------------------------

Add Product To Cart
    [Documentation]    Clicks the "Add to Cart" button for a given product by its button locator.
    [Arguments]    ${add_to_cart_locator}
    Wait Until Element Is Visible    ${add_to_cart_locator}    timeout=${TIMEOUT}
    Click Button    ${add_to_cart_locator}

Add Single Product To Cart
    [Documentation]    Adds the first product (Sauce Labs Backpack) to the cart.
    Add Product To Cart    ${ADD_TO_CART_BTN_1}

Add Multiple Products To Cart
    [Documentation]    Adds three products (Backpack, Bike Light, Bolt T-Shirt) to the cart sequentially.
    Add Product To Cart    ${ADD_TO_CART_BTN_1}
    Add Product To Cart    ${ADD_TO_CART_BTN_2}
    Add Product To Cart    ${ADD_TO_CART_BTN_3}

Navigate To Cart
    [Documentation]    Clicks the cart icon to open the shopping cart page.
    Click Element    ${CART_ICON}
    Wait Until Page Contains Element    ${CHECKOUT_BUTTON}    timeout=${TIMEOUT}


# -------------------------------------------------------
# CHECKOUT ACTIONS
# -------------------------------------------------------

Proceed To Checkout
    [Documentation]    Clicks the Checkout button from the Cart page to begin checkout.
    Click Button    ${CHECKOUT_BUTTON}
    Wait Until Page Contains Element    ${FIRST_NAME_FIELD}    timeout=${TIMEOUT}

Fill Checkout Information
    [Documentation]    Fills in the shipping information form fields required for checkout.
    [Arguments]    ${first_name}    ${last_name}    ${zip_code}
    Input Text    ${FIRST_NAME_FIELD}    ${first_name}
    Input Text    ${LAST_NAME_FIELD}     ${last_name}
    Input Text    ${ZIP_CODE_FIELD}      ${zip_code}
    Click Button  ${CONTINUE_BUTTON}
