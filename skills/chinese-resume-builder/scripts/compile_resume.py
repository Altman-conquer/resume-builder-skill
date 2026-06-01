#!/usr/bin/env python3
"""Detect and run common resume template build commands."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


def choose_tex_file(project: Path) -> Path | None:
    preferred = ["resume.tex", "resume-zh_CN.tex", "main.tex", "cv.tex"]
    for name in preferred:
        candidate = project / name
        if candidate.exists():
            return candidate

    tex_files = sorted(project.glob("*.tex"))
    return tex_files[0] if tex_files else None


def detect_command(project: Path) -> list[str]:
    typ_files = sorted(project.glob("*.typ"))
    if typ_files:
        target = next((path for path in typ_files if path.name == "main.typ"), typ_files[0])
        return ["typst", "compile", target.name]

    tex_file = choose_tex_file(project)
    if tex_file:
        content = tex_file.read_text(encoding="utf-8", errors="ignore")
        engine = "xelatex"
        if "pdflatex" in content and "fontspec" not in content:
            engine = "pdflatex"
        return [engine, "-interaction=nonstopmode", "-halt-on-error", tex_file.name]

    if (project / "package.json").exists():
        return ["npm", "run", "build"]

    if (project / "resume.md").exists():
        return ["pandoc", "resume.md", "-o", "resume.pdf"]

    raise SystemExit(f"could not detect a resume build command in {project}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Template or resume project directory")
    parser.add_argument("--dry-run", action="store_true", help="Print detected command only")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    if not project.is_dir():
        raise SystemExit(f"project directory not found: {project}")

    command = detect_command(project)
    if args.dry_run:
        print(shlex.join(command))
        return 0

    subprocess.run(command, cwd=project, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
