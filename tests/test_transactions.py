"""
Tests covering deposit, withdrawal, and transaction history for a customer.
"""

from pages.account_page import AccountPage


class TestDeposit:
    """Verify the deposit feature."""

    def test_deposit_increases_balance(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter is logged in with a known balance
        WHEN   he deposits 500
        THEN   the balance increases by exactly 500
               AND a success message is displayed
        """
        initial_balance = account_page_harry.balance()
        deposit_amount = 500

        account_page_harry.deposit(deposit_amount)

        account_page_harry.should_show_success_message("Deposit Successful")
        account_page_harry.should_have_balance(initial_balance + deposit_amount)

    def test_deposit_zero_does_not_change_balance(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter is logged in
        WHEN   he tries to deposit 0
        THEN   the balance remains unchanged
        """
        initial_balance = account_page_harry.balance()
        account_page_harry.deposit(0)
        account_page_harry.should_have_balance(initial_balance)


class TestWithdrawal:
    """Verify the withdrawal feature."""

    def test_withdraw_decreases_balance(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter has sufficient funds (seeded via deposit)
        WHEN   he withdraws 200
        THEN   balance decreases by 200
        """
        initial_balance = account_page_harry.balance()

        account_page_harry.deposit(1000)
        account_page_harry.should_have_balance(initial_balance + 1000)  # ждём обновления баланса

        account_page_harry.withdraw(200)
        account_page_harry.should_have_balance(initial_balance + 800)

    def test_overdraft_does_not_change_balance(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter has a known balance
        WHEN   he tries to withdraw more than his balance
        THEN   an error message is displayed
               AND the balance does not change
        """
        initial_balance = account_page_harry.balance()
        overdraft_amount = initial_balance + 99_999

        account_page_harry.withdraw(overdraft_amount)

        account_page_harry.should_show_success_message("Transaction Failed")
        account_page_harry.should_have_balance(initial_balance)


class TestTransactionHistory:
    """Verify the transaction history table."""

    def test_transactions_tab_shows_history(self, account_page_harry: AccountPage):
        """
        GIVEN  Harry Potter has performed at least one transaction
        WHEN   he opens the Transactions tab
        THEN   the transaction table is visible
        """
        account_page_harry.deposit(100)
        account_page_harry.view_transactions()
        account_page_harry.should_show_transaction_table()
