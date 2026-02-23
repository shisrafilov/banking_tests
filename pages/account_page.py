"""Account page – shown after a customer logs in successfully."""
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AccountPage(BasePage):
    """Models the customer account dashboard (transactions, deposit, withdraw)."""

    # -- Locators ----------------------------------------------------------
    ACCOUNT_NO        = "div.center > strong:nth-of-type(1)"
    BALANCE           = "div.center > strong:nth-of-type(2)"
    CURRENCY          = "div.center > strong:nth-of-type(3)"
    DEPOSIT_TAB       = "button[ng-click='deposit()']"
    WITHDRAW_TAB      = "button[ng-click='withdrawl()']"
    TRANSACTIONS_TAB  = "button[ng-click='transactions()']"
    AMOUNT_INPUT      = "input[placeholder='amount']"
    SUBMIT_BTN        = "button[type='submit']"
    WELCOME_MSG       = "span.fontBig"
    SUCCESS_MSG       = "span.error"          # Angular reuses .error class for success too
    TRANSACTION_TABLE = "table.table"
    LOGOUT_BTN        = "button[ng-click='byebye()']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -- Helpers -----------------------------------------------------------
    def _current_balance(self) -> int:
        text = self.page.locator(self.BALANCE).inner_text().strip()
        return int(text)

    # -- Actions -----------------------------------------------------------
    def deposit(self, amount: int) -> None:
        self.page.click(self.DEPOSIT_TAB)
        self.page.fill(self.AMOUNT_INPUT, str(amount))
        self.page.click(self.SUBMIT_BTN)

    def withdraw(self, amount: int) -> None:
        self.page.click(self.WITHDRAW_TAB)
        self.page.fill(self.AMOUNT_INPUT, str(amount))
        self.page.click(self.SUBMIT_BTN)

    def view_transactions(self) -> None:
        self.page.click(self.TRANSACTIONS_TAB)

    def logout(self) -> None:
        self.page.click(self.LOGOUT_BTN)

    # -- Assertions --------------------------------------------------------
    def should_be_logged_in(self) -> None:
        expect(self.page.locator(self.DEPOSIT_TAB)).to_be_visible()

    def should_show_welcome(self, name: str) -> None:
        expect(self.page.locator(self.WELCOME_MSG)).to_contain_text(name)

    def should_show_success_message(self, text: str) -> None:
        expect(self.page.locator(self.SUCCESS_MSG)).to_contain_text(text)


    def should_have_balance(self, expected: int) -> None:
        expect(self.page.locator(self.BALANCE)).to_have_text(str(expected))

    def should_show_transaction_table(self) -> None:
        expect(self.page.locator(self.TRANSACTION_TABLE)).to_be_visible()

    def balance(self) -> int:
        return self._current_balance()
