import pytest
from unittest.mock import patch
from TransactionHandler import TransactionHandler

# Template account and transactions for future tests
@pytest.fixture
def account_template():
    return {
        'account_number': '00001',
        'name': 'John Doe',
        'status': 'A',
        'balance': 100.00,
        'total_transactions': 1,
        'plan': 'NP'
    }

@pytest.fixture
def _transaction_template():
    return {
        'transaction_code': None,
        'name': 'John Doe',
        'account_number': '00001',
        'amount': 10.00,
        'misc': ''
    }

@pytest.fixture
def transaction_template(_transaction_template, tc):
    temp = _transaction_template.copy()
    temp['transaction_code'] = tc
    return temp



class TestWithdraw:
    """
    Handles all tests related to TransactionHandler.withdraw()
    """
    # Fixture sets transaction code for all tests
    @pytest.fixture(scope="class")
    def tc(self): return 1


    def test_withdraw_success(self, account_template, transaction_template):
        """
        Able to withdraw from account successfully
        """
        # Provide harness for implemented functions
        with patch('TransactionHandler.Toolbox.search_account') as mock_search:
            mock_search.return_value = account_template

            # Run function
            TransactionHandler.withdraw([], transaction_template)

            # Check if test was passed
            assert account_template['balance'] == 90.00
            assert account_template['total_transactions'] == 2

    def test_withdraw_account_missing(self, account_template, transaction_template):
        """
        Account from transaction not in accounts list
        """
        # Provide harness for implemented functions
        with patch('TransactionHandler.Toolbox.search_account') as mock_search:
            with patch('TransactionHandler.Toolbox.log_constraint_error') as mock_error:
                mock_search.return_value = None

                # Run function
                TransactionHandler.withdraw([], transaction_template)

                # Check if test was passed
                mock_error.assert_called_once_with(
                    "Account Not Found",
                    "Account 00001 does not exist"
                )
                assert account_template['balance'] == 100.00
                assert account_template['total_transactions'] == 1

    def test_withdraw_account_disabled(self, account_template, transaction_template):
        """
        Account is disabled and cannot withdraw
        """

        # Provide harness for implemented functions
        with patch('TransactionHandler.Toolbox.search_account') as mock_search:
            with patch('TransactionHandler.Toolbox.log_constraint_error') as mock_error:
                account_template['status'] = 'D'
                mock_search.return_value = account_template

                # Run function
                TransactionHandler.withdraw([], transaction_template)

                # Check if test was passed
                mock_error.assert_called_once_with(
                    "Account Disabled",
                    "Cannot withdraw from disabled account 00001"
                )
                assert account_template['balance'] == 100.00
                assert account_template['total_transactions'] == 1

    def test_withdraw_amount_invalid(self, account_template, transaction_template):
        """
        Attempted to withdraw more than balance
        """

        # Provide harness for implemented functions
        with patch('TransactionHandler.Toolbox.search_account') as mock_search:
            with patch('TransactionHandler.Toolbox.log_constraint_error') as mock_error:
                account_template['balance'] = 5.00
                mock_search.return_value = account_template

                # Run function
                TransactionHandler.withdraw([], transaction_template)

                # Check if test was passed
                mock_error.assert_called_once_with(
                    "Insufficient Funds",
                    "Cannot withdraw 10.00 from account 00001"
                )
                assert account_template['balance'] == 5.00
                assert account_template['total_transactions'] == 1