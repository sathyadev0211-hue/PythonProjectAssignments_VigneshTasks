"""
Base Page class providing common methods for all page objects.
Implements explicit wait strategies using Playwright.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """
    Base class for all Page Object Models.
    Provides reusable utility methods with explicit waits.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to a given URL and wait until the page is fully loaded."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """
        Explicit wait: wait for an element to be visible on the page.

        Args:
            selector: CSS or text selector for the element.
            timeout:  Maximum wait time in milliseconds (default 10 s).
        """
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)
        return self.page.locator(selector)

    def is_element_visible(self, selector: str) -> bool:
        """Return True if the element identified by selector is visible."""
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=5000)
            return True
        except Exception:
            return False
