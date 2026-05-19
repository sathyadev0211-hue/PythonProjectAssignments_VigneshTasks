"""
environment.py
--------------
Behave environment hooks for browser setup and teardown.
Runs before/after each scenario to manage WebDriver lifecycle.
Also integrates Allure reporting hooks.
"""

import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException
import allure


# -----------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------

ALLURE_RESULTS_DIR = "allure-results"
IMPLICIT_WAIT      = 5   # seconds
PAGE_LOAD_TIMEOUT  = 30  # seconds


# -----------------------------------------------------------------------
# Suite-level hooks
# -----------------------------------------------------------------------

def before_all(context):
    """
    Runs once before the entire test suite.
    Sets up Allure output directory and shared configuration.
    """
    # Ensure Allure results directory exists
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

    # Store base URL in context so steps can reference it
    context.base_url = "https://www.guvi.in/sign-in/"

    print("\n[INFO] Test suite started.")
    print(f"[INFO] Allure results will be stored in: {ALLURE_RESULTS_DIR}/")


def after_all(context):
    """
    Runs once after the entire test suite completes.
    Prints a reminder to generate the Allure HTML report.
    """
    print("\n[INFO] Test suite completed.")
    print("[INFO] To generate the Allure HTML report, run:")
    print("       allure generate allure-results --clean -o allure-report")
    print("       allure open allure-report")


# -----------------------------------------------------------------------
# Feature-level hooks
# -----------------------------------------------------------------------

def before_feature(context, feature):
    """Called before each feature file is executed."""
    print(f"\n[INFO] Starting feature: {feature.name}")


def after_feature(context, feature):
    """Called after each feature file finishes."""
    print(f"[INFO] Finished feature: {feature.name}")


# -----------------------------------------------------------------------
# Scenario-level hooks
# -----------------------------------------------------------------------

def before_scenario(context, scenario):
    """
    Called before each scenario.
    Initialises a fresh Chrome WebDriver instance.
    """
    print(f"\n[INFO] Starting scenario: {scenario.name}")

    try:
        # Configure Chrome options
        chrome_options = ChromeOptions()

        # Uncomment the line below to run headlessly (e.g. in CI)
        # chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-popup-blocking")

        # Initialise WebDriver
        # Uses locally installed ChromeDriver; replace with webdriver-manager
        # if you prefer automatic driver management:
        #   from webdriver_manager.chrome import ChromeDriverManager
        #   service = ChromeService(ChromeDriverManager().install())
        context.driver = webdriver.Chrome(options=chrome_options)

        # Set timeouts
        context.driver.implicitly_wait(IMPLICIT_WAIT)
        context.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

        # Maximise browser window
        context.driver.maximize_window()

    except WebDriverException as e:
        raise RuntimeError(
            f"WebDriver could not be initialised for scenario "
            f"'{scenario.name}': {e}"
        )


def after_scenario(context, scenario):
    """
    Called after each scenario completes.
    Captures a screenshot on failure and quits the WebDriver.
    """
    # Capture screenshot on failure and attach to Allure report
    if scenario.status == "failed":
        try:
            screenshot = context.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"FAILED - {scenario.name}",
                attachment_type=allure.attachment_type.PNG
            )
            print(f"[INFO] Screenshot captured for failed scenario: {scenario.name}")
        except WebDriverException:
            print("[Warning] Could not capture failure screenshot.")

    # Quit the WebDriver instance
    try:
        if hasattr(context, "driver") and context.driver:
            context.driver.quit()
            print(f"[INFO] Browser closed after scenario: {scenario.name}")
    except WebDriverException as e:
        print(f"[Warning] Error closing browser: {e}")


# -----------------------------------------------------------------------
# Step-level hooks
# -----------------------------------------------------------------------

def before_step(context, step):
    """Called before each step — useful for logging step execution."""
    print(f"  [STEP] {step.keyword} {step.name}")


def after_step(context, step):
    """
    Called after each step.
    Attaches a screenshot to Allure for any failed step.
    """
    if step.status == "failed":
        try:
            screenshot = context.driver.get_screenshot_as_png()
            allure.attach(
                screenshot,
                name=f"Step Failed: {step.name}",
                attachment_type=allure.attachment_type.PNG
            )
        except (WebDriverException, AttributeError):
            pass
