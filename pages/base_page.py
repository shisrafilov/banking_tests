"""Base page class providing shared browser interactions."""
from playwright.sync_api import Page


class BasePage:
    """All page objects inherit from this class."""

    BASE_URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#"

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate_to(self, path: str = "/login") -> None:
        self.page.goto(f"{self.BASE_URL}{path}")
