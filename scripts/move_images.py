#!/usr/bin/env python3
"""move_images.py

Move top-level ("loose") image files (jpg/png/gif/svg/webp) into
`public/images/` and rewrite HTML references so they point to `/images/<file>`.

Run from repository root:
    python scripts/move_images.py

The script is idempotent: if an image is already in `public/images/`, it will
be skipped and HTML will not be touched again.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Iterable

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_IMAGES = WORKSPACE_ROOT / "public" / "images"
SRC_PAGE_ASSETS = WORKSPACE_ROOT / "src" / "page-assets"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"}

EXCLUDE_DIR_KEYWORDS = {
    ".git",
    "public/images",
    "src/page-assets",
    "node_modules",
    "scripts",
}

# ----------------------------------------------------------------------

def is_loose_image(path: Path) -> bool:
    """Return True if *path* is an image that should be relocated."""
    if not path.is_file():
        return False
    if path.suffix.lower() not in IMAGE_EXTS:
        return False

    # Fast check: already inside public/images or page-assets → skip
    if str(path).startswith(str(PUBLIC_IMAGES)):
        return False
    if str(path).startswith(str(SRC_PAGE_ASSETS)):
        return False

    # Skip any excluded directory keyword in its parts
    for part in path.parts:
        if part in EXCLUDE_DIR_KEYWORDS or part.endswith("_files"):
            return False
    return True

# ----------------------------------------------------------------------

def collect_loose_images() -> list[Path]:
    """Gather all loose images in repository."""
    images: list[Path] = []
    for p in WORKSPACE_ROOT.rglob("*"):
        if is_loose_image(p):
            images.append(p)
    return images

# ----------------------------------------------------------------------

def move_image(path: Path) -> Path:
    """Move *path* into PUBLIC_IMAGES. Returns new path."""
    PUBLIC_IMAGES.mkdir(parents=True, exist_ok=True)
    dest = PUBLIC_IMAGES / path.name

    if dest.exists():
        if dest.stat().st_size == path.stat().st_size:
            # Assume identical → remove source
            print(f"[dup] {path.relative_to(WORKSPACE_ROOT)} duplicates {dest.relative_to(WORKSPACE_ROOT)} – deleting source")
            path.unlink()
            return dest
        else:
            # Name clash – make unique
            stem, ext = path.stem, path.suffix
            i = 1
            while True:
                candidate = PUBLIC_IMAGES / f"{stem}_{i}{ext}"
                if not candidate.exists():
                    dest = candidate
                    break
                i += 1
    print(f"[move] {path.relative_to(WORKSPACE_ROOT)} -> {dest.relative_to(WORKSPACE_ROOT)}")
    shutil.move(str(path), str(dest))
    return dest

# ----------------------------------------------------------------------

def update_html_files(image_names: Iterable[str]):
    """Replace references to moved images inside all HTML files."""
    # Prepare regex mapping for efficiency
    patterns = {
        name: re.compile(rf"(src|href)=(['\"])([^'\"]*?){re.escape(name)}(['\"])", re.IGNORECASE)
        for name in image_names
    }

    html_files = list(WORKSPACE_ROOT.rglob("*.htm")) + list(WORKSPACE_ROOT.rglob("*.html"))
    updated = 0
    for html_path in html_files:
        # Skip files inside public or scripts to avoid recompilation
        if str(html_path).startswith(str(PUBLIC_IMAGES)) or "scripts" in html_path.parts:
            continue

        content = html_path.read_text(encoding="utf-8", errors="ignore")
        original = content

        for name, pat in patterns.items():
            replacement = rf"\1=\2/images/{name}\4"
            content = pat.sub(replacement, content)

        if content != original:
            html_path.write_text(content, encoding="utf-8")
            print(f"[update] {html_path.relative_to(WORKSPACE_ROOT)}")
            updated += 1
    print(f"Updated {updated} HTML file(s) with new /images/ paths.")

# ----------------------------------------------------------------------

def main() -> None:
    loose_images = collect_loose_images()
    if not loose_images:
        print("No loose images found – nothing to do.")
        return

    image_names_moved: list[str] = []
    for img_path in loose_images:
        new_path = move_image(img_path)
        image_names_moved.append(new_path.name)

    update_html_files(image_names_moved)
    print("\nmove_images complete!")


if __name__ == "__main__":
    main()