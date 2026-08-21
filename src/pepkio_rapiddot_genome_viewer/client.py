import time
from typing import Any, Dict, Optional, Union

import httpx

from .config import get_api_base_url, get_api_key, get_verify_ssl
from .exceptions import (
    PepkioAPIError,
    PepkioAuthError,
    PepkioNotFoundError,
    PepkioValidationError,
)
from .models import Manifest, RunOptions, RunResult, ToolInput

TOOL_ID = "rapiddot-genome-viewer"


class PepkioClient:
    """Client for interacting with Pepkio rapiddot-genome-viewer REST API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        verify: Optional[bool] = None,
    ):
        self.base_url = get_api_base_url(base_url)
        self.api_key = get_api_key(api_key)
        self.timeout = timeout
        self.verify = get_verify_ssl(verify)

    def _get_headers(self, requires_auth: bool = True) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif requires_auth:
            raise PepkioAuthError(
                "PEPKIO_API_KEY is required for tool execution. "
                "Provide it via PepkioClient(api_key=...) or set PEPKIO_API_KEY env var."
            )
        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        if response.status_code in (401, 403):
            raise PepkioAuthError(
                f"Authentication failed ({response.status_code}): {response.text}",
                status_code=response.status_code,
            )
        elif response.status_code == 404:
            raise PepkioNotFoundError(
                f"Resource not found (404): {response.text}",
                status_code=404,
            )
        elif response.status_code >= 400:
            raise PepkioAPIError(
                f"API request failed ({response.status_code}): {response.text}",
                status_code=response.status_code,
            )

        try:
            data = response.json()
        except Exception as e:
            raise PepkioAPIError(f"Failed to parse JSON response: {e}") from e

        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            msg = err if isinstance(err, str) else str(err)
            raise PepkioAPIError(f"API returned error: {msg}", response_data=data)

        return data

    def get_manifest(self) -> Dict[str, Any]:
        """Fetch raw manifest dictionary for rapiddot-genome-viewer."""
        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/manifest"
        headers = self._get_headers(requires_auth=False)
        with httpx.Client(timeout=self.timeout, verify=self.verify) as client:
            resp = client.get(url, headers=headers)
            return self._handle_response(resp)

    def get_manifest_model(self) -> Manifest:
        """Fetch typed Manifest object for rapiddot-genome-viewer."""
        raw = self.get_manifest()
        return Manifest.model_validate(raw)

    def run(
        self,
        input: Union[Dict[str, Any], ToolInput],
        options: Optional[Union[Dict[str, Any], RunOptions]] = None,
        poll: bool = False,
        poll_interval: float = 1.0,
        max_wait_sec: float = 60.0,
        **options_kwargs,
    ) -> RunResult:
        """Execute rapiddot-genome-viewer tool.

        :param input: Input parameters (dict or ToolInput)
        :param options: Optional execution options (dict or RunOptions)
        :param poll: If True and run is async (status queued/running), poll until completion
        :param poll_interval: Polling interval in seconds
        :param max_wait_sec: Maximum time to wait during polling
        :return: RunResult object
        """
        if isinstance(input, ToolInput):
            input_dict = input.model_dump(exclude_none=True)
        elif isinstance(input, dict):
            input_dict = input
        else:
            raise PepkioValidationError("Input must be a dict or ToolInput instance.")

        opts_dict: Dict[str, Any] = {}
        if isinstance(options, RunOptions):
            opts_dict.update(options.model_dump(exclude_none=True))
        elif isinstance(options, dict):
            opts_dict.update(options)

        opts_dict.update({k: v for k, v in options_kwargs.items() if v is not None})

        payload = {
            "input": input_dict,
            "options": opts_dict,
        }

        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/run"
        headers = self._get_headers(requires_auth=True)

        with httpx.Client(timeout=self.timeout, verify=self.verify) as client:
            resp = client.post(url, headers=headers, json=payload)
            raw = self._handle_response(resp)
            result = RunResult.model_validate(raw)

        if poll and result.status in ("queued", "running"):
            start_time = time.time()
            while result.status in ("queued", "running"):
                if time.time() - start_time > max_wait_sec:
                    raise PepkioAPIError(
                        f"Run {result.run_id} timed out after {max_wait_sec} seconds."
                    )
                time.sleep(poll_interval)
                result = self.get_run(result.run_id)

        return result

    def get_run(self, run_id: str) -> RunResult:
        """Fetch status and result of a tool run by run_id."""
        url = f"{self.base_url}/api/tools/v1/runs/{run_id}"
        headers = self._get_headers(requires_auth=False)
        with httpx.Client(timeout=self.timeout, verify=self.verify) as client:
            resp = client.get(url, headers=headers)
            raw = self._handle_response(resp)
            return RunResult.model_validate(raw)

    async def aget_manifest(self) -> Dict[str, Any]:
        """Fetch raw manifest asynchronously."""
        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/manifest"
        headers = self._get_headers(requires_auth=False)
        async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify) as client:
            resp = await client.get(url, headers=headers)
            return self._handle_response(resp)

    async def arun(
        self,
        input: Union[Dict[str, Any], ToolInput],
        options: Optional[Union[Dict[str, Any], RunOptions]] = None,
        **options_kwargs,
    ) -> RunResult:
        """Execute tool asynchronously."""
        if isinstance(input, ToolInput):
            input_dict = input.model_dump(exclude_none=True)
        elif isinstance(input, dict):
            input_dict = input
        else:
            raise PepkioValidationError("Input must be a dict or ToolInput instance.")

        opts_dict: Dict[str, Any] = {}
        if isinstance(options, RunOptions):
            opts_dict.update(options.model_dump(exclude_none=True))
        elif isinstance(options, dict):
            opts_dict.update(options)

        opts_dict.update({k: v for k, v in options_kwargs.items() if v is not None})

        payload = {
            "input": input_dict,
            "options": opts_dict,
        }

        url = f"{self.base_url}/api/tools/v1/tools/{TOOL_ID}/run"
        headers = self._get_headers(requires_auth=True)

        async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify) as client:
            resp = await client.post(url, headers=headers, json=payload)
            raw = self._handle_response(resp)
            return RunResult.model_validate(raw)

    async def aget_run(self, run_id: str) -> RunResult:
        """Fetch run status asynchronously."""
        url = f"{self.base_url}/api/tools/v1/runs/{run_id}"
        headers = self._get_headers(requires_auth=False)
        async with httpx.AsyncClient(timeout=self.timeout, verify=self.verify) as client:
            resp = await client.get(url, headers=headers)
            raw = self._handle_response(resp)
            return RunResult.model_validate(raw)
