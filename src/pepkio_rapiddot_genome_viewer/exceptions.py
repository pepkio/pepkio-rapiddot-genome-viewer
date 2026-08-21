from typing import Any, Dict, Optional


class PepkioError(Exception):
    """Base exception for Pepkio client SDK."""

    pass


class PepkioAPIError(PepkioError):
    """Raised when the Pepkio API returns an HTTP error status or explicit error payload."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class PepkioAuthError(PepkioAPIError):
    """Raised when authentication fails (401/403) or API key is missing/invalid."""

    pass


class PepkioNotFoundError(PepkioAPIError):
    """Raised when requested resource (e.g. tool or run) is not found (404)."""

    pass


class PepkioValidationError(PepkioError):
    """Raised when client-side validation of input fails."""

    pass
