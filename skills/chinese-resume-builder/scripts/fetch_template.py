#!/usr/bin/env python3
"""Fetch an upstream resume template repository safely."""

from __future__ import annotations

import argparse
import shlex
import subprocess
from pathlib import Path


def build_clone_command(repo: str, dest: Path, branch: str | None) -> list[str]:
    command = ["git", "clone", "--depth", "1"]
    if branch:
        command.extend(["--branch", branch])
    command.extend([repo, str(dest)])
    return command


def validate_destination(dest: Path) -> None:
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"destination already exists and is not empty: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Git repository URL")
    parser.add_argument("--dest", required=True, help="Destination directory")
    parser.add_argument("--branch", help="Optional branch or tag to clone")
    parser.add_argument("--dry-run", action="store_true", help="Print the command only")
    args = parser.parse_args()

    dest = Path(args.dest).expanduser().resolve()
    command = build_clone_command(args.repo, dest, args.branch)

    if args.dry_run:
        print(shlex.join(command))
        return 0

    validate_destination(dest)
    subprocess.run(command, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
