"""Custom exception hierarchy for pyopenf1.

All exceptions inherit from :class:`PyOpenF1Error` so callers can catch a
single base type for broad error handling, or specific subtypes for
fine-grained control.
"""

from __future__ import annotations


class PyOpenF1Error(Exception):
    """Base exception for all pyopenf1 errors."""

    def __init__(self, message: str = "An unexpected pyopenf1 error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


class APIError(PyOpenF1Error):
    """Raised when the OpenF1 API returns a non-success HTTP status.

    Attributes:
        status_code: The HTTP status code returned by the API.
        response_body: The raw response body, if available.
    """

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        response_body: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class RateLimitError(APIError):
    """Raised when the API returns HTTP 429 (Too Many Requests).

    The caller should back off and retry after the period indicated by the
    ``Retry-After`` header, if present.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded. Please slow down.",
        *,
        status_code: int = 429,
        response_body: str | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, status_code=status_code, response_body=response_body)


class AuthenticationError(APIError):
    """Raised when the API returns HTTP 401 or 403."""

    def __init__(
        self,
        message: str = "Authentication failed.",
        *,
        status_code: int = 401,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class NotFoundError(APIError):
    """Raised when the API returns HTTP 404."""

    def __init__(
        self,
        message: str = "The requested resource was not found.",
        *,
        status_code: int = 404,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)


class ServerError(APIError):
    """Raised when the API returns an HTTP 5xx status."""

    def __init__(
        self,
        message: str = "The server encountered an internal error.",
        *,
        status_code: int = 500,
        response_body: str | None = None,
    ) -> None:
        super().__init__(message, status_code=status_code, response_body=response_body)
