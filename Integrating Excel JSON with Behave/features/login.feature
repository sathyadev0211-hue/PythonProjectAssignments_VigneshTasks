# login.feature
# BDD Feature file for Zen Portal Login and Logout functionality
# Uses Gherkin syntax with Behave framework

@zen_portal
Feature: Zen Portal Login and Logout

  As a registered user of the Zen Portal
  I want to be able to log in and log out securely
  So that I can access my learning content and protect my account

  Background:
    Given I have navigated to the Zen Portal login page

  # ---------------------------------------------------------------
  # Scenario 1: Validate UI elements on the login page
  # ---------------------------------------------------------------

  @validate_ui
  Scenario: Validate Username and Password input fields are present
    Then the Username input field should be visible
    And the Password input field should be visible

  @validate_ui
  Scenario: Validate Submit button is present and functional
    Then the Submit button should be present on the login page

  # ---------------------------------------------------------------
  # Scenario 2: Successful Login
  # ---------------------------------------------------------------

  @successful_login
  Scenario: Login to Zen Portal with valid credentials
    When I enter a valid username "<your_email@example.com>"
    And I enter a valid password "<your_password>"
    And I click the Submit button
    Then I should be logged in successfully

  # ---------------------------------------------------------------
  # Scenario 3: Unsuccessful Login
  # ---------------------------------------------------------------

  @unsuccessful_login
  Scenario: Login to Zen Portal with invalid credentials
    When I enter an invalid username "invalid_user@test.com"
    And I enter an invalid password "wrongpassword123"
    And I click the Submit button
    Then I should see a login error message

  # ---------------------------------------------------------------
  # Scenario 4: Logout functionality
  # ---------------------------------------------------------------

  @logout
  Scenario: Logout from Zen Portal after successful login
    When I enter a valid username "<your_email@example.com>"
    And I enter a valid password "<your_password>"
    And I click the Submit button
    Then I should be logged in successfully
    When I click the Logout button
    Then I should be logged out successfully

  @validate_ui
  Scenario: Validate the Logout button is present after login
    When I enter a valid username "<your_email@example.com>"
    And I enter a valid password "<your_password>"
    And I click the Submit button
    Then I should be logged in successfully
    And the Logout button should be visible on the page
