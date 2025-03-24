class FileIO:
    """
    A static class which manages all file input and output functions
    """

    # //// STARTER CODE: DO NOT ALTER ////
    @staticmethod
    def read_old_bank_accounts(file_path):
        """
        Reads and validates the bank account file format
        Returns list of accounts and prints fatal errors for invalid format
        """
        accounts = []
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Remove newline but preserve other characters
                clean_line = line.rstrip('\n')

                # Validate line length
                if len(clean_line) != 42:
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars)")
                    continue

                try:
                    # Extract fields with positional validation
                    account_number = clean_line[0:5]
                    name = clean_line[6:26]  # 20 characters
                    status = clean_line[27]
                    balance_str = clean_line[29:37]  # 8 characters
                    transactions_str = clean_line[38:42]  # 4 characters

                    # Validate account number format (5 digits)
                    if not account_number.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid account number format")
                        continue

                    # Validate status
                    if status not in ('A', 'D'):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid status '{status}'")
                        continue

                    # Validate balance format (XXXXX.XX)
                    if (len(balance_str) != 8 or
                            balance_str[5] != '.' or
                            not balance_str[:5].isdigit() or
                            not balance_str[6:].isdigit()):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid balance format")
                        continue

                    # Validate transaction count format
                    if not transactions_str.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction count format")
                        continue

                    # Convert numerical values
                    balance = float(balance_str)
                    transactions = int(transactions_str)

                    # Validate business constraints
                    if balance < 0:
                        print(f"ERROR: Fatal error - Line {line_num}: Negative balance")
                        continue
                    if transactions < 0:
                        print(f"ERROR: Fatal error - Line {line_num}: Negative transaction count")
                        continue

                    accounts.append({
                        'account_number': account_number.lstrip('0') or '0',
                        'name': name.strip(),
                        'status': status,
                        'balance': balance,
                        'total_transactions': transactions
                    })

                except Exception as e:
                    print(f"ERROR: Fatal error - Line {line_num}: Unexpected error: {str(e)}")
                    continue

        return accounts



    @staticmethod
    def read_transactions(file_path):
        """
        Reads and validates the merged transaction file format
        Returns list of sequential transactions and prints fatal errors for invalid format
        """
        transactions = []
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                # Remove newline but preserve other characters
                clean_line = line.rstrip('\n')

                # Validate line length
                if len(clean_line) != 40:
                    print(f"ERROR: Fatal error - Line {line_num}: Invalid length ({len(clean_line)} chars)")
                    continue

                try:
                    # Extract fields with positional validation
                    tr_code_str = clean_line[0:2]
                    name = clean_line[3:23]  # 20 characters
                    account_number = clean_line[24:29]
                    amount_str = clean_line[30:38]  # 8 characters
                    misc = clean_line[39:41]  # 2 characters

                    # Validate transaction code
                    if not tr_code_str.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction code format")
                        continue

                    # Validate account number format (5 digits)
                    if not account_number.isdigit():
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid account number format")
                        continue

                    # Validate transaction amount format (XXXXX.XX)
                    if (len(amount_str) != 8 or
                            amount_str[5] != '.' or
                            not amount_str[:5].isdigit() or
                            not amount_str[6:].isdigit()):
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction amount format")
                        continue

                    # Convert numerical values
                    tr_code = int(tr_code_str)
                    amount = float(amount_str)

                    # Validate business constraints
                    if amount < 0:
                        print(f"ERROR: Fatal error - Line {line_num}: Negative balance")
                        continue
                    if tr_code < 0 or tr_code > 8:
                        print(f"ERROR: Fatal error - Line {line_num}: Invalid transaction code '{tr_code_str}'")
                        continue

                    transactions.append({
                        'transaction_code': tr_code,
                        'name': name.strip(),
                        'account_number': account_number.lstrip('0') or '0',
                        'amount': amount,
                        'misc': misc
                    })

                except Exception as e:
                    print(f"ERROR: Fatal error - Line {line_num}: Unexpected error: {str(e)}")
                    continue

        return transactions


    # //// STARTER CODE: DO NOT ALTER ////
    @staticmethod
    def write_new_current_accounts(accounts, file_path):
        """
        Writes Current Bank Accounts File with strict format validation.
        Raises ValueError for invalid data to enable testing.
        """
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

                # Format fields
                acc_num = acc['account_number'].zfill(5)
                name = acc['name'].ljust(20)[:20]
                balance = f"{acc['balance']:08.2f}"

                file.write(f"{acc_num} {name} {acc['status']} {balance}\n")

            # Add END_OF_FILE marker
            file.write("00000 END_OF_FILE          A 00000.00\n")



    @staticmethod
    def write_new_master_accounts(accounts, file_path):
        """
        Writes New Master Bank Accounts File with strict format validation.
        Raises ValueError for invalid data to enable testing.
        """
        with open(file_path, 'w') as file:
            accounts.sort(key=lambda x,y: x['account_number'] < y['account_number'])
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

                # Format fields
                acc_num = acc['account_number'].zfill(5)
                name = acc['name'].ljust(20)[:20]
                balance = f"{acc['balance']:08.2f}"
                tot_tr = acc['total_transactions'].zfill(4)

                file.write(f"{acc_num} {name} {acc['status']} {balance} {tot_tr}\n")
