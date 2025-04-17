import unittest
import tempfile
import os


def write_new_current_accounts(accounts, file_path):
    with open(file_path, 'w') as file:
        for acc in accounts:
            # Validate account number
            if not isinstance(acc['account_number'], str) or not acc['account_number'].isdigit():
                raise ValueError(f"Invalid account number: {acc['account_number']}")
            if len(acc['account_number']) > 5:
                raise ValueError(f"Account number too long: {acc['account_number']}")

            # Validate name length
            if len(acc['name']) > 20:
                raise ValueError(f"Name exceeds 20 characters: {acc['name']}")

            # Validate status
            if acc['status'] not in ('A', 'D'):
                raise ValueError(f"Invalid status: {acc['status']}")

            # Validate balance
            if not isinstance(acc['balance'], (int, float)):
                raise ValueError(f"Invalid balance type: {type(acc['balance'])}")
            if acc['balance'] > 99999.99 or acc['balance'] < 0:
                raise ValueError(f"Balance out of range: {acc['balance']}")

            # Validate plan
            if acc['plan'] not in ("NP", "SP"):
                raise ValueError(f"Invalid plan: {acc['plan']}")

            # Format fields
            acc_num = acc['account_number'].zfill(5)
            name = acc['name'].ljust(20)[:20]
            balance = f"{acc['balance']:08.2f}"

            file.write(f"{acc_num} {name} {acc['status']} {balance} {acc['plan']}\n")

        # Add END_OF_FILE marker
        file.write("00000 END_OF_FILE          A 00000.00 NP\n")


def write_new_master_accounts(accounts, file_path):
    with open(file_path, 'w') as file:
        accounts.sort(key=(lambda x: x['account_number']))
        for acc in accounts:
            # Validate account number
            if not isinstance(acc['account_number'], str) or not acc['account_number'].isdigit():
                raise ValueError(f"Invalid account number: {acc['account_number']}")
            if len(acc['account_number']) > 5:
                raise ValueError(f"Account number too long: {acc['account_number']}")

            # Validate name length
            if len(acc['name']) > 20:
                raise ValueError(f"Name exceeds 20 characters: {acc['name']}")

            # Validate status
            if acc['status'] not in ('A', 'D'):
                raise ValueError(f"Invalid status: {acc['status']}")

            # Validate balance
            if not isinstance(acc['balance'], (int, float)):
                raise ValueError(f"Invalid balance type: {type(acc['balance'])}")
            if acc['balance'] > 99999.99 or acc['balance'] < 0:
                raise ValueError(f"Balance out of range: {acc['balance']}")

            # Validate number of transactions
            if not isinstance(acc['total_transactions'], int):
                raise ValueError(f"Invalid transaction count type: {type(acc['total_transactions'])}")
            if acc['total_transactions'] > 9999 or acc['total_transactions'] < 0:
                raise ValueError(f"Transaction count out of range: {acc['total_transactions']}")

            # Validate plan
            if acc['plan'] not in ("NP", "SP"):
                raise ValueError(f"Invalid plan: {acc['plan']}")

            # Format fields
            acc_num = acc['account_number'].zfill(5)
            name = acc['name'].ljust(20)[:20]
            balance = f"{acc['balance']:08.2f}"
            tot_tr = str(acc['total_transactions']).zfill(4)

            file.write(f"{acc_num} {name} {acc['status']} {balance} {tot_tr} {acc['plan']}\n")


class TestWriteNewCurrentAccounts(unittest.TestCase):
    """Tests for write_new_current_accounts (Statement Coverage)"""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = self.temp_file.name
        self.temp_file.close()  # Close the file so the function can write to it

    def tearDown(self):
        os.remove(self.file_path)

    def test_valid_account(self):
        account = [{
            'account_number': '123',
            'name': 'Alice',
            'status': 'A',
            'balance': 1234.56,
            'plan': 'NP'
        }]
        # Expect no exception and file to be written.
        write_new_current_accounts(account, self.file_path)
        with open(self.file_path, 'r') as f:
            content = f.read()
            self.assertIn("00123", content)  # Check that account number is formatted

    def test_invalid_account_number(self):
        account = [{
            'account_number': '12A3',
            'name': 'Alice',
            'status': 'A',
            'balance': 0.0,
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_account_number_too_long(self):
        account = [{
            'account_number': '123456',
            'name': 'Alice',
            'status': 'A',
            'balance': 0.0,
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_name_too_long(self):
        account = [{
            'account_number': '12345',
            'name': 'A' * 21,
            'status': 'A',
            'balance': 0.0,
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_invalid_status(self):
        account = [{
            'account_number': '12345',
            'name': 'Alice',
            'status': 'X',
            'balance': 0.0,
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_invalid_balance_type(self):
        account = [{
            'account_number': '12345',
            'name': 'Alice',
            'status': 'A',
            'balance': 'abc',
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_balance_out_of_range(self):
        account = [{
            'account_number': '12345',
            'name': 'Alice',
            'status': 'A',
            'balance': 100000.00,
            'plan': 'NP'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)

    def test_invalid_plan(self):
        account = [{
            'account_number': '12345',
            'name': 'Alice',
            'status': 'A',
            'balance': 100.00,
            'plan': 'XX'
        }]
        with self.assertRaises(ValueError):
            write_new_current_accounts(account, self.file_path)


class TestWriteNewMasterAccounts(unittest.TestCase):
    """Tests for write_new_master_accounts (Decision and Loop Coverage)"""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.file_path = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.file_path)

    def test_empty_accounts(self):
        # Loop executes 0 times.
        write_new_master_accounts([], self.file_path)
        with open(self.file_path, 'r') as f:
            content = f.read()
            # For an empty list, nothing is written.
            self.assertEqual(content, "")

    def test_one_valid_account(self):
        account = [{
            'account_number': '1',
            'name': 'Bob',
            'status': 'D',
            'balance': 500.0,
            'total_transactions': 5,
            'plan': 'SP'
        }]
        write_new_master_accounts(account, self.file_path)
        with open(self.file_path, 'r') as f:
            content = f.read()
            self.assertIn("00001", content)
            self.assertIn("Bob", content)

    def test_multiple_sorted_accounts(self):
        accounts = [
            {'account_number': '9', 'name': 'Zoe', 'status': 'A', 'balance': 100.0, 'total_transactions': 1, 'plan': 'NP'},
            {'account_number': '2', 'name': 'Alex', 'status': 'A', 'balance': 50.0, 'total_transactions': 2, 'plan': 'NP'}
        ]
        write_new_master_accounts(accounts, self.file_path)
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            # The first line should have the lower account number ("00002") after sorting.
            self.assertTrue(lines[0].startswith("00002"))

    def test_invalid_transaction_type(self):
        account = [{
            'account_number': '1',
            'name': 'Bob',
            'status': 'D',
            'balance': 500.0,
            'total_transactions': 'abc',  # Wrong type
            'plan': 'SP'
        }]
        with self.assertRaises(ValueError):
            write_new_master_accounts(account, self.file_path)

    def test_transaction_count_out_of_range(self):
        account = [{
            'account_number': '1',
            'name': 'Bob',
            'status': 'D',
            'balance': 500.0,
            'total_transactions': 10000,  # Out of allowed range
            'plan': 'SP'
        }]
        with self.assertRaises(ValueError):
            write_new_master_accounts(account, self.file_path)


if __name__ == '__main__':
    unittest.main()
