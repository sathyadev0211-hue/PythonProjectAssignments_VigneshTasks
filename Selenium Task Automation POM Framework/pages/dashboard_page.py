"""
pages/dashboard_page.py
-----------------------
Page Object Model for the Zen Portal Dashboard (https://v2.zenclass.in).
Handles post-login page actions including logout.
"""

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object for the Zen Portal dashboard shown after a successful login.
    Inherits common wait utilities from BasePage.
    """

    # ──────────────────────────────────────────────
    # Locators  (v2.zenclass.in post-login layout)
    # ──────────────────────────────────────────────

    # Dashboard body — confirms the page loaded after login
    DASHBOARD_CONTENT = (By.XPATH,
        "//*[contains(@class,'dashboard') or contains(@class,'home') "
        "or contains(@class,'sidebar') or contains(@class,'main-content') "
        "or contains(@class,'nav') or contains(@class,'layout')]"
    )

    # Profile / avatar toggle to open dropdown
    PROFILE_MENU = (By.XPATH,
        "//img[contains(@class,'profile') or contains(@class,'avatar') "
        "or contains(@alt,'profile') or contains(@alt,'avatar')] | "
        "//*[contains(@class,'user-menu') or contains(@class,'profile-menu') "
        "or contains(@class,'dropdown-toggle') or contains(@class,'user-profile')]"
    )

    # Logout link/button — covers text and href patterns
    LOGOUT_BUTTON = (By.XPATH,
        "//*[normalize-space(text())='Logout' or normalize-space(text())='Log Out' "
        "or normalize-space(text())='Sign Out' "
        "or contains(@href,'logout') or contains(@href,'sign-out') "
        "or contains(@onclick,'logout')]"
    )

    def __init__(self, driver):
        """Initialize DashboardPage."""
        super().__init__(driver)

    # ──────────────────────────────────────────────
    # Actions
    # ──────────────────────────────────────────────
    def click_profile_menu(self):
        """Click the profile/user icon to open the dropdown menu."""
        self.click_element(self.PROFILE_MENU)

    def click_logout(self):
        """Click the Logout link."""
        self.click_element(self.LOGOUT_BUTTON)

    def logout(self):
        """
        Full logout flow:
        1. Click the profile menu to reveal dropdown.
        2. Click logout.
        """
        try:
            self.click_profile_menu()
        except Exception:
            # Some views expose logout directly (no dropdown needed)
            pass
        self.click_logout()

    # ──────────────────────────────────────────────
    # Validations
    # ──────────────────────────────────────────────
    def is_dashboard_loaded(self) -> bool:
        """Return True if dashboard content is visible."""
        return self.is_element_visible(self.DASHBOARD_CONTENT)

    def is_logged_in(self) -> bool:
        """
        Return True if user appears logged in
        (URL no longer points to the login page).
        """
        current_url = self.get_current_url()
        return "login" not in current_url and "sign-in" not in current_url

    def is_logout_button_visible(self) -> bool:
        """Return True if the logout button/link is currently visible."""
        return self.is_element_visible(self.LOGOUT_BUTTON)

    def wait_for_logout_redirect(self) -> bool:
        """Wait for URL to return to the login page after logout."""
        return self.wait_for_url_contains("login") or self.wait_for_url_contains("sign-in")
