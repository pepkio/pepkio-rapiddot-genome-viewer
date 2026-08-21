import os

DEFAULT_API_BASE_URL = "https://tools.pepkio.com"


def get_api_base_url(custom_base_url: str | None = None) -> str:
    """Return configured API base URL, preferring passed value over environment variable."""
    if custom_base_url:
        url = custom_base_url
    else:
        url = os.getenv("PEPKIO_API_BASE_URL", DEFAULT_API_BASE_URL)
    return url.rstrip("/")


def get_api_key(custom_api_key: str | None = None) -> str | None:
    """Return API key, preferring explicitly passed value over environment variable."""
    if custom_api_key:
        return custom_api_key
    return os.getenv("PEPKIO_API_KEY") or os.getenv("LOCAL_PEPKIO_API_KEY")


def get_verify_ssl(custom_verify: bool | None = None) -> bool:
    """Return SSL verification setting."""
    if custom_verify is not None:
        return custom_verify
    val = os.getenv("PEPKIO_VERIFY_SSL", "true").lower()
    return val not in ("false", "0", "no", "off")
