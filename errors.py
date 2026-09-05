class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass

class UserAlreadyExistsError(Exception):
    """Raised when a signup attempt is made with an email that already exists."""
    pass
