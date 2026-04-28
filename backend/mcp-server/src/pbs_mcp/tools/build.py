"""Build tools — compile_latex, scaffold_project."""
from __future__ import annotations

import logging
import re
import shutil
import subprocess
from pathlib import Path

from pbs_mcp.schemas import (
    CompileLatexInput,
    CompileLatexOutput,
    ScaffoldProjectInput,
    ScaffoldProjectOutput,
)

logger = logging.getLogger(__name__)


def compile_latex(input: CompileLatexInput) -> CompileLatexOutput:
    project_dir = Path(input.project_path)
    if not project_dir.is_dir():
        raise FileNotFoundError(f"not a directory: {project_dir}")

    master = input.master_file
    if not master:
        # Auto-detect: look for a file with `\documentclass` at top level
        candidates = list(project_dir.glob("*.tex"))
        for c in candidates:
            try:
                head = c.read_text(encoding="utf-8")[:2000]
                if "\\documentclass" in head:
                    master = c.name
                    break
            except UnicodeDecodeError:
                pass
        if not master:
            return CompileLatexOutput(
                success=False,
                pdf_path=None,
                log_excerpt="No master .tex file with \\documentclass found",
                warnings=[],
                errors=["No master .tex file detected"],
                page_count=None,
            )

    master_path = project_dir / master
    if not master_path.is_file():
        return CompileLatexOutput(
            success=False, pdf_path=None,
            log_excerpt=f"master file not found: {master}",
            warnings=[], errors=[f"master file not found: {master}"],
            page_count=None,
        )

    pdf_name = master_path.stem + ".pdf"
    log_name = master_path.stem + ".log"

    # Prefer latexmk; fall back to pdflatex
    if shutil.which("latexmk"):
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", master]
    else:
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", master]

    try:
        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=600,
        )
        success = result.returncode == 0
    except subprocess.TimeoutExpired:
        return CompileLatexOutput(
            success=False, pdf_path=None,
            log_excerpt="compile timed out after 600s",
            warnings=[], errors=["compile timeout"],
            page_count=None,
        )

    log_path = project_dir / log_name
    log_text = log_path.read_text(encoding="utf-8", errors="ignore") if log_path.is_file() else result.stdout

    warnings = re.findall(r"^.*[Ww]arning:.*$", log_text, flags=re.MULTILINE)
    errors = re.findall(r"^!.+$", log_text, flags=re.MULTILINE)

    pdf_path = project_dir / pdf_name
    page_count = None
    if pdf_path.is_file() and shutil.which("pdfinfo"):
        try:
            info = subprocess.run(
                ["pdfinfo", str(pdf_path)], capture_output=True, text=True, timeout=10
            )
            m = re.search(r"^Pages:\s+(\d+)", info.stdout, flags=re.MULTILINE)
            if m:
                page_count = int(m.group(1))
        except (subprocess.TimeoutExpired, OSError):
            pass

    return CompileLatexOutput(
        success=success and pdf_path.is_file(),
        pdf_path=str(pdf_path) if pdf_path.is_file() else None,
        log_excerpt="\n".join(log_text.splitlines()[-50:]),
        warnings=warnings[:20],
        errors=errors[:20],
        page_count=page_count,
    )


def scaffold_project(input: ScaffoldProjectInput) -> ScaffoldProjectOutput:
    """Copy template tree to a new project root; optionally git-init LaTeX dirs."""
    target = Path(input.target_root)
    if target.exists():
        raise FileExistsError(f"target already exists: {target}")

    if input.template_repo:
        template = Path(input.template_repo)
    else:
        # Default: use the canonical local Friedrichshof template for the doctype
        template_root = Path.home() / "dev" / "Planungsbüro-Schulz"
        if input.doctype == "b-plan-begruendung":
            template = template_root / "22-16-Maxsolar---Friedrichshof---B-Plan---Begruendung"
        elif input.doctype == "b-plan-festsetzungen":
            template = template_root / "22-16-Maxsolar---Friedrichshof---B-Plan-Textliche-Festsetzungen"
        else:
            raise ValueError(f"no default template for doctype: {input.doctype}")

    if not template.is_dir():
        raise FileNotFoundError(f"template not found: {template}")

    # Copy tree, excluding build artifacts and git history
    EXCLUDE = {".git", ".aux", ".fdb_latexmk", ".fls", ".log", ".lot",
               ".pdf", ".synctex.gz", ".toc", ".png", ".jpg", "image"}

    def _ignore(d, names):
        return [n for n in names if any(n.endswith(e) or n.startswith(e) for e in EXCLUDE)]

    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, target, ignore=_ignore, dirs_exist_ok=True)

    created_paths = [str(target)]

    # Patch Projektdaten.tex with provided project data
    projektdaten = target / "Projektdaten.tex"
    if projektdaten.is_file() and input.project_data:
        text = projektdaten.read_text(encoding="utf-8")
        for key, value in input.project_data.items():
            # Replace \newcommand{\Key}{old} with \newcommand{\Key}{new}
            pat = rf"\\newcommand\{{\\{key}\}}\{{[^}}]*\}}"
            new = f"\\newcommand{{\\{key}}}{{{value}}}"
            text = re.sub(pat, new, text)
        projektdaten.write_text(text, encoding="utf-8")

    # git init for Overleaf sync
    git_repos: list[str] = []
    if input.git_init_latex and shutil.which("git"):
        try:
            subprocess.run(
                ["git", "init", "-b", "main"], cwd=target, check=True, capture_output=True, timeout=30
            )
            git_repos.append(str(target))
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            logger.warning(f"git init failed for {target}")

    return ScaffoldProjectOutput(
        name=input.name,
        project_root=str(target),
        created_paths=created_paths,
        git_repos_initialized=git_repos,
    )
