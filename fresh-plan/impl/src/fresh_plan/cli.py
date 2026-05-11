"""CLI: `fresh-plan-validate` (B1) + `fresh-plan-run` (B2).

Per D36 setup decision B.2: Python primary. CLI library: click (mature,
declarative, low ceremony).
"""
from __future__ import annotations

import importlib.util
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


@click.command(name="fresh-plan-run")
@click.argument(
    "workspace_manifest", type=click.Path(exists=True, dir_okay=False, path_type=Path)
)
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
    "--scenario",
    required=False,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help=(
        "Optional Python module defining `def run(ws: Workspace): ...`. "
        "Without it, the CLI boots + shuts down (sanity check)."
    ),
)
def run(
    workspace_manifest: Path,
    extensions_dir: Path,
    schemas_dir: Path | None,
    scenario: Path | None,
) -> None:
    """Boot a workspace via the B2 in-process substrate; optionally run a scenario.

    Per the B2 brief: exits 0 on success; non-zero with a structured error
    report on failure (boot failure or runtime exception).
    """
    from fresh_plan.runtime import (
        EventRejected,
        MalformedEventError,
        Workspace,
        WorkspaceBootError,
    )

    manifest = _load_manifest(workspace_manifest)
    try:
        ws = Workspace.boot(manifest, extensions_dir, schemas_dir)
    except WorkspaceBootError as e:
        click.echo(f"Boot FAILED: {len(e.failures)} failure(s).", err=True)
        for f in e.failures:
            click.echo(f"  [{f.category}] {f.path}: {f.reason}", err=True)
        sys.exit(2)

    exit_code = 0
    try:
        if scenario is not None:
            spec = importlib.util.spec_from_file_location("_scenario", scenario)
            if spec is None or spec.loader is None:
                click.echo(f"Could not load scenario {scenario}", err=True)
                exit_code = 3
            else:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if not hasattr(module, "run"):
                    click.echo(
                        f"Scenario {scenario} must define `def run(ws): ...`",
                        err=True,
                    )
                    exit_code = 3
                else:
                    module.run(ws)
                    click.echo(
                        f"Scenario completed; event chain length = {len(ws.event_chain)}."
                    )
        else:
            click.echo(
                f"Workspace booted ({ws.workspace_id}); no scenario; shutting down."
            )
    except (EventRejected, MalformedEventError) as e:
        click.echo(f"Runtime FAILED: {e}", err=True)
        exit_code = 4
    except Exception as e:  # noqa: BLE001 — surface unexpected scenario errors
        click.echo(f"Scenario raised: {e}", err=True)
        exit_code = 5
    finally:
        ws.shutdown()
    sys.exit(exit_code)


if __name__ == "__main__":  # pragma: no cover
    main()
