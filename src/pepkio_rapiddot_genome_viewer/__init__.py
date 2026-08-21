"""Python client for Pepkio rapiddot-genome-viewer tool."""

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL, get_api_base_url, get_api_key
from .exceptions import (
    PepkioAPIError,
    PepkioAuthError,
    PepkioError,
    PepkioNotFoundError,
    PepkioValidationError,
)
from .models import (
    ContigRange,
    DotPlotDot,
    Manifest,
    ManifestExample,
    RunOptions,
    RunResult,
    ToolInput,
    ToolResult,
)

__all__ = [
    "PepkioClient",
    "DEFAULT_API_BASE_URL",
    "get_api_base_url",
    "get_api_key",
    "PepkioError",
    "PepkioAPIError",
    "PepkioAuthError",
    "PepkioNotFoundError",
    "PepkioValidationError",
    "ToolInput",
    "RunOptions",
    "ContigRange",
    "DotPlotDot",
    "ToolResult",
    "RunResult",
    "ManifestExample",
    "Manifest",
]
