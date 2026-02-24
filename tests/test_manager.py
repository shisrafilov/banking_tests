"""
tests/test_manager.py

Tests covering Bank Manager panel: add customer, open account, customer list.
"""
import uuid

import pytest

from pages.manager_page import ManagerPage


def unique_name(base: str) -> str:
    """Generate a unique name to avoid leftover-data conflicts between runs."""
    return f"{base}_{uuid.uuid4().hex[:6]}"


class TestManagerPanel:
    """Verify the Bank Manager panel features."""

    def test_manager_panel_is_accessible(self, manager_page: ManagerPage):
        """
        GIVEN  the user clicks 'Bank Manager Login'
        WHEN   the manager panel loads
        THEN   the Add Customer, Open Account, and Customers tabs are visible
        """
        manager_page.should_show_manager_panel()

    def test_add_new_customer(self, manager_page: ManagerPage):
        """
        GIVEN  the manager is on the Add Customer tab
        WHEN   a valid first name, last name, and post code are submitted
        THEN   the customer appears in the Customers list
        """
        first = unique_name("Test")
        last  = "Automation"
        post  = "E1 7AA"

        manager_page.add_customer(first, last, post)
        manager_page.should_find_customer_in_list(first)

    def test_customers_list_is_not_empty(self, manager_page: ManagerPage):
        """
        GIVEN  the manager navigates to the Customers list
        WHEN   the table renders
        THEN   at least one customer row is present (pre-seeded data)
        """
        manager_page.should_have_customers()

    def test_search_filters_customer_list(self, manager_page: ManagerPage):
        """
        GIVEN  the manager is on the Customers tab
        WHEN   he searches for 'Harry'
        THEN   only rows containing 'Harry' are displayed
        """
        manager_page.search_customer("Harry")
        manager_page.should_all_rows_contain("Harry")
