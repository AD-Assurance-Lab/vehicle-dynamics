#!/usr/bin/env python3
# Copyright 2026 AD Assurance Lab. Licensed under the Apache License, Version 2.0.
"""Check that every local link and image in the site's HTML files points to a file.

    python3 tools/check_links.py [site_dir]

Run after the PDFs are built, so links to handouts resolve. A link to a page that
is still on the draft branch fails here, which keeps it off the public site.
"""
import html.parser
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.refs.append((self.getpos()[0], value))


def main(root):
    root = Path(root).resolve()
    bad = []
    for page in sorted(root.rglob("*.html")):
        if any(part.startswith(".") or part in ("archive", "quizzes-exams", "practice-problems", "_to_delete")
               for part in page.relative_to(root).parts):
            continue
        p = Links()
        p.feed(page.read_text(encoding="utf-8"))
        for line, ref in p.refs:
            u = urlsplit(ref)
            if u.scheme or u.netloc or ref.startswith(("#", "mailto:", "data:")):
                continue
            target = (page.parent / unquote(u.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                bad.append(f"{page.relative_to(root)}:{line}: {ref}")
    print("\n".join(bad) if bad else "links: all local links resolve")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
