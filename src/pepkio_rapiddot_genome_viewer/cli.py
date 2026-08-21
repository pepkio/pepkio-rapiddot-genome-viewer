import json
import sys
from typing import Optional

import click

from .client import PepkioClient
from .config import DEFAULT_API_BASE_URL
from .exceptions import PepkioError


@click.group()
def main():
    """CLI tool for Pepkio rapiddot-genome-viewer REST API."""
    pass


@main.command()
@click.option(
    "--base-url",
    default=None,
    help=f"API base URL (default: {DEFAULT_API_BASE_URL} or PEPKIO_API_BASE_URL env var)",
)
@click.option("--json", "json_output", is_flag=True, help="Print raw JSON output")
def manifest(base_url: Optional[str], json_output: bool):
    """Fetch and display the tool manifest."""
    try:
        client = PepkioClient(base_url=base_url)
        man_dict = client.get_manifest()
        if json_output:
            click.echo(json.dumps(man_dict, indent=2))
        else:
            click.echo(f"Tool ID:     {man_dict.get('tool_id')}")
            click.echo(f"Title:       {man_dict.get('title')}")
            click.echo(f"Description: {man_dict.get('description', '').strip()}")
            click.echo(f"Category:    {man_dict.get('category')}")
            click.echo(f"Exec Mode:   {man_dict.get('execution_mode')}")
            examples = man_dict.get("examples", [])
            if examples:
                click.echo("\nAvailable Examples:")
                for ex in examples:
                    click.echo(f"  - {ex.get('name')}")
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--example",
    help="Run using a manifest example name (e.g. identical_short_dna, self_repeat, protein_pair)",
)
@click.option("--input-json", help="Input parameters formatted as JSON string")
@click.option(
    "--input-file", type=click.Path(exists=True), help="Path to JSON file containing input"
)
@click.option("--base-url", help="Override API base URL")
@click.option("--api-key", help="Pepkio API key (or set PEPKIO_API_KEY env var)")
@click.option(
    "--poll/--no-poll",
    default=False,
    help="Poll until completion if run status is queued/running",
)
@click.option("--output-json", type=click.Path(), help="Optional file path to save response JSON")
def run(
    example: Optional[str],
    input_json: Optional[str],
    input_file: Optional[str],
    base_url: Optional[str],
    api_key: Optional[str],
    poll: bool,
    output_json: Optional[str],
):
    """Execute rapiddot-genome-viewer tool."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)

        input_data = None

        if example:
            manifest_dict = client.get_manifest()
            examples = manifest_dict.get("examples", [])
            matched = [e for e in examples if e.get("name") == example]
            if not matched:
                avail = ", ".join([e.get("name", "") for e in examples])
                click.echo(
                    f"Error: Example '{example}' not found. Available examples: {avail}",
                    err=True,
                )
                sys.exit(1)
            input_data = matched[0].get("input")
        elif input_json:
            try:
                input_data = json.loads(input_json)
            except json.JSONDecodeError as e:
                click.echo(f"Error: Invalid JSON in --input-json: {e}", err=True)
                sys.exit(1)
        elif input_file:
            try:
                with open(input_file, "r", encoding="utf-8") as f:
                    input_data = json.load(f)
            except Exception as e:
                click.echo(f"Error reading input file '{input_file}': {e}", err=True)
                sys.exit(1)

        if input_data is None:
            click.echo(
                "Error: Must specify one of --example, --input-json, or --input-file.",
                err=True,
            )
            sys.exit(1)

        res = client.run(input=input_data, poll=poll)
        res_dict = res.model_dump(exclude_none=True)

        if output_json:
            with open(output_json, "w", encoding="utf-8") as f:
                json.dump(res_dict, f, indent=2)
            click.echo(f"Result saved to {output_json}")
        else:
            click.echo(json.dumps(res_dict, indent=2))

    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@main.command(name="get-run")
@click.argument("run_id")
@click.option("--base-url", help="Override API base URL")
@click.option("--api-key", help="Pepkio API key")
def get_run(run_id: str, base_url: Optional[str], api_key: Optional[str]):
    """Fetch status and result of a run by run_id."""
    try:
        client = PepkioClient(api_key=api_key, base_url=base_url)
        res = client.get_run(run_id)
        click.echo(json.dumps(res.model_dump(exclude_none=True), indent=2))
    except PepkioError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
