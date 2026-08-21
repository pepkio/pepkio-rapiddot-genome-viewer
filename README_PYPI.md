# pepkio-rapiddot-genome-viewer

Python client for Pepkio rapiddot-genome-viewer tool.

## Usage

```python
from pepkio_rapiddot_genome_viewer import PepkioClient

client = PepkioClient(api_key="YOUR_API_KEY")
res = client.run(
    input={
        "mode": "pairwise",
        "query_fasta": ">q\nATCGATCGATCG\n",
        "subject_fasta": ">s\nATCGATCGATCG\n",
        "kmer_size": 11,
    }
)
print(res.status)
```
