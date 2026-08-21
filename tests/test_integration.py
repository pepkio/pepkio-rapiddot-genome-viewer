import os

import pytest
from dotenv import load_dotenv

from pepkio_rapiddot_genome_viewer import PepkioClient, get_api_key

# Load environment variables from parent workspace .env if present
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))


def get_test_client() -> PepkioClient:
    api_key = get_api_key()
    if not api_key:
        pytest.skip("PEPKIO_API_KEY / LOCAL_PEPKIO_API_KEY not set in environment.")
    base_url = os.getenv("PEPKIO_API_BASE_URL")
    verify = False if base_url and "localtest.me" in base_url else True
    return PepkioClient(api_key=api_key, base_url=base_url, verify=verify)


def test_integration_manifest():
    base_url = os.getenv("PEPKIO_API_BASE_URL")
    verify = False if base_url and "localtest.me" in base_url else True
    client = PepkioClient(base_url=base_url, verify=verify)
    manifest = client.get_manifest()
    assert manifest.get("tool_id") == "rapiddot-genome-viewer"
    assert "examples" in manifest
    assert len(manifest["examples"]) > 0


def test_integration_run_identical_short_dna():
    client = get_test_client()
    manifest = client.get_manifest()
    examples = {ex["name"]: ex["input"] for ex in manifest.get("examples", [])}

    inp = examples.get(
        "identical_short_dna",
        {
            "mode": "pairwise",
            "query_fasta": ">query\nATCGATCGATCGATCGATCG\n",
            "subject_fasta": ">subject\nATCGATCGATCGATCGATCG\n",
            "kmer_size": 11,
            "min_identity": 75,
        },
    )

    run_res = client.run(input=inp)
    assert run_res.status == "completed"
    assert run_res.result is not None
    assert "dot_count" in run_res.result or "dots" in run_res.result

    # Test get_run
    run_fetch = client.get_run(run_res.run_id)
    assert run_fetch.run_id == run_res.run_id
    assert run_fetch.status == "completed"


def test_integration_run_self_repeat():
    client = get_test_client()
    manifest = client.get_manifest()
    examples = {ex["name"]: ex["input"] for ex in manifest.get("examples", [])}

    inp = examples.get(
        "self_repeat",
        {
            "mode": "self",
            "query_fasta": ">plasmid\nATCGATCGATCGATCGATCGATCGATCG\n",
            "kmer_size": 11,
            "min_identity": 75,
        },
    )

    run_res = client.run(input=inp)
    assert run_res.status == "completed"
    assert run_res.result is not None


def test_integration_run_protein_pair():
    client = get_test_client()
    manifest = client.get_manifest()
    examples = {ex["name"]: ex["input"] for ex in manifest.get("examples", [])}

    inp = examples.get("protein_pair")
    if not inp:
        pytest.skip("protein_pair example not found in manifest")

    run_res = client.run(input=inp)
    assert run_res.status == "completed"
    assert run_res.result is not None
