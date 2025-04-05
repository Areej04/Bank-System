import pytest
from FileIO import FileIO

# Fixture to create a temporary file for testing
@pytest.fixture
def create_temp_file(tmpdir):
    return tmpdir.join("temp_test_file.txt")

# Test case: valid transactions
def test_valid_transactions(create_temp_file):
    # Test content with two transactions
    content = """01 John Smith        12345 1000.00 NP
02 Jane Doe          67890 1500.50 SP
"""
    # Ensure each line is exactly 41 characters by padding with spaces
    content = "\n".join([line.ljust(41) for line in content.split("\n")])

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that exactly 2 valid transactions are read
    assert len(transactions) == 2  # Expecting 2 valid transactions


# Test case: a single valid transaction
def test_single_transaction(create_temp_file):
    # Test content with one valid transaction
    content = """01 John Smith        12345 1000.00 NP
"""
    # Ensure the line is exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that exactly one valid transaction is read
    assert len(transactions) == 1  # Expecting 1 valid transaction


# Test case: invalid length (less than 41 characters)
def test_invalid_length(create_temp_file):
    # Test content with a line shorter than 41 characters
    content = """01 John Smith        12345 1000.00
"""
    # Pad the line to exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that no transactions are read due to invalid length
    assert len(transactions) == 0  # No valid transactions should be read


# Test case: invalid format (missing amount)
def test_invalid_format(create_temp_file):
    # Test content with a line missing the amount
    content = """01 John Smith        12345
"""
    # Pad the line to exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that no transactions are read due to invalid format
    assert len(transactions) == 0  # No valid transactions should be read


# Test case: valid transaction with maximum field lengths
def test_maximum_field_lengths(create_temp_file):
    # Test content with a transaction where fields are at max length
    content = """01 AAAAAAAAAAAAAAAAAAAA 12345 99999.99 NP
"""
    # Ensure the line is exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that exactly 1 valid transaction is read
    assert len(transactions) == 1  # Expecting 1 valid transaction


# Test case: invalid transaction code
def test_invalid_transaction_code(create_temp_file):
    # Test content with an invalid transaction code (e.g., 99)
    content = """99 John Smith        12345 1000.00 NP
"""
    # Ensure the line is exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that no transactions are read due to invalid transaction code
    assert len(transactions) == 0  # No valid transactions should be read


# Test case: invalid account number (non-numeric)
def test_invalid_account_number(create_temp_file):
    # Test content with a non-numeric account number
    content = """01 John Smith        123A0 1000.00 NP
"""
    # Ensure the line is exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that no transactions are read due to invalid account number format
    assert len(transactions) == 0  # No valid transactions should be read


# Test case: invalid amount format (incorrect decimal separator)
def test_invalid_amount_format(create_temp_file):
    # Test content with an incorrect decimal separator
    content = """01 John Smith        12345 1000,00 NP
"""
    # Ensure the line is exactly 41 characters
    content = content.ljust(41)

    # Write the content to the temporary file
    with open(create_temp_file, 'w') as file:
        file.write(content)

    # Read the transactions using FileIO
    transactions = FileIO.read_transactions(create_temp_file)

    # Assert that no transactions are read due to invalid amount format
    assert len(transactions) == 0  # No valid transactions should be rea