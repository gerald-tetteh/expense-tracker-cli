class DBNotInitializedError(Exception):
    """Exception raised when the database is not initialized."""
    pass


class InvalidImportFileError(Exception):
    """Exception raised when the expense import file is malformed"""
    pass
