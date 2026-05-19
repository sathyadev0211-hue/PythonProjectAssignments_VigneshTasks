# conftest.py
# Pytest configuration file for OrangeHRM Login Automation
# Provides shared fixtures for WebDriver setup and teardown

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def pytest_configure(config):
    """Register custom markers to avoid warnings."""
    config.addinivalue_line("markers", "login: mark test as a login test")


@pytest.fixture(scope="function")
def driver():
    """
    Fixture: Initializes and returns a Chrome WebDriver instance.
    Scope is 'function' so each test gets a fresh browser.
    Teardown quits the driver after each test automatically.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")           # Open browser maximized
    chrome_options.add_argument("--disable-notifications")     # Suppress browser notifications
    chrome_options.add_argument("--disable-popup-blocking")    # Prevent popup blocks

    # Initialize Chrome WebDriver (ChromeDriver must be in PATH)
    driver_instance = webdriver.Chrome(options=chrome_options)

    yield driver_instance  # Provide driver to the test

    # Teardown: quit browser after test completes
    driver_instance.quit()
