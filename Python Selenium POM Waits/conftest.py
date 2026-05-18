"""
conftest.py — Pytest fixtures shared across all test modules.

Sets up and tears down the Selenium WebDriver instance.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped WebDriver fixture.

    Launches a Chrome browser once per test session and quits it
    after all tests in the session have finished.
    """
    chrome_options = Options()

    # Run headless so it works on CI / servers without a display
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # ChromeDriver must be on PATH (or pass executable_path= to Service)
    service = Service()
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.implicitly_wait(0)  # We rely solely on Explicit Waits

    yield browser  # Hand the driver to every test that requests it

    browser.quit()  # Teardown: close browser after all tests finish
