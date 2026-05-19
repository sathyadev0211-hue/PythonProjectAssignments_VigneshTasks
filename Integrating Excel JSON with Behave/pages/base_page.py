"""
base_page.py
------------
Base Page class implementing common Selenium interactions.
Uses Python OOP principles and Selenium exception handling.
All page classes inherit from this base class (Page Object Model).
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    WebDriverException
)
import allure


class BasePage:
    """
    Base Page class providing reusable browser interaction methods.
    All page-specific classes inherit from this class.
    """

    # Default explicit wait timeout in seconds
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver):
        """
        Initialize BasePage with a Selenium WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(self.driver, self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate_to(self, url: str) -> None:
        """
        Navigate the browser to the specified URL.

        Args:
            url (str): The URL to navigate to.

        Raises:
            WebDriverException: If navigation fails.
        """
        try:
            self.driver.get(url)
            allure.attach(
                f"Navigated to: {url}",
                name="Navigation",
                attachment_type=allure.attachment_type.TEXT
            )
        except WebDriverException as e:
            allure.attach(
                f"Navigation failed to {url}: {str(e)}",
                name="Navigation Error",
                attachment_type=allure.attachment_type.TEXT
            )
            raise WebDriverException(
                f"Failed to navigate to URL '{url}': {str(e)}"
            ) from e

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Return the current page title."""
        return self.driver.title

    # ------------------------------------------------------------------
    # Element Interactions
    # ------------------------------------------------------------------

    def find_element(self, locator: tuple):
        """
        Wait for and return a web element located by the given locator.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Returns:
            WebElement: The found element.

        Raises:
            TimeoutException: If element is not found within timeout.
            NoSuchElementException: If element does not exist on page.
        """
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException as e:
            raise TimeoutException(
                f"Element not found within {self.DEFAULT_TIMEOUT}s "
                f"using locator: {locator}"
            ) from e
        except NoSuchElementException as e:
            raise NoSuchElementException(
                f"No such element with locator: {locator}"
            ) from e

    def find_clickable_element(self, locator: tuple):
        """
        Wait for an element to be clickable and return it.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Returns:
            WebElement: The clickable element.

        Raises:
            TimeoutException: If element is not clickable within timeout.
        """
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException as e:
            raise TimeoutException(
                f"Element not clickable within {self.DEFAULT_TIMEOUT}s "
                f"using locator: {locator}"
            ) from e

    def click_element(self, locator: tuple) -> None:
        """
        Click on a web element identified by the locator.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Raises:
            ElementClickInterceptedException: If click is intercepted.
            ElementNotInteractableException: If element is not interactable.
            TimeoutException: If element is not found/clickable.
        """
        try:
            element = self.find_clickable_element(locator)
            element.click()
        except ElementClickInterceptedException as e:
            raise ElementClickInterceptedException(
                f"Click intercepted on element with locator: {locator}"
            ) from e
        except ElementNotInteractableException as e:
            raise ElementNotInteractableException(
                f"Element not interactable with locator: {locator}"
            ) from e
        except StaleElementReferenceException as e:
            # Retry once on stale element
            element = self.find_clickable_element(locator)
            element.click()

    def enter_text(self, locator: tuple, text: str) -> None:
        """
        Clear existing text and enter new text into an input field.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.
            text (str): The text to enter into the field.

        Raises:
            ElementNotInteractableException: If element is not interactable.
            TimeoutException: If element is not found within timeout.
        """
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except ElementNotInteractableException as e:
            raise ElementNotInteractableException(
                f"Cannot enter text — element not interactable: {locator}"
            ) from e

    def is_element_visible(self, locator: tuple) -> bool:
        """
        Check whether an element is visible on the page.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Returns:
            bool: True if element is visible, False otherwise.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """
        Check whether an element is present in the DOM.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Returns:
            bool: True if element is present, False otherwise.
        """
        try:
            self.find_element(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def get_element_text(self, locator: tuple) -> str:
        """
        Retrieve the visible text of an element.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.

        Returns:
            str: The visible text content of the element.
        """
        element = self.find_element(locator)
        return element.text.strip()

    def get_element_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Retrieve a specific attribute value from an element.

        Args:
            locator (tuple): A (By.*, 'selector') tuple.
            attribute (str): The attribute name (e.g., 'value', 'placeholder').

        Returns:
            str: The attribute value.
        """
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    # ------------------------------------------------------------------
    # Screenshot utility
    # ------------------------------------------------------------------

    def take_screenshot(self, name: str = "screenshot") -> None:
        """
        Capture a screenshot and attach it to the Allure report.

        Args:
            name (str): Label for the screenshot in the Allure report.
        """
        try:
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except WebDriverException as e:
            print(f"[Warning] Could not capture screenshot: {e}")
