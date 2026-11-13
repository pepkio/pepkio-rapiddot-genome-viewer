# Pepkio RapidDot Genome Viewer

Generate comparative sequence dot plots and identify genomic synteny, inversions, and repeat structures from DNA or protein sequences via Python or CLI.

# What It Does

Comparing genomic sequences or identifying structural variants—such as inversions, duplications, translocations, and tandem repeats—often requires dot plot visual matrix alignments. Traditional desktop tools can be cumbersome to automate or integrate into computational workflows, while manual matrix generation lacks synteny ordering and PAF/BLAST alignment import.

This package provides a Python client and CLI interface for the Pepkio Tools REST API to compute fast k-mer dot plots and window-based protein similarity matrices. It performs pairwise sequence comparisons, self-dotplot repeat characterizations, and PAF/BLAST tabular alignment conversions, outputting coordinates, match metrics, and synteny-oriented contig orders.

Programmatic runs require an active network connection and a Pepkio API key. Calculations are processed via the remote API service.

# Features

- **Pairwise & Self-Dotplot Modes**: Compare two distinct sequences or analyze a single sequence for tandem and inverted repeats.
- **DNA & Protein Compatibility**: Exact k-mer matching for DNA sequences and BLOSUM62 window scoring for protein sequences.
- **Alignment Import**: Direct ingestion of minimap2 PAF or BLAST tabular format files.
- **Contig Synteny Ordering**: Automatic sorting of query contigs against subject reference sequences to highlight collinear synteny blocks.
- **Customizable Window Filtering**: Select k-mer sizes (11, 15, 21, 31), minimum identity thresholds (0–100%), and strand orientation filters.
- **GFF3 Track Support**: Ingest GFF3 genomic annotations to correlate dot plot features with gene boundaries.
- **API Manifest & Examples**: Inspect available examples and inputs using `get_manifest()`, `list_examples()`, and `get_example_input()`.
- **Command-Line Interface**: Run dot plot analyses or inspect manifests directly via `pepkio-rapiddot-genome-viewer`.

# Installation

```bash
pip install pepkio-rapiddot-genome-viewer
```

Set your API key as an environment variable before running calculations:

```bash
export PEPKIO_API_KEY="your-api-key"
```

You can obtain an API key from your [Pepkio account API keys](https://www.pepkio.com/account/api-keys) setting page.

# Quick Example

```python
from pepkio_rapiddot_genome_viewer import PepkioClient

with PepkioClient() as client:
    # Pairwise comparison between two sequences
    result = client.run({
        "mode": "pairwise",
        "query_fasta": ">query\nATCGATCGATCGATCGATCG\n",
        "subject_fasta": ">subject\nATCGATCGATCGATCGATCG\n",
        "kmer_size": 11,
        "min_identity": 75,
    })

    print(f"Status: {result.status}")
    print(f"Total matching dots: {result.result['dot_count']}")
    print(f"Query length: {result.result['query_length']} bp")
```

Run via the command-line interface:

```bash
pepkio-rapiddot-genome-viewer run --example identical_short_dna
```

Inspect the tool manifest without an API key:

```bash
pepkio-rapiddot-genome-viewer manifest
```

# Typical Use Cases

- Detecting large-scale genomic rearrangements, inversions, and translocations between bacterial or viral genomes.
- Identifying tandem repeat expansions, palindromes, and inverted repeats in plasmids and synthetic constructs.
- Visualizing whole-genome synteny and chromosome collinearity between closely related species or assembly versions.
- Parsing and plotting long-read alignment outputs from minimap2 PAF or BLAST tabular searches.
- Screening protein domain duplications and modular architecture shifts across homologous protein families.
- Validating de novo genome assembly scaffolding by comparing assembled contigs against reference genomes.

# Scientific Background

Dot matrix analysis is a fundamental bioinformatic method for comparing two biological sequences. One sequence is positioned along the horizontal axis and the other along the vertical axis. A dot is plotted at coordinates $(x, y)$ whenever the sequence window or k-mer starting at position $x$ matches that at position $y$.

Continuous diagonal lines indicate regions of sequence collinearity or homology. Displaced diagonal segments indicate insertions, deletions, or translocations. Diagonal lines running perpendicular (antiparallel) to the main diagonal represent genomic inversions. Off-diagonal parallel lines in a self-comparison plot reveal tandem or interspersed repeats.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available:

Web Application: https://www.pepkio.com/tools/rapiddot-genome-viewer

The web application provides real-time interactive zooming and panning, dynamic SVG and PNG export, interactive contig reordering, multi-track GFF3 feature visualization, and shareable permalinks.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-rapiddot-genome-viewer

Web Application: https://www.pepkio.com/tools/rapiddot-genome-viewer

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

genome dot plot, sequence dot plot, comparative genomics, synteny viewer, genomic rearrangement, sequence alignment, dot matrix analysis, k-mer matching, pairwise dotplot, self dotplot, inverted repeat detection, tandem repeat finder, PAF viewer, BLAST tabular dotplot, minimap2 dot plot, chromosome collinearity, bacterial genome comparison, plasmid repeat analysis, protein dot plot, BLOSUM62 window, contig synteny ordering, GFF3 annotation overlay, structural variant visualization, pepkio-rapiddot-genome-viewer, bioinformatics dot plot Python, fast genome dot plot generator, compare two genomes dot plot, detect inversions in bacterial genomes, self dot plot tandem repeat identification, visualize minimap2 PAF alignment dot plot, blast tabular alignment dot plot viewer, Python client genome synteny dot plot, whole genome collinearity analysis tool, protein domain duplication dot matrix, interactive comparative genomics web app, automated FASTA dot plot generation Python

A semantic, AI-native version of this document in the K2F format is available at https://k2f.dev (https://k2f.dev/v/0cc94d4953514b9ba927f29c4ac05464ae27e67b53731641741177f8e5a31233)
