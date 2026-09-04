class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass