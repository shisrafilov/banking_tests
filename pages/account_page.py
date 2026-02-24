"""Account page – shown after a customer logs in successfully."""
import re

from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AccountPage(BasePage):
    """Models the customer account dashboard (transactions, deposit, withdraw)."""

    # -- Locators ----------------------------------------------------------
    DEPOSIT_TAB       = "button[ng-click='deposit()']"
    WITHDRAW_TAB      = "button[ng-click='withdrawl()']"
    TRANSACTIONS_TAB  = "button[ng-click='transactions()']"
    AMOUNT_INPUT      = "input[placeholder='amount']"
    DEPOSIT_SUBMIT_BTN  = "form[ng-submit='deposit()'] button"
    WITHDRAW_SUBMIT_BTN = "form[ng-submit='withdrawl()'] button"
    WELCOME_MSG       = "span.fontBig"
    SUCCESS_MSG       = "span.error"
    BALANCE           = "div.center > strong:nth-of-type(2)"
    TRANSACTION_TABLE = "table.table"
    LOGOUT_BTN        = "button[ng-click='byebye()']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -- Actions -----------------------------------------------------------
    def deposit(self, amount: int) -> None:
        self.page.click(self.DEPOSIT_TAB)
        expect(self.page.locator(self.DEPOSIT_TAB)).to_have_class(re.compile(r"btn-primary"))
        self.page.locator(self.AMOUNT_INPUT).clear()
        self.page.locator(self.AMOUNT_INPUT).type(str(amount))
        self.page.click(self.DEPOSIT_SUBMIT_BTN)

    def withdraw(self, amount: int) -> None:
        self.page.click(self.WITHDRAW_TAB)
        expect(self.page.locator(self.WITHDRAW_TAB)).to_have_class(re.compile(r"btn-primary"))
        expect(self.page.locator(self.SUCCESS_MSG)).to_be_hidden()
        self.page.locator(self.AMOUNT_INPUT).clear()
        self.page.locator(self.AMOUNT_INPUT).type(str(amount))
        self.page.click(self.WITHDRAW_SUBMIT_BTN)

    def view_transactions(self) -> None:
        self.page.click(self.TRANSACTIONS_TAB)

    def logout(self) -> None:
        self.page.click(self.LOGOUT_BTN)

    # -- Assertions --------------------------------------------------------
    def should_be_logged_in(self) -> None:
        expect(self.page.locator(self.DEPOSIT_TAB)).to_be_visible()

    def should_show_welcome(self, name: str) -> None:
        expect(self.page.locator(self.WELCOME_MSG)).to_contain_text(name)

    def should_show_welcome_for(self, full_name: str) -> None:
        """Assert welcome banner using full name – extracts first name internally."""
        self.should_show_welcome(full_name.split()[0])

    def should_show_success_message(self, text: str) -> None:
        expect(self.page.locator(self.SUCCESS_MSG)).to_contain_text(text)

    def should_have_balance(self, expected: int) -> None:
        expect(self.page.locator(self.BALANCE)).to_have_text(str(expected))

    def should_show_transaction_table(self) -> None:
        expect(self.page.locator(self.TRANSACTION_TABLE)).to_be_visible()

    def balance(self) -> int:
        expect(self.page.locator(self.BALANCE)).to_be_visible()
        return int(self.page.locator(self.BALANCE).inner_text().strip())
