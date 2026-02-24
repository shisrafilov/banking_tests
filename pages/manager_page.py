"""Manager page – bank manager panel (add customer, open account, list customers)."""
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class ManagerPage(BasePage):
    """Models the Bank Manager dashboard."""

    # -- Locators ----------------------------------------------------------
    ADD_CUSTOMER_TAB = "button[ng-click='addCust()']"
    CUSTOMERS_TAB    = "button[ng-click='showCust()']"

    # Add customer form
    FIRST_NAME_INPUT = "input[placeholder='First Name']"
    LAST_NAME_INPUT  = "input[placeholder='Last Name']"
    POST_CODE_INPUT  = "input[placeholder='Post Code']"
    ADD_CUSTOMER_BTN = "button[type='submit']"

    # Customer list
    CUSTOMER_TABLE   = "table.table"
    CUSTOMER_ROWS    = "table.table tbody tr"
    SEARCH_INPUT     = "input[placeholder='Search Customer']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -- Actions -----------------------------------------------------------
    def go_to_add_customer(self) -> None:
        self.page.click(self.ADD_CUSTOMER_TAB)
        expect(self.page.locator(self.FIRST_NAME_INPUT)).to_be_visible()

    def add_customer(self, first: str, last: str, post_code: str) -> None:
        self.go_to_add_customer()
        self.page.fill(self.FIRST_NAME_INPUT, first)
        self.page.fill(self.LAST_NAME_INPUT, last)
        self.page.fill(self.POST_CODE_INPUT, post_code)
        self.page.once("dialog", lambda d: d.accept())
        expect(self.page.locator(self.ADD_CUSTOMER_BTN)).to_be_enabled()
        self.page.click(self.ADD_CUSTOMER_BTN)

    def go_to_customers_list(self) -> None:
        self.page.click(self.CUSTOMERS_TAB)
        expect(self.page.locator(self.SEARCH_INPUT)).to_be_visible()

    def search_customer(self, name: str) -> None:
        self.go_to_customers_list()
        self.page.fill(self.SEARCH_INPUT, name)

    # -- Assertions --------------------------------------------------------
    def should_show_manager_panel(self) -> None:
        expect(self.page.locator(self.ADD_CUSTOMER_TAB)).to_be_visible()

    def should_find_customer_in_list(self, name: str) -> None:
        self.search_customer(name)
        expect(self.page.locator(self.CUSTOMER_ROWS).first).to_contain_text(name)

    def should_show_customer_table(self) -> None:
        self.go_to_customers_list()
        expect(self.page.locator(self.CUSTOMER_TABLE)).to_be_visible()

    def should_have_customers(self) -> None:
        self.go_to_customers_list()
        rows = self.page.locator(self.CUSTOMER_ROWS)
        assert rows.count() > 0, "Expected at least one customer row"

    def should_all_rows_contain(self, text: str) -> None:
        rows = self.page.locator(self.CUSTOMER_ROWS)
        count = rows.count()
        assert count >= 1, f"Expected at least one row, got 0"
        assert all(text in rows.nth(i).inner_text() for i in range(count)), \
            f"Not all rows contain '{text}'"
