"""
pages/base_page.py
------------------
Base Page class for Page Object Model (POM).
Contains reusable methods with Explicit Waits used across all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)


class BasePage:
    """
    Base class that all page objects inherit from.
    Encapsulates common WebDriver interactions with Explicit Waits.
    """

    TIMEOUT = 15  # Default explicit wait timeout in seconds

    def __init__(self, driver):
        """Initialize BasePage with a WebDriver instance."""
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    # ──────────────────────────────────────────────
    # Navigation
    # ──────────────────────────────────────────────
    def open_url(self, url: str):
        """Navigate the browser to the given URL."""
        self.driver.get(url)

    def get_current_url(self) -> str:
        """Return the current page URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    # ──────────────────────────────────────────────
    # Element Interactions (with Explicit Wait)
    # ──────────────────────────────────────────────
    def find_element(self, locator: tuple):
        """
        Wait until element is present in DOM, then return it.
        :param locator: tuple (By.XX, 'selector')
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(
                f"[BasePage] Element not found within {self.TIMEOUT}s: {locator}"
            )

    def click_element(self, locator: tuple):
        """
        Wait until element is clickable, then click it.
        :param locator: tuple (By.XX, 'selector')
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except (TimeoutException, ElementNotInteractableException) as e:
            raise Exception(
                f"[BasePage] Could not click element {locator}: {e}"
            )

    def enter_text(self, locator: tuple, text: str):
        """
        Wait until element is visible, clear it, then type text.
        :param locator: tuple (By.XX, 'selector')
        :param text: string to type
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            raise TimeoutException(
                f"[BasePage] Input element not visible within {self.TIMEOUT}s: {locator}"
            )

    def get_element_text(self, locator: tuple) -> str:
        """
        Wait until element is visible, then return its text content.
        :param locator: tuple (By.XX, 'selector')
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element.text
        except TimeoutException:
            raise TimeoutException(
                f"[BasePage] Element text not available within {self.TIMEOUT}s: {locator}"
            )

    def is_element_visible(self, locator: tuple) -> bool:
        """
        Check if an element is visible on the page without raising an exception.
        :param locator: tuple (By.XX, 'selector')
        :return: True if visible, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """
        Check if an element exists in the DOM (not necessarily visible).
        :param locator: tuple (By.XX, 'selector')
        :return: True if present, False otherwise
        """
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def wait_for_url_contains(self, partial_url: str) -> bool:
        """
        Wait until the current URL contains the given string.
        :param partial_url: substring to look for in URL
        :return: True if matched, False on timeout
        """
        try:
            return self.wait.until(EC.url_contains(partial_url))
        except TimeoutException:
            return False
