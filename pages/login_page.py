"""Login page – entry point of the Banking Project application."""
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Models the /login route (role selection screen)."""

    # -- Locators ----------------------------------------------------------
    CUSTOMER_LOGIN_BTN = "button[ng-click='customer()']"
    MANAGER_LOGIN_BTN  = "button[ng-click='manager()']"
    PAGE_HEADER        = "div.home > div"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -- Actions -----------------------------------------------------------
    def load(self) -> "LoginPage":
        self.navigate_to("/login")
        return self

    def go_to_customer_login(self) -> None:
        self.page.click(self.CUSTOMER_LOGIN_BTN)

    def go_to_manager_login(self) -> None:
        self.page.click(self.MANAGER_LOGIN_BTN)

    # -- Assertions --------------------------------------------------------
    def should_show_role_selection(self) -> None:
        expect(self.page.locator(self.CUSTOMER_LOGIN_BTN)).to_be_visible()
        expect(self.page.locator(self.MANAGER_LOGIN_BTN)).to_be_visible()
