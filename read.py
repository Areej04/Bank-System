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
