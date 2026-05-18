"""
Page Object Model for the World Population Clock page.
URL: https://www.theworldcounts.com/challenges/planet-earth/state-of-the-planet/world-population-clock-live
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WorldPopulationPage:
    """
    Page Object Model class encapsulating all locators and interactions
    for the World Population Clock Live page.
    """

    # ---------------------------------------------------------------
    # Constants
    # ---------------------------------------------------------------
    URL = (
        "https://www.theworldcounts.com/challenges/planet-earth/"
        "state-of-the-planet/world-population-clock-live"
    )

    # XPath locator for the live population counter element
    POPULATION_COUNT_XPATH = (
        "//div[contains(@class,'count') or contains(@class,'counter') "
        "or contains(@class,'odometer') or contains(@class,'number')]"
        "[normalize-space(text()) != '']"
    )

    # Fallback XPath — targets any large numeric display on the page
    POPULATION_COUNT_FALLBACK_XPATH = (
        "//*[contains(@class,'count')]"
    )

    # ---------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------
    def __init__(self, driver, timeout: int = 20):
        """
        Initialise the page object.

        :param driver:  Selenium WebDriver instance
        :param timeout: Maximum wait time (seconds) for Explicit Waits
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # ---------------------------------------------------------------
    # Navigation
    # ---------------------------------------------------------------
    def open(self) -> None:
        """Navigate to the World Population Clock Live page."""
        self.driver.get(self.URL)

    # ---------------------------------------------------------------
    # Element retrieval helpers
    # ---------------------------------------------------------------
    def _get_population_element(self):
        """
        Wait for and return the population counter WebElement.
        Tries the primary XPath first; falls back to the secondary one.
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.POPULATION_COUNT_XPATH)
                )
            )
            return element
        except Exception:
            # Fallback locator
            element = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, self.POPULATION_COUNT_FALLBACK_XPATH)
                )
            )
            return element

    # ---------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------
    def get_population_count(self) -> str:
        """
        Extract and return the current live population count as a string.

        :returns: Population count text (digits only, stripped of whitespace)
        """
        element = self._get_population_element()
        raw_text = element.text.strip()
        # Keep only digits so the value is clean regardless of formatting
        digits_only = "".join(filter(str.isdigit, raw_text))
        return digits_only if digits_only else raw_text

    def get_page_title(self) -> str:
        """Return the current page <title> text."""
        return self.driver.title
