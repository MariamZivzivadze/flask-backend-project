"""Flask application entry point: routes, config, and error handlers."""
class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""
    pass


class InvalidCredentialsError(Exception):
    """Raised when login credentials are invalid."""
    pass

class UserAlreadyExistsError(Exception):
    """Raised when a signup attempt is made with an email that already exists."""
    pass

class MissingFieldError(Exception):
    """Raised when a request is missing one or more required fields."""
    pass