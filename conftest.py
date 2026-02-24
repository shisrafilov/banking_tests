"""
conftest.py – shared pytest fixtures for the Banking Project test suite.

Fixtures follow the Page Object Model: each fixture provides a ready-to-use
page object, navigated to the correct URL, so individual tests stay concise.
"""
import pytest
from playwright.sync_api import Page, Browser, expect

from pages.login_page import LoginPage
from pages.customer_login_page import CustomerLoginPage
from pages.account_page import AccountPage
from pages.manager_page import ManagerPage


# ---------------------------------------------------------------------------
# Browser / context configuration
# ---------------------------------------------------------------------------

@pytest.fixture
def page(browser: Browser) -> Page:
    """
    Override the default pytest-playwright page fixture.
    Creates a fresh context + page for every test with:
      - consistent viewport
      - 30s timeout to handle slow Angular rendering
    """
    context = browser.new_context(viewport={"width": 1280, "height": 1024})
    pg = context.new_page()
    pg.set_default_timeout(10_000)
    expect.set_options(timeout=10_000)
    yield pg
    context.close()


# ---------------------------------------------------------------------------
# Page-object fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Open the app login (role selection) page."""
    lp = LoginPage(page)
    lp.load()
    return lp


@pytest.fixture
def customer_login_page(login_page: LoginPage) -> CustomerLoginPage:
    """Navigate from login to the Customer Login form."""
    login_page.go_to_customer_login()
    return CustomerLoginPage(login_page.page)


@pytest.fixture
def manager_page(login_page: LoginPage) -> ManagerPage:
    """Navigate from login to the Manager panel."""
    login_page.go_to_manager_login()
    return ManagerPage(login_page.page)


@pytest.fixture
def account_page_harry(customer_login_page: CustomerLoginPage) -> AccountPage:
    """Log in as Harry Potter and return the AccountPage."""
    customer_login_page.login_as("Harry Potter")
    return AccountPage(customer_login_page.page)
