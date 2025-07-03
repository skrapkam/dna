#!/usr/bin/env python3
"""move_assets.py

Re-organises page-specific asset folders.

For each directory matching *_files at repository root (or any depth) it:
1. Calculates a slug from the directory name with `_files` removed.
2. Creates `src/page-assets/<slug>/` if it does not already exist.
3. Moves the contents of the *_files directory into that destination directory.
4. Locates the HTML page(s) whose basename matches the directory base name and
   rewrites asset references so that paths such as
   `<img src="ENT1-P1_files/abc.jpg">` become
   `<img src="src/page-assets/ent1-p1/abc.jpg">`.

Run from repository root:
    python scripts/move_assets.py
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

# Constants ------------------------------------------------------------
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SRC_PAGE_ASSETS = WORKSPACE_ROOT / "src" / "page-assets"

# Helpers --------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert *text* to a filesystem-friendly slug (lowercase, hyphens)."""
    text = text.lower()
    # Replace any sequence of non-alphanumeric characters with a single dash
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def move_directory_contents(src_dir: Path, dest_dir: Path) -> None:
    """Move all children of *src_dir* into *dest_dir* (creates dest_dir)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    for child in src_dir.iterdir():
        target = dest_dir / child.name
        # If file already exists at destination, skip
        if target.exists():
            print(f"[skip] {target.relative_to(WORKSPACE_ROOT)} already exists")
            continue
        shutil.move(str(child), str(target))

    # Remove the now-empty directory
    try:
        src_dir.rmdir()
    except OSError:
        # Directory not empty (unexpected) – ignore
        pass


def update_html_references(html_path: Path, original_dir: str, slug: str) -> bool:
    """Replace occurrences of original_dir/… with src/page-assets/slug/…

    Returns True if file content changed."""
    rel_new_prefix = f"src/page-assets/{slug}/"
    content = html_path.read_text(encoding="utf-8", errors="ignore")
    new_content = content

    # Replace forward and backslash versions
    new_content = new_content.replace(f"{original_dir}/", rel_new_prefix)
    new_content = new_content.replace(f"{original_dir}\\", rel_new_prefix)

    if new_content != content:
        html_path.write_text(new_content, encoding="utf-8")
        print(f"[update] {html_path.relative_to(WORKSPACE_ROOT)}")
        return True
    return False


# Core -----------------------------------------------------------------

def main() -> None:
    moved_count = 0
    updated_html_count = 0

    # Walk repository looking for *_files directories (depth-first)
    for root, dirs, _files in os.walk(WORKSPACE_ROOT):
        # We mutate dirs in-place, so iterate over a copy
        for dirname in list(dirs):
            if not dirname.endswith("_files"):
                continue

            src_dir = Path(root) / dirname
            base_name = dirname[:-6]  # Strip "_files"
            slug = slugify(base_name)
            dest_dir = SRC_PAGE_ASSETS / slug

            print(f"[move] {src_dir.relative_to(WORKSPACE_ROOT)} -> {dest_dir.relative_to(WORKSPACE_ROOT)}")
            move_directory_contents(src_dir, dest_dir)
            moved_count += 1

            # Possible HTML filenames that reference this directory
            potential_html_names = [f"{base_name}.html", f"{base_name}.htm"]

            # Search for these HTML files anywhere in repo
            for html_name in potential_html_names:
                for html_path in WORKSPACE_ROOT.rglob(html_name):
                    if html_path.is_file():
                        if update_html_references(html_path, dirname, slug):
                            updated_html_count += 1

    print(f"\nComplete! Moved {moved_count} asset folder(s). Updated {updated_html_count} HTML file(s).")


if __name__ == "__main__":
    main()