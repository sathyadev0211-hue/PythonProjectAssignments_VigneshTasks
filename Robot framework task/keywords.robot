*** Settings ***
# ---------------------------------------------------------
# Resource File: keywords.robot
# Description  : Contains reusable keywords for the Robot
#                Spare Bin Industries web application tests.
# Libraries    : SeleniumLibrary for browser/UI interactions
#                BuiltIn for standard operations (implicit)
# ---------------------------------------------------------
Library    SeleniumLibrary


*** Variables ***
# Application URL and browser configuration
${URL}              https://robotsparebinindustries.com
${BROWSER}          chrome
${TIMEOUT}          10s

# Login credentials (valid test user)
${USERNAME}         maria
${PASSWORD}         thoushallnotpass

# Locators for login page elements
${USERNAME_FIELD}   id:username
${PASSWORD_FIELD}   id:password
${LOGIN_BUTTON}     css:button[type="submit"]

# Locator to verify successful login (element present on landing page)
${LOGOUT_BUTTON}    id:logout-button


*** Keywords ***

# ---------------------------------------------------------
# Keyword   : Open Browser And Navigate To Application
# Description: Launches the browser, maximizes the window,
#              sets implicit wait timeout, and navigates to
#              the application URL.
# ---------------------------------------------------------
Open Browser And Navigate To Application
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    Wait Until Page Contains Element    ${USERNAME_FIELD}
    Log    Browser opened and navigated to: ${URL}


# ---------------------------------------------------------
# Keyword   : Login To Application
# Arguments : ${username} - the login username
#             ${password} - the login password
# Description: Clears any pre-filled values, inputs the
#              provided credentials into the login form,
#              and submits it by clicking the login button.
# ---------------------------------------------------------
Login To Application
    [Arguments]    ${username}    ${password}
    # Clear fields before entering credentials (defensive step)
    Clear Element Text    ${USERNAME_FIELD}
    Input Text            ${USERNAME_FIELD}    ${username}
    Clear Element Text    ${PASSWORD_FIELD}
    Input Text            ${PASSWORD_FIELD}    ${password}
    # Click the submit button to trigger login
    Click Button          ${LOGIN_BUTTON}
    Log    Login attempted with username: ${username}


# ---------------------------------------------------------
# Keyword   : Verify Login Is Successful
# Description: Confirms a successful login by checking that
#              the logout button is visible on the landing
#              page, which only appears after authentication.
# ---------------------------------------------------------
Verify Login Is Successful
    # The logout button is only present when the user is logged in
    Wait Until Element Is Visible    ${LOGOUT_BUTTON}    timeout=${TIMEOUT}
    Element Should Be Visible        ${LOGOUT_BUTTON}
    Log    Login verified successfully — logout button is present on the page.


# ---------------------------------------------------------
# Keyword   : Logout From Application
# Description: Clicks the logout button to end the user
#              session and verifies the login form is shown
#              again, confirming a clean logout.
# ---------------------------------------------------------
Logout From Application
    # Click logout to terminate the session
    Click Button    ${LOGOUT_BUTTON}
    # After logout, the username field should reappear on the login page
    Wait Until Element Is Visible    ${USERNAME_FIELD}    timeout=${TIMEOUT}
    Log    Logout successful — login page is displayed again.


# ---------------------------------------------------------
# Keyword   : Close Browser Session
# Description: Closes all open browser windows and cleans
#              up the WebDriver session gracefully.
# ---------------------------------------------------------
Close Browser Session
    Close All Browsers
    Log    Browser session closed.
