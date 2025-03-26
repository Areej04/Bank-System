class ErrorLogger :
    """
        Handles error logging for contraint violations and fatal errors

    """

    def log_constraint_error(constraint_type, description):
        print(f"Error: {constraint_type}: {description}")


    def log_fatal_error(file_name, description):
        print(f"Error: Fatal error in {file_name}: {description}")