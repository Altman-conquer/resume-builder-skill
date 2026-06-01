#!/usr/bin/env python3
"""Normalize resume template URLs and expose license lookup metadata."""

from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse


def normalize_repo_name(name: str) -> str:
    return name[:-4] if name.endswith(".git") else name


def inspect_url(url: str) -> dict:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]

    payload = {
        "url": url,
        "host": host,
        "path": parsed.path,
        "owner": None,
        "repo": None,
        "license_api_url": None,
        "license_page_url": None,
    }

    if host in {"github.com", "www.github.com"} and len(path_parts) >= 2:
        owner = path_parts[0]
        repo = normalize_repo_name(path_parts[1])
        payload.update(
            {
                "host": "github.com",
                "owner": owner,
                "repo": repo,
                "license_api_url": f"https://api.github.com/repos/{owner}/{repo}/license",
                "license_page_url": f"https://github.com/{owner}/{repo}",
            }
        )
    elif host in {"gitee.com", "www.gitee.com"} and len(path_parts) >= 2:
        owner = path_parts[0]
        repo = normalize_repo_name(path_parts[1])
        payload.update(
            {
                "host": "gitee.com",
                "owner": owner,
                "repo": repo,
                "license_page_url": f"https://gitee.com/{owner}/{repo}",
            }
        )

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True, help="Template repository or project URL")
    args = parser.parse_args()

    print(json.dumps(inspect_url(args.url), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
