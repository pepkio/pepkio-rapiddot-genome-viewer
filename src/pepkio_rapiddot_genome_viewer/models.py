from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ToolInput(BaseModel):
    """Typed input model for rapiddot-genome-viewer tool."""

    model_config = ConfigDict(extra="allow")

    mode: Optional[str] = Field(
        default=None, description="pairwise, self, or alignment"
    )
    query_fasta: Optional[str] = Field(
        default=None, description="Query FASTA text (pairwise/self modes)"
    )
    subject_fasta: Optional[str] = Field(
        default=None, description="Subject FASTA text (pairwise mode)"
    )
    alignment_text: Optional[str] = Field(
        default=None, description="PAF or BLAST tabular alignment text"
    )
    alignment_format: Optional[str] = Field(
        default=None, description="paf or blast"
    )
    kmer_size: Optional[int] = Field(
        default=None, description="K-mer/window size (11, 15, 21, or 31)"
    )
    strand_mode: Optional[str] = Field(
        default=None, description="plus_plus, plus_minus, minus_plus, or minus_minus"
    )
    min_identity: Optional[float] = Field(
        default=None, description="Minimum identity percent filter (0-100)"
    )
    auto_sort_contigs: Optional[bool] = Field(
        default=None, description="Auto-sort query contigs by synteny"
    )
    show_contig_grid: Optional[bool] = Field(
        default=None, description="Show contig boundary grid lines"
    )
    gff_text: Optional[str] = Field(
        default=None, description="Optional GFF3 annotation rows"
    )


class RunOptions(BaseModel):
    """Options for running a Pepkio tool."""

    model_config = ConfigDict(extra="allow")

    idempotency_key: Optional[str] = None
    label: Optional[str] = None
    share: Optional[str] = None


class ContigRange(BaseModel):
    """Contig boundary specification."""

    model_config = ConfigDict(extra="allow")

    id: str
    start: int
    end: int
    length: int


class DotPlotDot(BaseModel):
    """Individual dot coordinate in the dotplot."""

    model_config = ConfigDict(extra="allow")

    query_pos: int
    subject_pos: int
    identity: float
    bin: Optional[str] = None
    strand: Optional[str] = None
    query_contig_id: Optional[str] = None
    subject_contig_id: Optional[str] = None


class ToolResult(BaseModel):
    """Execution result details from rapiddot-genome-viewer."""

    model_config = ConfigDict(extra="allow")

    query_length: Optional[int] = None
    subject_length: Optional[int] = None
    sequence_kind: Optional[str] = None
    dot_count: Optional[int] = None
    dots: Optional[List[Dict[str, Any]]] = None
    warnings: Optional[List[str]] = None
    truncated: Optional[bool] = None
    response_truncated: Optional[bool] = None
    query_contigs: Optional[List[Dict[str, Any]]] = None
    subject_contigs: Optional[List[Dict[str, Any]]] = None


class RunResult(BaseModel):
    """Complete run response object returned by Pepkio REST API."""

    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    result_url: Optional[str] = None
    permalink: Optional[str] = None
    duration_ms: Optional[int] = None

    @property
    def typed_result(self) -> Optional[ToolResult]:
        """Parse result into typed ToolResult if present."""
        if self.result:
            return ToolResult.model_validate(self.result)
        return None


class ManifestExample(BaseModel):
    """An example input provided in the tool manifest."""

    model_config = ConfigDict(extra="allow")

    name: str
    input: Dict[str, Any]


class Manifest(BaseModel):
    """Pepkio tool manifest schema."""

    model_config = ConfigDict(extra="allow")

    schema_version: str
    tool_id: str
    title: str
    description: str
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    execution_mode: Optional[str] = None
    estimated_runtime_sec: Optional[int] = None
    input: Dict[str, Any] = Field(default_factory=dict)
    output: Dict[str, Any] = Field(default_factory=dict)
    examples: List[ManifestExample] = Field(default_factory=list)
    agent_notes: Optional[str] = None
    example_prompts: Optional[List[str]] = None
    limits: Optional[Dict[str, Any]] = None
