from Toolbox import Toolbox

class TransactionHandler:
    """
    Handles the application of transactions to account data
    """
    # TODO: Ensure all transactions implement Toolbox.log_constraint_error()

    @staticmethod
    def withdraw(account, transaction):
        if account['status'] == 'D':
            Toolbox.log_constraint_error("Account Disabled", f"Cannot withdraw from disabled account {account['account_number']}")
            return

        if transaction['amount'] > account['balance']:
            Toolbox.log_constraint_error("Insufficient Funds", f"Cannot withdraw {transaction['amount']} from account {account['account_number']}")
            return

        account['balance'] -= transaction['amount']
        account['total_transactions'] += 1

    @staticmethod
    def transfer(account, transaction):
        if not account:
            Toolbox.log_constraint_error("Account Not Found", f"Account {transaction['account_number']} does not exist")
            return

        if transaction['misc'] not in ("SD", "RV"):
            Toolbox.log_constraint_error("Invalid Code", f"{transaction['misc']} is not a valid transfer code")
            return

        if account['status'] == 'D':
            Toolbox.log_constraint_error("Account Disabled", "Cannot transfer involving disabled account")
            return

        sending = (transaction['misc'] == "SD")

        if sending:
            if transaction['amount'] > account['balance']:
                Toolbox.log_constraint_error("Insufficient Funds", f"Cannot transfer {transaction['amount']} from account {account['account_number']}")
                return

            account['balance'] -= transaction['amount']
            account['total_transactions'] += 1
        else:
            if (account['balance'] + transaction['amount']) > 99999.99:
                Toolbox.log_constraint_error("Balance Limit Exceeded",f"Cannot deposit {transaction['amount']} into account {account['account_number']}")
                return

            account['balance'] += transaction['amount']
            account['total_transactions'] += 1

    @staticmethod
    def paybill(account, transaction):
        if account['status'] == 'D':
            Toolbox.log_constraint_error("Account Disabled", f"Cannot pay bills from disabled account {account['account_number']}")
            return

        if transaction['amount'] > account['balance']:
            Toolbox.log_constraint_error("Insufficient Funds", f"Cannot pay bill of {transaction['amount']} from account {account['account_number']}")
            return

        account['balance'] -= transaction['amount']
        account['total_transactions'] += 1

    @staticmethod
    def deposit(account, transaction):
        if account['status'] == 'D':
            Toolbox.log_constraint_error("Account Disabled", f"Cannot deposit into disabled account {account['account_number']}")
            return

        if (account['balance'] + transaction['amount']) > 99999.99:
            Toolbox.log_constraint_error("Balance Limit Exceeded", f"Cannot deposit {transaction['amount']} into account {account['account_number']}")
            return

        account['balance'] += transaction['amount']
        account['total_transactions'] += 1

    @staticmethod
    def create(account, transaction):
        if account:
            Toolbox.log_constraint_error("Account Exists", f"Cannot create duplicate account {transaction['account_number']}")
            return

        if transaction['misc'] not in ("NP", "SP"):
            Toolbox.log_constraint_error("Invalid Code", f"{transaction['misc']} is not a valid plan")
            return

        new_account = {
            'account_number': transaction['account_number'],
            'name': transaction['name'],
            'status': 'A',  # Active by default
            'balance': transaction['amount'],
            'total_transactions': 0,
            'plan': transaction['misc']  # Regular or Student plan
    }

        accounts.append(new_account)

    @staticmethod
    def delete(account, transaction):
        if not account:
            Toolbox.log_constraint_error("Account Not Found", f"Cannot delete non-existent account {transaction['account_number']}")
            return

        if account['balance'] != 0:
            Toolbox.log_constraint_error("Non-Zero Balance", f"Cannot delete account {account['account_number']} with non-zero balance")
            return

        accounts.remove(account)

    @staticmethod
    def disable(account, transaction):
        if transaction['misc'].strip() not in ('A', 'D'):
            Toolbox.log_constraint_error("Invalid Code", f"{transaction['misc']} is not a valid status")
            return

        if account['status'] == transaction['misc'].strip():
            Toolbox.log_constraint_error("Account Already Disabled", f"Account {account['account_number']} is already disabled")
            return

        account['status'] = transaction['misc'].strip()

    @staticmethod
    def changeplan(account, transaction):
        if transaction['misc'] not in ("NP", "SP"):
            Toolbox.log_constraint_error("Invalid Code", f"{transaction['misc']} is not a valid plan")
            return

        if account['status'] == 'D':
            Toolbox.log_constraint_error("Account Disabled", f"Cannot change plan for disabled account {account['account_number']}")
            return

        if account['plan'] == transaction['misc']:
            Toolbox.log_constraint_error("Plan Unchanged", f"Account {account['account_number']} is already on plan {transaction['misc']}")
            return

        account['plan'] = transaction['misc']

    @staticmethod
    def apply(accounts, transactions):
        """
        Applies list of transactions to given account list
        """
        for transaction in transactions:
            account = Toolbox.search_account(accounts, transaction)
            transaction_function = Toolbox.decode_tc(transaction['transaction_code'])

            if not transaction_function:
                Toolbox.log_constraint_error("Invalid Transaction Code", f"Transaction code {transaction['transaction_code']} is not recognized")
                continue

            transaction_function(account, transaction)
