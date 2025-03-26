from bank_accont import BankAccount
from transaction import Transaction
from error_logger import ErrorLogger
from read import read_old_bank_accounts
from write import write_new_current_accounts

class BackEndProcessor:
    """
        Processes bank transactions, applies them to accounts, and enforces constratins.
    """

    def __init__(self, master_file, transaction_file, new_master_file, current_accounts_file):
        self.master_file = master_file
        self.transaction_file = transaction_file
        self.new_master_file = new_master_file
        self.current_accounts_file = current_accounts_file

    
    def load_account(self):
        """
            Reads the old master bank account file and loads account into a dictionary.
        """

        account_list = read_old_bank_accounts(self.master_file)
        self.accounts = {acc["account_number"]: BankAccount(**acc) for acc in account_list}

    def read_transactions(self):
        """
            Reads transactionsn from the transaction file
        """

        transactions = []
        with open(self.transaction_file, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue # Ignore malformed lines

                transaction_id, account_number, tx_type, amount = parts[0], parts[1], parts[2], float(parts[3])
                transactions.append(Transaction(transaction_id, account_number, tx_type, amount))
        
        return transactions

    
    def process_transactions(self):
        """
        Applies transactions to accounts while enforcing constraints.
        """
        transactions = self.read_transactions()

        for tx in transactions:
            if tx.account_number not in self.accounts:
                ErrorLogger.log_constraint_error("Account Not Found", f"Account {tx.account_number} does not exist")
                continue

            account = self.accounts[tx.account_number]

            if not tx.apply(account):
                ErrorLogger.log_constraint_error("Transaction Failed", 
                                                 f"Failed to process {tx.tx_type} {tx.amount} for {tx.account_number}")

    def save_accounts(self):
        """
        Writes the new master bank accounts file and current accounts file.
        """
        account_dicts = [acc.to_dict() for acc in self.accounts.values()]
        write_new_current_accounts(account_dicts, self.current_accounts_file)

        with open(self.new_master_file, 'w') as file:
            for acc in account_dicts:
                file.write(f"{acc['account_number'].zfill(5)} {acc['name'].ljust(20)[:20]} {acc['status']} "
                           f"{acc['balance']:08.2f} {str(acc['total_transactions']).zfill(4)}\n")

    def run(self):
        """
        Executes the entire processing sequence.
        """
        self.load_account()
        self.process_transactions()
        self.save_accounts()
        print("Processing complete. New master and current accounts files created.")

# Example usage
if __name__ == "__main__":
    backend = BackEndProcessor("old_master_accounts.txt", "merged_transactions.txt",
                               "new_master_accounts.txt", "current_accounts.txt")
    backend.run()