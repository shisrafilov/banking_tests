"""Base page class providing shared browser interactions."""
from playwright.sync_api import Page, expect


class BasePage:
    """All page objects inherit from this class."""

    BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#"

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, path: str = "/login") -> None:
        self.page.goto(f"{self.BASE_URL}{path}")

    def get_alert_text(self) -> str:
        """Capture and dismiss browser dialog, returning its message."""
        with self.page.expect_event("dialog") as dialog_info:
            yield
        return dialog_info.value.message
