class Transaction:
    """ Represents a transaction to be applied to a bank account """

    def __init__(self, transaction_id, account_number, tx_type, amount):
        self.transaction_id = transaction_id
        self.account_number = account_number
        self.tx_type = tx_type
        self.amount = amount

    def apply(self, account):
        """ Applies the transaction to the given bank account """

        transaction_fee = 0.05 if "student" in account.name.lower() else 0.10

        if self.tx_type == "D": # Deposit
            account.credit(self.amount)
        elif self.tx_type == "W": # Withdrawal
            if not account.debit(self.amount, transaction_fee):
                return False # Transaction failed (negative balance)
        else:
            return False # Invalid transaction type
        return True