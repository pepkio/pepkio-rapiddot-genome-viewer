# Pepkio RapidDot Genome Viewer Python Client

Python client library and CLI for the Pepkio `rapiddot-genome-viewer` tool.

## Installation

```bash
pip install pepkio-rapiddot-genome-viewer
```

## Quickstart

```python
from pepkio_rapiddot_genome_viewer import PepkioClient

client = PepkioClient(api_key="YOUR_PEPKIO_API_KEY")

# Fetch tool manifest
manifest = client.get_manifest()

# Run genome dot plot alignment
result = client.run(
    input={
        "mode": "pairwise",
        "query_fasta": ">query\nATCGATCGATCGATCGATCG\n",
        "subject_fasta": ">subject\nATCGATCGATCGATCGATCG\n",
        "kmer_size": 11,
        "min_identity": 75,
    }
)

print(f"Status: {result.status}")
print(f"Dot count: {result.result['dot_count']}")
```

## CLI Usage

```bash
# Fetch manifest
pepkio-rapiddot-genome-viewer manifest

# Run with manifest example
pepkio-rapiddot-genome-viewer run --example identical_short_dna
```
