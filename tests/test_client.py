import pytest
from pytest_httpx import HTTPXMock

from pepkio_rapiddot_genome_viewer import (
    Manifest,
    PepkioAPIError,
    PepkioAuthError,
    PepkioClient,
    PepkioNotFoundError,
    RunResult,
    ToolInput,
)


def test_client_init_defaults(monkeypatch):
    monkeypatch.delenv("PEPKIO_API_BASE_URL", raising=False)
    monkeypatch.delenv("PEPKIO_API_KEY", raising=False)
    monkeypatch.delenv("LOCAL_PEPKIO_API_KEY", raising=False)

    client = PepkioClient()
    assert client.base_url == "https://tools.pepkio.com"
    assert client.api_key is None


def test_client_init_custom():
    client = PepkioClient(api_key="test_key", base_url="https://tools.localtest.me/")
    assert client.base_url == "https://tools.localtest.me"
    assert client.api_key == "test_key"


def test_get_manifest(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/manifest",
        json={
            "schema_version": "1.0",
            "tool_id": "rapiddot-genome-viewer",
            "title": "RapidDot Genome Viewer",
            "description": "Browser dot plot",
            "examples": [{"name": "test_ex", "input": {"mode": "pairwise"}}],
        },
        is_reusable=True,
    )

    client = PepkioClient()
    manifest = client.get_manifest()
    assert manifest["tool_id"] == "rapiddot-genome-viewer"
    assert manifest["title"] == "RapidDot Genome Viewer"

    model = client.get_manifest_model()
    assert isinstance(model, Manifest)
    assert model.tool_id == "rapiddot-genome-viewer"


def test_run_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/run",
        method="POST",
        json={
            "run_id": "run-123",
            "status": "completed",
            "result": {
                "sequence_kind": "dna",
                "dot_count": 10,
                "dots": [],
            },
            "error": None,
        },
    )

    client = PepkioClient(api_key="mock-key")
    inp = ToolInput(
        mode="pairwise",
        query_fasta=">q\nATCG\n",
        subject_fasta=">s\nATCG\n",
        kmer_size=11,
    )
    res = client.run(inp)

    assert isinstance(res, RunResult)
    assert res.run_id == "run-123"
    assert res.status == "completed"
    assert res.result["dot_count"] == 10

    # Verify request payload
    request = httpx_mock.get_request()
    assert request is not None
    assert request.headers["Authorization"] == "Bearer mock-key"


def test_get_run_success(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/runs/run-456",
        json={
            "run_id": "run-456",
            "status": "completed",
            "result": {"dot_count": 5},
        },
    )

    client = PepkioClient()
    res = client.get_run("run-456")
    assert res.run_id == "run-456"
    assert res.status == "completed"


def test_missing_api_key_raises_auth_error():
    client = PepkioClient(api_key=None)
    with pytest.raises(PepkioAuthError) as excinfo:
        client.run({"mode": "pairwise"})
    assert "PEPKIO_API_KEY is required" in str(excinfo.value)


def test_http_401_raises_auth_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/run",
        status_code=401,
        text="Unauthorized",
    )

    client = PepkioClient(api_key="bad-key")
    with pytest.raises(PepkioAuthError):
        client.run({"mode": "pairwise"})


def test_http_404_raises_not_found_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/runs/nonexistent",
        status_code=404,
        text="Not found",
    )

    client = PepkioClient()
    with pytest.raises(PepkioNotFoundError):
        client.get_run("nonexistent")


def test_body_error_raises_api_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/run",
        json={
            "run_id": "run-789",
            "status": "failed",
            "error": "Invalid FASTA format",
        },
    )

    client = PepkioClient(api_key="mock-key")
    with pytest.raises(PepkioAPIError) as excinfo:
        client.run({"mode": "pairwise"})
    assert "API returned error: Invalid FASTA format" in str(excinfo.value)


@pytest.mark.asyncio
async def test_async_methods(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/manifest",
        json={"tool_id": "rapiddot-genome-viewer"},
    )
    httpx_mock.add_response(
        url="https://tools.pepkio.com/api/tools/v1/tools/rapiddot-genome-viewer/run",
        json={"run_id": "async-run", "status": "completed"},
    )

    client = PepkioClient(api_key="mock-key")
    manifest = await client.aget_manifest()
    assert manifest["tool_id"] == "rapiddot-genome-viewer"

    run_res = await client.arun({"mode": "pairwise"})
    assert run_res.run_id == "async-run"
