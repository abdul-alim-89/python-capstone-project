"""Custom error classes for the compliance service."""
class CustomError(Exception):
    """Base class for custom exceptions in the compliance service."""
    pass

class MissingManifestError(CustomError):
    """Exception raised when a required manifest file is missing."""
    pass

class InvalidRowError(CustomError):
    """Exception raised when a row in the manifest is invalid or malformed."""
    pass

class EmptyInputError(CustomError):
    """Exception raised when the input data is empty or contains no valid manifests."""
    pass