"""
create_release.py – Create a GitHub Release from a pending-release metadata file.

Called by the workflow AFTER commit+push so the release points to the correct commit.

Usage:
  python scripts/create_release.py state/tq-pending-release.json
"""

import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

import release as release_module


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: create_release.py <pending-release.json>")
        sys.exit(1)

    meta_path = Path(sys.argv[1])
    if not meta_path.exists():
        print(f"No metadata file at {meta_path}, nothing to release.")
        sys.exit(0)

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    server = meta["server"]
    build = meta["build"]
    changed_langs = meta["changed_langs"]
    changes_md = Path(meta["changes_md"])
    body = meta.get(
        "summary") or f"Localization update for {server} build {build}."

    print(
        f"Creating release {server.lower()}-{build} with langs: {changed_langs}"
    )

    url = release_module.create_release(
        server,
        build,
        changed_langs,
        changes_md_path=changes_md if changes_md.exists() else None,
        body=body,
    )
    print(f"Release created: {url}")

    # Remove metadata so a re-run of the workflow doesn't re-create the release
    meta_path.unlink()
    print(f"Removed {meta_path}")


if __name__ == "__main__":
    main()
