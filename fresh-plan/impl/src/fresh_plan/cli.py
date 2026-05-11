"""CLI: `fresh-plan-validate`.

Per D36 setup decision B.2: Python primary. CLI library: click (mature,
declarative, low ceremony).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import click
import yaml

from fresh_plan.validator import validate_workspace_boot


def _load_manifest(path: Path) -> dict:
    """Parse JSON or YAML by extension."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        return yaml.safe_load(text)
    return json.loads(text)


@click.command(name="fresh-plan-validate")
@click.argument("workspace_manifest", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option(
    "--extensions-dir",
    required=True,
    type=click.Path(file_okay=False, path_type=Path),
    help="Directory under which extensions live (<ext-id>/<version>/extension-manifest.json).",
)
@click.option(
    "--schemas-dir",
    required=False,
    type=click.Path(file_okay=False, exists=True, path_type=Path),
    help="Override path to the Phase A schemas (default: fresh-plan/schemas/).",
)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Emit failures as a JSON document on stdout (machine-readable).",
)
def main(
    workspace_manifest: Path,
    extensions_dir: Path,
    schemas_dir: Path | None,
    json_output: bool,
) -> None:
    """Validate a workspace manifest's boot per D29 + D30 + D32 + D33."""
    manifest = _load_manifest(workspace_manifest)
    result = validate_workspace_boot(manifest, extensions_dir, schemas_dir)

    if json_output:
        payload = {
            "success": result.success,
            "failures": [
                {
                    "category": f.category,
                    "path": f.path,
                    "reason": f.reason,
                    "value": f.value,
                    "declarers": f.declarers,
                }
                for f in result.failures
            ],
        }
        click.echo(json.dumps(payload, indent=2, default=str))
        sys.exit(0 if result.success else 1)

    if result.success:
        n_ext = len(result.loaded_extensions or {})
        click.echo(f"Validation succeeded; {n_ext} extension(s) loaded.")
        sys.exit(0)

    click.echo(f"Validation FAILED: {len(result.failures)} failure(s).", err=True)
    for f in result.failures:
        click.echo(f"  [{f.category}] {f.path}", err=True)
        click.echo(f"      reason: {f.reason}", err=True)
        if f.value is not None:
            click.echo(f"      value:  {f.value!r}", err=True)
        if f.declarers:
            click.echo(f"      declarers:", err=True)
            for d in f.declarers:
                click.echo(f"        - {d}", err=True)
    sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
