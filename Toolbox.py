class Toolbox:
    """
    A toolbox class with useful miscellaneous functions
    """

    # //// STARTER CODE: DO NOT ALTER ////
    @staticmethod
    def log_constraint_error(constraint_type, description):
        """
        Prints an error message for failed constraints in the required format
        """
        print(f"ERROR: {constraint_type}: {description}")


    @staticmethod
    def decode_tc(transaction_code):
        """
        Decodes transaction code into corresponding transaction
        Returns related transaction function
        """
        from TransactionHandler import TransactionHandler
        match transaction_code:
            case 1:
                return TransactionHandler.withdraw
            case 2:
                return TransactionHandler.transfer
            case 3:
                return TransactionHandler.paybill
            case 4:
                return TransactionHandler.deposit
            case 5:
                return TransactionHandler.create
            case 6:
                return TransactionHandler.delete
            case 7:
                return TransactionHandler.disable
            case 8:
                return TransactionHandler.changeplan
            case _:
                return lambda x, y: None


    @staticmethod
    def search_account(accounts, transaction):
        """
        Searches for account that matches transaction
        Returns account or None if account does not exist
        """
        for account in accounts:
            if account['account_number'] == transaction['account_number']:
                return account
        return None