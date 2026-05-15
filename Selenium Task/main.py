"""
Task - 12: Dynamic XPath on https://www.guvi.in/
This module contains pytest test cases to validate Dynamic XPath usage
on the GUVI web application navbar elements.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture(scope="module")
def driver():
    """Set up Chrome WebDriver and navigate to guvi.in."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")          # Run headless (no UI window)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.guvi.in/")

    # Wait until the navbar is loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//nav"))
    )

    yield driver
    driver.quit()


# ─────────────────────────────────────────────
# Section 3: Relative XPath Tests
# ─────────────────────────────────────────────

class TestRelativeXPath:
    """Test cases using Relative XPath on the GUVI navbar."""

    def test_find_parent_and_first_child_of_courses(self, driver):
        """
        Relative XPath:
        Given the 'Courses' nav link (underlined in red in the task image),
        find its parent element and then locate the first child of that parent.
        """
        # Locate the 'Courses' link element (the highlighted element in the task)
        courses_element = driver.find_element(
            By.XPATH, "//a[normalize-space(text())='Courses']"
        )
        assert courses_element is not None, "Courses element not found"

        # Find the parent element using relative XPath (..)
        parent_element = driver.find_element(
            By.XPATH, "//a[normalize-space(text())='Courses']/.."
        )
        assert parent_element is not None, "Parent element of 'Courses' not found"
        print(f"\n[Relative XPath] Parent tag: {parent_element.tag_name}")

        # Find the first child of that parent using relative XPath
        first_child = driver.find_element(
            By.XPATH, "//a[normalize-space(text())='Courses']/../*[1]"
        )
        assert first_child is not None, "First child of parent not found"
        print(f"[Relative XPath] First child tag: {first_child.tag_name}, "
              f"text: {first_child.text.strip()}")

    def test_locate_second_sibling_of_courses(self, driver):
        """
        Relative XPath:
        Locate the second sibling of the 'Courses' element.
        Uses following-sibling axis with position index [2].
        """
        # Get the second following sibling of 'Courses'
        second_sibling = driver.find_elements(
            By.XPATH,
            "//a[normalize-space(text())='Courses']/following-sibling::*"
        )

        if len(second_sibling) >= 2:
            print(f"\n[Relative XPath] Second sibling tag: {second_sibling[1].tag_name}, "
                  f"text: {second_sibling[1].text.strip()}")
            assert second_sibling[1] is not None, "Second sibling not found"
        else:
            pytest.skip("Less than 2 siblings found for 'Courses' element")

    def test_select_parent_of_href_element(self, driver):
        """
        Relative XPath:
        Select the parent element of an element that has the attribute 'href'.
        Targets the first anchor tag with an href inside the navbar.
        """
        # Find the parent of the first element with 'href' attribute in the navbar
        parent_of_href = driver.find_element(
            By.XPATH, "(//nav//a[@href])[1]/.."
        )
        assert parent_of_href is not None, "Parent of href element not found"
        print(f"\n[Relative XPath] Parent of href element - tag: {parent_of_href.tag_name}")


# ─────────────────────────────────────────────
# Section 4: Axes Tests
# ─────────────────────────────────────────────

class TestAxes:
    """Test cases using XPath Axes on the GUVI navbar."""

    def test_find_all_ancestor_elements(self, driver):
        """
        Axes:
        Find all ancestor elements of the 'Courses' nav link.
        Uses the 'ancestor::' axis to traverse up the DOM tree.
        """
        ancestors = driver.find_elements(
            By.XPATH, "//a[normalize-space(text())='Courses']/ancestor::*"
        )
        assert len(ancestors) > 0, "No ancestor elements found"
        print(f"\n[Axes] Total ancestors of 'Courses': {len(ancestors)}")
        for i, ancestor in enumerate(ancestors, 1):
            print(f"  Ancestor {i}: <{ancestor.tag_name}>")

    def test_locate_all_following_siblings(self, driver):
        """
        Axes:
        Locate all following siblings of the 'Courses' nav link.
        Uses the 'following-sibling::' axis.
        """
        following_siblings = driver.find_elements(
            By.XPATH, "//a[normalize-space(text())='Courses']/following-sibling::*"
        )
        assert len(following_siblings) > 0, "No following siblings found"
        print(f"\n[Axes] Total following siblings of 'Courses': {len(following_siblings)}")
        for i, sibling in enumerate(following_siblings, 1):
            print(f"  Sibling {i}: <{sibling.tag_name}> - {sibling.text.strip()}")

    def test_select_all_preceding_elements(self, driver):
        """
        Axes:
        Select all preceding elements of the 'Login' nav link.
        Uses the 'preceding::' axis to get all elements that appear before it in the DOM.
        """
        # Using 'Login' button as reference point for preceding elements
        preceding_elements = driver.find_elements(
            By.XPATH, "//a[normalize-space(text())='Login']/preceding::*"
        )
        assert len(preceding_elements) > 0, "No preceding elements found"
        print(f"\n[Axes] Total preceding elements before 'Login': {len(preceding_elements)}")
        # Print just the last 5 for brevity
        for elem in preceding_elements[-5:]:
            print(f"  Preceding: <{elem.tag_name}> - {elem.text.strip()[:40]}")
