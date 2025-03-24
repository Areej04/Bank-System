from FileIO import FileIO
from TransactionHandler import TransactionHandler

# TODO: Constants may be passed through command line in future for testing purposes
OLD_MASTER_PATH = "test_files/old_master.txt"
NEW_MASTER_PATH = "test_files/new_master.txt"
LOG_FILE_PATH   = "test_files/log.txt"
CURR_ACC_PATH   = "test_files/accounts.txt"

class BackEndSystem:
    """
    Handles the main functionality of the back end system
    """

    @staticmethod
    def commit_transactions(old_acc_path, new_acc_path, log_path, curr_acc_path):
        """
        Applies daily transactions to master account file and produces new account files
        """
        # Read files
        accounts = FileIO.read_old_bank_accounts(old_acc_path)
        transactions = FileIO.read_transactions(log_path)

        # Apply transactions to accounts
        TransactionHandler.apply(accounts, transactions)

        # Write files
        FileIO.write_new_master_accounts(accounts, new_acc_path)
        FileIO.write_new_current_accounts(accounts, curr_acc_path)

BackEndSystem.commit_transactions(OLD_MASTER_PATH, NEW_MASTER_PATH, LOG_FILE_PATH, CURR_ACC_PATH)