"""
Dashboard Page Object Model for the Guvi Zen Portal.
Represents the page a user lands on after a successful login.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """
    Page Object for the Zen Portal Dashboard (post-login home page).
    Provides locators and actions for verifying login and performing logout.
    """

    # ── Locators ──────────────────────────────────────────────────────────────
    # Profile / avatar area (top-right corner in most portals)
    PROFILE_ICON     = "img[alt*='profile'], .profile-icon, [class*='avatar'], #user-avatar"
    # Logout link/button – adjust selector to match your portal's actual DOM
    LOGOUT_BUTTON    = "a[href*='logout'], button[class*='logout'], [data-testid='logout']"
    # A reliable indicator that the dashboard has loaded
    DASHBOARD_MARKER = ".dashboard, #dashboard, [class*='home-page'], main"

    def __init__(self, page: Page):
        super().__init__(page)

    # ── Validation helpers ────────────────────────────────────────────────────

    def is_dashboard_loaded(self) -> bool:
        """
        Return True when at least one known dashboard element is visible,
        confirming a successful login redirect.
        """
        # Try several common post-login URL patterns as a fallback
        current_url = self.get_current_url()
        url_ok = any(
            kw in current_url
            for kw in ("dashboard", "home", "profile", "course", "zen")
        )
        dom_ok = self.is_element_visible(self.DASHBOARD_MARKER)
        return url_ok or dom_ok

    def is_logout_button_visible(self) -> bool:
        """Return True if the logout button/link is present and visible."""
        return self.is_element_visible(self.LOGOUT_BUTTON)

    # ── Actions ───────────────────────────────────────────────────────────────

    def open_profile_menu(self) -> None:
        """Click the profile icon to reveal the dropdown menu (if applicable)."""
        if self.is_element_visible(self.PROFILE_ICON):
            self.page.locator(self.PROFILE_ICON).first.click()
            self.page.wait_for_timeout(1000)   # brief wait for animation

    def click_logout(self) -> None:
        """
        Perform logout.
        Tries to open a profile dropdown first; then clicks the logout control.
        """
        self.open_profile_menu()
        logout = self.wait_for_element(self.LOGOUT_BUTTON, timeout=7000)
        logout.click()
        # Wait until we are redirected away from the dashboard
        self.page.wait_for_load_state("networkidle")

    def logout(self) -> None:
        """High-level helper to fully log out and land back on the login page."""
        self.click_logout()
