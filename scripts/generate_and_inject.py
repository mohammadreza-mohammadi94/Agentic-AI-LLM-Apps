#!/usr/bin/env python3
"""
generate_and_inject.py

Scan a projects/ folder (categories + projects) and inject a generated
Markdown index into README.md between two markers.

Usage:
    python3 generate_and_inject.py                # run with defaults
    python3 generate_and_inject.py --dry-run      # print output, don't write README
    python3 generate_and_inject.py --root myproj  # change projects root
    python3 generate_and_inject.py --readme README.md --start "<!-- START -->" --end "<!-- END -->"
"""
# Libs
from pathlib import Path
from urllib.parse import quote
import argparse
import datetime
import shutil
import sys

MARKER_START_DEFAULT = "<!-- PROJECTS-INDEX-START -->"
MARKER_END_DEFAULT   = "<!-- PROJECTS-INDEX-END -->"

def is_hidden(p: Path):
    return any(part.startswith('.') for part in p.parts)

def escape_md(text: str) -> str:
    # Escape common markdown-significant characters for safe display
    return text.replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('*', '\\*').replace('_', '\\_').replace('`','\\`')

def build_index(root: Path) -> str:
    lines = ["# Project index\n"]
    if not root.exists() or not root.is_dir():
        return "\n".join(lines) + "\n\n*(no projects found)*\n"
    # iterate categories (one level)
    categories = sorted([p for p in root.iterdir() if p.is_dir() and not is_hidden(p)], key=lambda x: x.name.lower())
    for cat in categories:
        lines.append(f"## {escape_md(cat.name)}\n")
        projects = sorted([p for p in cat.iterdir() if p.is_dir() and not is_hidden(p)], key=lambda x: x.name.lower())
        if not projects:
            lines.append("\n")
            continue
        for proj in projects:
            display = escape_md(proj.name)
            # create posix-style encoded relative link: projects/<cat>/<proj>
            encoded_parts = [quote(part) for part in (root.name, cat.name, proj.name)]
            rel = "/".join(encoded_parts)
            # optionally include short desc from README inside project if exists
            short_desc = ""
            readme_f = proj / "README.md"
            if readme_f.exists():
                try:
                    with readme_f.open(encoding="utf8") as fh:
                        for ln in fh:
                            s = ln.strip()
                            if s:
                                short_desc = s
                                break
                except Exception:
                    short_desc = ""
            if short_desc:
                short_desc = " - " + short_desc.replace("\n"," ").strip()[:200]
            lines.append(f"- [{display}]({rel}){short_desc}")
        lines.append("\n")
    return "\n".join(lines)

def inject_into_readme(readme_path: Path, start_marker: str, end_marker: str, content: str, backup: bool = True):
    text = readme_path.read_text(encoding="utf8")
    if start_marker not in text or end_marker not in text:
        raise ValueError(f"Markers not found in {readme_path}. Add {start_marker} and {end_marker} in the README.")
    before, rest = text.split(start_marker, 1)
    _, after = rest.split(end_marker, 1)
    new_text = before + start_marker + "\n\n" + content.strip() + "\n\n" + end_marker + after
    if backup:
        ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        bak = readme_path.with_suffix(readme_path.suffix + f".bak.{ts}")
        shutil.copy2(readme_path, bak)
        print(f"[info] backup created: {bak}")
    readme_path.write_text(new_text, encoding="utf8")
    print(f"[info] README updated: {readme_path}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="projects", help="projects root folder (default: projects)")
    p.add_argument("--readme", default="README.md", help="README file to inject into (default: README.md)")
    p.add_argument("--start", default=MARKER_START_DEFAULT, help="start marker")
    p.add_argument("--end", default=MARKER_END_DEFAULT, help="end marker")
    p.add_argument("--dry-run", action="store_true", help="print generated index but don't write README")
    args = p.parse_args()

    root = Path(args.root)
    readme = Path(args.readme)
    start_marker = args.start
    end_marker = args.end

    index_md = build_index(root)
    if args.dry_run:
        print(index_md)
        return

    if not readme.exists():
        print(f"[error] README file not found: {readme}", file=sys.stderr)
        sys.exit(2)

    try:
        inject_into_readme(readme, start_marker, end_marker, index_md, backup=True)
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(3)

if __name__ == "__main__":
    main()
