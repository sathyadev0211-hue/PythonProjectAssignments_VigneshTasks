"""
Task - 13: Selenium Automation - Drag and Drop Operation
URL: https://jqueryui.com/droppable/
Description: Automates drag and drop of the White Rectangular Box into the
             Yellow Rectangular Box using Python Selenium and Action Chains.
             Includes both Positive and Negative test cases with Pytest HTML report.
"""

import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException,
)


# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
TARGET_URL = "https://jqueryui.com/droppable/"
IFRAME_LOCATOR = (By.CLASS_NAME, "demo-frame")
DRAGGABLE_LOCATOR = (By.ID, "draggable")
DROPPABLE_LOCATOR = (By.ID, "droppable")
DROP_SUCCESS_TEXT = "Dropped!"
IMPLICIT_WAIT = 10  # seconds
PAGE_LOAD_TIMEOUT = 20  # seconds


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────
@pytest.fixture(scope="function")
def driver():
    """
    Set up a Chrome WebDriver instance for each test function.
    Yields the driver and ensures the browser is closed after each test.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # Uncomment the line below to run headlessly in CI/CD environments
    # chrome_options.add_argument("--headless")

    browser = webdriver.Chrome(options=chrome_options)
    browser.implicitly_wait(IMPLICIT_WAIT)
    browser.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    yield browser  # Provide the driver to the test

    browser.quit()  # Teardown: close browser after each test


@pytest.fixture(scope="function")
def driver_on_page(driver):
    """
    Navigate to the target URL and switch into the demo iframe.
    Returns (driver, draggable_element, droppable_element).
    """
    # Navigate to the droppable demo page
    driver.get(TARGET_URL)

    # Wait for the iframe containing the demo to be present
    wait = WebDriverWait(driver, IMPLICIT_WAIT)
    iframe = wait.until(EC.presence_of_element_located(IFRAME_LOCATOR))

    # Switch context into the iframe
    driver.switch_to.frame(iframe)

    # Locate the draggable (white box) and droppable (yellow box) elements
    draggable = wait.until(EC.presence_of_element_located(DRAGGABLE_LOCATOR))
    droppable = wait.until(EC.presence_of_element_located(DROPPABLE_LOCATOR))

    return driver, draggable, droppable


# ──────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────
def perform_drag_and_drop(driver, source, target):
    """
    Perform a drag-and-drop action from source element to target element
    using ActionChains.
    """
    actions = ActionChains(driver)
    actions.drag_and_drop(source, target).perform()
    time.sleep(0.5)  # Brief pause to let the UI update


# ──────────────────────────────────────────────
# Positive Test Cases
# ──────────────────────────────────────────────
class TestDragAndDropPositive:
    """
    Positive test cases: verify that drag and drop works as expected
    when performed correctly.
    """

    def test_page_title_is_correct(self, driver):
        """
        TC-P-01: Verify that the page title contains 'Droppable'.
        Ensures the browser has landed on the correct page.
        """
        driver.get(TARGET_URL)
        assert "Droppable" in driver.title, (
            f"Expected 'Droppable' in page title, got: '{driver.title}'"
        )

    def test_draggable_element_is_present(self, driver_on_page):
        """
        TC-P-02: Verify that the draggable (white) box exists on the page.
        """
        _, draggable, _ = driver_on_page
        assert draggable.is_displayed(), "Draggable element is not visible on the page."

    def test_droppable_element_is_present(self, driver_on_page):
        """
        TC-P-03: Verify that the droppable (yellow) box exists on the page.
        """
        _, _, droppable = driver_on_page
        assert droppable.is_displayed(), "Droppable element is not visible on the page."

    def test_drag_and_drop_changes_text(self, driver_on_page):
        """
        TC-P-04 (Core): Drag the white box into the yellow box and confirm
        the drop zone text changes to 'Dropped!'.
        """
        driver, draggable, droppable = driver_on_page

        # Verify the initial state of the drop target
        initial_text = droppable.text
        assert DROP_SUCCESS_TEXT not in initial_text, (
            "Drop zone already shows 'Dropped!' before the drag action."
        )

        # Perform the drag-and-drop
        perform_drag_and_drop(driver, draggable, droppable)

        # Assert the drop zone updated its text
        updated_text = droppable.text
        assert DROP_SUCCESS_TEXT in updated_text, (
            f"Expected '{DROP_SUCCESS_TEXT}' after drop, but got: '{updated_text}'"
        )

    def test_drag_and_drop_changes_background_color(self, driver_on_page):
        """
        TC-P-05: After a successful drop, the droppable box background color
        should change (jQuery UI changes it to a darker green by default).
        """
        driver, draggable, droppable = driver_on_page

        # Capture background color before drop
        color_before = droppable.value_of_css_property("background-color")

        # Perform the drag-and-drop
        perform_drag_and_drop(driver, draggable, droppable)

        # Capture background color after drop
        color_after = droppable.value_of_css_property("background-color")

        assert color_before != color_after, (
            "Background color of the droppable box did not change after drop. "
            f"Before: {color_before}, After: {color_after}"
        )

    def test_draggable_initial_text(self, driver_on_page):
        """
        TC-P-06: Verify the draggable box displays 'Drag me to my target' initially.
        """
        _, draggable, _ = driver_on_page
        assert "Drag me" in draggable.text, (
            f"Unexpected initial text on draggable: '{draggable.text}'"
        )

    def test_droppable_initial_text(self, driver_on_page):
        """
        TC-P-07: Verify the droppable box displays 'Drop here' initially.
        """
        _, _, droppable = driver_on_page
        assert "Drop here" in droppable.text, (
            f"Unexpected initial text on droppable: '{droppable.text}'"
        )


# ──────────────────────────────────────────────
# Negative Test Cases
# ──────────────────────────────────────────────
class TestDragAndDropNegative:
    """
    Negative test cases: verify that the system handles incorrect/edge-case
    scenarios gracefully.
    """

    def test_wrong_url_raises_no_draggable_element(self, driver):
        """
        TC-N-01: Navigate to a wrong URL and confirm the draggable element
        is NOT found, ensuring the locator is page-specific.
        """
        driver.get("https://jqueryui.com/sortable/")  # Different jQuery UI demo

        # Switch into the demo iframe if present
        try:
            wait = WebDriverWait(driver, 5)
            iframe = wait.until(EC.presence_of_element_located(IFRAME_LOCATOR))
            driver.switch_to.frame(iframe)
        except TimeoutException:
            pass  # No iframe on this page is also fine

        # The draggable element (id="draggable") should NOT be present
        elements = driver.find_elements(*DRAGGABLE_LOCATOR)
        assert len(elements) == 0, (
            "Found a #draggable element on the wrong page — unexpected."
        )

    def test_drop_text_not_present_before_action(self, driver_on_page):
        """
        TC-N-02: Confirm 'Dropped!' text does NOT appear before performing
        the drag-and-drop (pre-condition validation).
        """
        _, _, droppable = driver_on_page
        assert DROP_SUCCESS_TEXT not in droppable.text, (
            "'Dropped!' text found before any drag-and-drop action was performed."
        )

    def test_drag_to_wrong_target_does_not_trigger_drop(self, driver_on_page):
        """
        TC-N-03: Attempt to drag the white box to a non-droppable area
        (the page body) and confirm 'Dropped!' is NOT shown.
        """
        driver, draggable, droppable = driver_on_page

        # Drag to the body element (outside the drop zone)
        body = driver.find_element(By.TAG_NAME, "body")
        actions = ActionChains(driver)
        actions.drag_and_drop(draggable, body).perform()
        time.sleep(0.5)

        assert DROP_SUCCESS_TEXT not in droppable.text, (
            "Drop zone unexpectedly shows 'Dropped!' after dragging to the body."
        )

    def test_invalid_element_id_raises_exception(self, driver):
        """
        TC-N-04: Using a non-existent element ID should raise NoSuchElementException.
        Validates that the correct locators are used in the positive tests.
        """
        driver.get(TARGET_URL)

        wait = WebDriverWait(driver, IMPLICIT_WAIT)
        iframe = wait.until(EC.presence_of_element_located(IFRAME_LOCATOR))
        driver.switch_to.frame(iframe)

        # driver.implicitly_wait(0) to get an immediate failure
        driver.implicitly_wait(0)
        with pytest.raises(NoSuchElementException):
            driver.find_element(By.ID, "non_existent_element_id_xyz")

        # Restore implicit wait
        driver.implicitly_wait(IMPLICIT_WAIT)

    def test_page_load_with_javascript_disabled_scenario(self, driver):
        """
        TC-N-05: Verify the page title is NOT 'Droppable' when navigating
        to a completely different website (sanity / negative URL check).
        """
        driver.get("https://www.example.com")
        assert "Droppable" not in driver.title, (
            "Page title unexpectedly contains 'Droppable' for example.com."
        )
