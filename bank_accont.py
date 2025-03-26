class BankAccount:

    """
        Represents a bank account with an account number, name, status, balance, and transaction count.
    """

    def __init__(self, account_number, name, status, balance, total_transactions):
        self.account_number = account_number
        self.name = name
        self.status = status
        self.balance = balance
        self.total_transactions = total_transactions
    

    def debit(self, amount, fee):
        """ Debit an amount from the account, with constraints """
        total_deduction = amount + fee
        if self.balance - total_deduction < 0:
                return False # Insufficient funds
        self.balance -= total_deduction
        self.total_transactions += 1

        return True
    

    def credit(self, amount):
        """Credits an amount to the account."""
        self.balance += amount
        self.total_transactions += 1

    def to_dict(self):
        """Returns account details as a dictionary."""
        return {
            "account_number": self.account_number,
            "name": self.name,
            "status": self.status,
            "balance": self.balance,
            "total_transactions": self.total_transactions
        }