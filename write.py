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
