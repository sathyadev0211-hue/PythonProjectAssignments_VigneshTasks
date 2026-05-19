"""
Task 11 - Selenium Automation for https://www.saucedemo.com/
Fetches:
  1. Title of the webpage
  2. Current URL of the webpage
  3. Entire contents of the webpage saved to Webpage_task_11.txt
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --------------------------------------------------------------------------- #
#  Constants
# --------------------------------------------------------------------------- #
BASE_URL   = "https://www.saucedemo.com/"
USERNAME   = "standard_user"
PASSWORD   = "secret_sauce"
OUTPUT_TXT = "Webpage_task_11.txt"


def get_driver() -> webdriver.Chrome:
    """Return a configured headless Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


def login(driver: webdriver.Chrome) -> None:
    """Navigate to saucedemo and log in with the provided credentials."""
    driver.get(BASE_URL)

    # Wait until the username field is present
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "user-name")))

    # Enter credentials and submit
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()

    # Wait until the inventory page loads
    wait.until(EC.url_contains("inventory"))


def fetch_title(driver: webdriver.Chrome) -> str:
    """Return the current page title."""
    return driver.title


def fetch_current_url(driver: webdriver.Chrome) -> str:
    """Return the current URL of the page."""
    return driver.current_url


def save_page_content(driver: webdriver.Chrome, filepath: str = OUTPUT_TXT) -> str:
    """
    Extract the full text content of the page and save it to a .txt file.
    Returns the filepath that was written.
    """
    page_text = driver.find_element(By.TAG_NAME, "body").text
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(page_text)
    return filepath


# --------------------------------------------------------------------------- #
#  Main entry point
# --------------------------------------------------------------------------- #
def main() -> None:
    driver = get_driver()
    try:
        login(driver)

        title       = fetch_title(driver)
        current_url = fetch_current_url(driver)
        saved_path  = save_page_content(driver)

        print(f"1. Page Title   : {title}")
        print(f"2. Current URL  : {current_url}")
        print(f"3. Content saved: {saved_path}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
