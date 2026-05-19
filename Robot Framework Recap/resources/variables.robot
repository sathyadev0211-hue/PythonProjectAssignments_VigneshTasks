*** Variables ***
# ============================================================
# variables.robot
# Centralized variable definitions for SauceDemo automation.
# Includes URLs, credentials, timeouts, and locators.
# ============================================================

# --- Application URL ---
${BASE_URL}             https://www.saucedemo.com/
${PRODUCTS_URL}         https://www.saucedemo.com/inventory.html
${CART_URL}             https://www.saucedemo.com/cart.html
${CHECKOUT_URL}         https://www.saucedemo.com/checkout-step-one.html

# --- Valid Credentials ---
${VALID_USERNAME}       standard_user
${VALID_PASSWORD}       secret_sauce

# --- Invalid Credentials ---
${INVALID_USERNAME}     invalid_user
${INVALID_PASSWORD}     wrong_password

# --- Browser Configuration ---
${BROWSER}              chrome
${TIMEOUT}              15s
${IMPLICIT_WAIT}        10s

# --- Login Page Locators ---
${USERNAME_FIELD}       id=user-name
${PASSWORD_FIELD}       id=password
${LOGIN_BUTTON}         id=login-button
${ERROR_MESSAGE}        css=.error-message-container h3

# --- Products Page Locators ---
${PRODUCTS_HEADER}      css=.title
${PRODUCT_ITEM}         css=.inventory_item
${ADD_TO_CART_BTN_1}    id=add-to-cart-sauce-labs-backpack
${ADD_TO_CART_BTN_2}    id=add-to-cart-sauce-labs-bike-light
${ADD_TO_CART_BTN_3}    id=add-to-cart-sauce-labs-bolt-t-shirt
${CART_BADGE}           css=.shopping_cart_badge
${CART_ICON}            css=.shopping_cart_link

# --- Cart Page Locators ---
${CART_ITEM}            css=.cart_item
${CART_ITEM_NAME}       css=.inventory_item_name
${CHECKOUT_BUTTON}      id=checkout

# --- Checkout Page Locators ---
${FIRST_NAME_FIELD}     id=first-name
${LAST_NAME_FIELD}      id=last-name
${ZIP_CODE_FIELD}       id=postal-code
${CONTINUE_BUTTON}      id=continue
${SUMMARY_ITEM}         css=.cart_item
${FINISH_BUTTON}        id=finish

# --- Product Names ---
${PRODUCT_1_NAME}       Sauce Labs Backpack
${PRODUCT_2_NAME}       Sauce Labs Bike Light
${PRODUCT_3_NAME}       Sauce Labs Bolt T-Shirt

# --- Expected Error Messages ---
${INVALID_CREDS_ERROR}      Epic sadface: Username and password do not match any user in this service
${LOCKED_USER_ERROR}        Epic sadface: Sorry, this user has been locked out.
