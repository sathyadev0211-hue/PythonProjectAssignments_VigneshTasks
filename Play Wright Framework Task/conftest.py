"""
conftest.py – Pytest configuration and shared fixtures.

Fixtures defined here are automatically available to every test file
in the project without any explicit import.
"""

import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page


# ── Browser-level fixture (one browser per test session) ──────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    """
    Launch a Chromium browser once for the entire test session
    and close it when all tests are done.
    """
    with sync_playwright() as pw:
        browser: Browser = pw.chromium.launch(headless=True)
        yield browser
        browser.close()


# ── Context-level fixture (fresh browser context per test) ────────────────────

@pytest.fixture(scope="function")
def browser_context(browser_instance: Browser):
    """
    Create a new isolated browser context for every individual test.
    This guarantees clean cookies / local-storage between tests.
    """
    context: BrowserContext = browser_instance.new_context(
        viewport={"width": 1280, "height": 720}
    )
    yield context
    context.close()


# ── Page-level fixture (new page per test) ────────────────────────────────────

@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Page:
    """
    Open a new page inside the browser context.
    Every test receives its own fresh page object.
    """
    new_page: Page = browser_context.new_page()
    yield new_page
    new_page.close()
