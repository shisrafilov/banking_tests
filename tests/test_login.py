"""
tests/test_login.py

Tests covering the login / role-selection flow.
"""
import pytest

from pages.login_page import LoginPage
from pages.manager_page import ManagerPage
from pages.customer_login_page import CustomerLoginPage
from pages.account_page import AccountPage


class TestLoginPage:
    """Verify the initial role-selection screen."""

    def test_login_page_shows_both_role_buttons(self, login_page: LoginPage):
        """
        GIVEN  the user opens the application root URL
        WHEN   the page loads
        THEN   both 'Customer Login' and 'Bank Manager Login' buttons are visible
        """
        login_page.should_show_role_selection()

    def test_navigate_to_customer_login(self, login_page: LoginPage):
        """
        GIVEN  the role-selection screen is displayed
        WHEN   the user clicks 'Customer Login'
        THEN   the customer dropdown form is shown
        """
        login_page.go_to_customer_login()
        CustomerLoginPage(login_page.page).should_show_dropdown()

    def test_navigate_to_manager_login(self, login_page: LoginPage):
        """
        GIVEN  the role-selection screen is displayed
        WHEN   the user clicks 'Bank Manager Login'
        THEN   the manager panel is displayed
        """
        login_page.go_to_manager_login()
        ManagerPage(login_page.page).should_show_manager_panel()


class TestCustomerLogin:
    """Verify customer authentication flow."""

    @pytest.mark.parametrize("customer_name", [
        "Harry Potter",
        "Hermoine Granger",
        "Neville Longbottom",
    ])
    def test_customer_can_login(self, customer_login_page: CustomerLoginPage, customer_name: str):
        """
        GIVEN  the customer login form
        WHEN   a valid customer name is selected and Login is clicked
        THEN   the account dashboard is shown with the customer's first name
        """
        customer_login_page.login_as(customer_name)
        ap = AccountPage(customer_login_page.page)
        ap.should_be_logged_in()
        ap.should_show_welcome_for(customer_name)

    def test_customer_can_logout(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter is logged in
        WHEN   he clicks the logout button
        THEN   the app returns to the Customer Login screen
        """
        account_page_harry.logout()
        CustomerLoginPage(account_page_harry.page).should_show_dropdown()