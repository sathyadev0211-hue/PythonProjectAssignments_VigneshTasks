"""
test_world_population.py
========================
Pytest test suite for the World Population Clock Live page.

Tasks covered
-------------
1. Navigate to the target URL.
2. Continuously extract & print the live Population Count to the
   console until the user interrupts with CTRL+C.
3. All element locators use XPATH only (no CSS / ID / Name / etc.).

Usage
-----
Run all tests and generate an HTML report:
    pytest test_world_population.py -v --html=report.html --self-contained-html

Run only the continuous-print test (stops on CTRL+C):
    pytest test_world_population.py::TestWorldPopulation::test_extract_population_continuously -v -s
"""

import time
import pytest
from pages.world_population_page import WorldPopulationPage


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------
class TestWorldPopulation:
    """
    Test class for the World Population Clock Live page.
    Uses the Page Object Model pattern with Explicit Waits.
    """

    # ------------------------------------------------------------------
    # Test 1 — Verify successful page load
    # ------------------------------------------------------------------
    def test_page_title_is_not_empty(self, driver):
        """
        Verify that the page loads successfully by checking that
        the <title> is non-empty.
        """
        # Arrange: create the page object and open the URL
        page = WorldPopulationPage(driver)
        page.open()

        # Act: fetch the page title
        title = page.get_page_title()

        # Assert: title must be a non-empty string
        assert title, "Page title should not be empty after navigation."
        print(f"\n[INFO] Page title: {title}")

    # ------------------------------------------------------------------
    # Test 2 — Verify population count is extractable (single snapshot)
    # ------------------------------------------------------------------
    def test_population_count_is_numeric(self, driver):
        """
        Verify that the extracted population count contains only digits
        and is a plausible world-population figure (> 7 billion).
        """
        # Arrange
        page = WorldPopulationPage(driver)
        page.open()

        # Act: extract the population count
        population = page.get_population_count()

        # Assert 1: value must be non-empty
        assert population, "Population count should not be empty."

        # Assert 2: value must be all digits
        assert population.isdigit(), (
            f"Expected a numeric population count, got: '{population}'"
        )

        # Assert 3: plausibility check — world population > 7,000,000,000
        assert int(population) > 7_000_000_000, (
            f"Population count seems too low: {population}"
        )

        print(f"\n[INFO] Snapshot population count: {population}")

    # ------------------------------------------------------------------
    # Test 3 — Continuously print population until CTRL+C
    # ------------------------------------------------------------------
    def test_extract_population_continuously(self, driver):
        """
        Open the page and print the live population count to the
        terminal every second until the user presses CTRL+C.

        This test intentionally runs indefinitely; interrupt it with
        CTRL+C when you have observed enough output.
        """
        # Arrange
        page = WorldPopulationPage(driver)
        page.open()

        print("\n" + "=" * 60)
        print(" Live World Population Counter")
        print(" Press CTRL+C to stop.")
        print("=" * 60)

        iteration = 1
        try:
            while True:
                # Act: extract the current population count
                population = page.get_population_count()

                # Print formatted output to the console
                print(f"[Reading #{iteration:>6}]  Population: {population}")

                iteration += 1
                time.sleep(1)  # Wait 1 second before the next reading

        except KeyboardInterrupt:
            # Gracefully handle CTRL+C — this is expected behaviour
            print("\n[INFO] CTRL+C detected. Stopping population extraction.")
            print(f"[INFO] Total readings captured: {iteration - 1}")

        # The test passes as long as at least one reading was captured
        assert iteration > 1, "No population readings were captured."
