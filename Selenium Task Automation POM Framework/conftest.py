"""
conftest.py
-----------
Pytest configuration file.
Provides shared fixtures for WebDriver initialization and teardown.
Uses Page Object Model (POM) pattern with Explicit Waits.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# ──────────────────────────────────────────────
# Fixture: WebDriver (session-scoped per test)
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """
    Initialize Chrome WebDriver with headless options.
    Yields the driver to the test, then quits after the test completes.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")          # Run headless (no UI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")

    # Initialize WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)  # Fallback implicit wait (Explicit Waits take priority)

    yield driver  # Provide driver to the test

    # Teardown: quit browser after each test
    driver.quit()
