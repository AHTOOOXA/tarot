class AppException(Exception):
    """Base exception for application-specific errors"""


class UserNotFoundException(AppException):
    """Raised when a user is not found"""


class FriendAlreadyExistsException(AppException):
    """Raised when trying to add an existing friend"""
