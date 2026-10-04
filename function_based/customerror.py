
class MissingManifestError(Exception):
    """Exception raised when a required manifest file is missing."""
    pass

class InvalidRowError(Exception):
    """Exception raised when a row in the manifest is invalid or malformed."""
    pass

class EmptyInputError(Exception):
    """Exception raised when the input data is empty or contains no valid manifests."""
    pass