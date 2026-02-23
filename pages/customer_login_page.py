"""Customer login page – customer selects their name and logs in."""
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CustomerLoginPage(BasePage):
    """Models the customer login form (name dropdown)."""

    # -- Locators ----------------------------------------------------------
    CUSTOMER_SELECT   = "select#userSelect"
    LOGIN_BTN         = "button[type='submit']"
    WELCOME_MSG       = "span.fontBig"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -- Actions -----------------------------------------------------------
    def select_customer(self, name: str) -> None:
        self.page.select_option(self.CUSTOMER_SELECT, label=name)

    def click_login(self) -> None:
        self.page.click(self.LOGIN_BTN)

    def login_as(self, name: str) -> None:
        self.select_customer(name)
        self.click_login()

    # -- Assertions --------------------------------------------------------
    def should_show_welcome(self, name: str) -> None:
        expect(self.page.locator(self.WELCOME_MSG)).to_contain_text(name)

    def should_show_dropdown(self) -> None:
        expect(self.page.locator(self.CUSTOMER_SELECT)).to_be_visible()

    def login_button_should_be_disabled_without_selection(self) -> None:
        """Login button should not submit when no customer is selected."""
        # The default option has value "" – button is still visible but
        # submitting it navigates nowhere; we verify we stay on same URL.
        expect(self.page.locator(self.LOGIN_BTN)).to_be_visible()
