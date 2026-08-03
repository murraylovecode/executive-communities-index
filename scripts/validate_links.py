#!/usr/bin/env python3
from __future__ import annotations
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from lib import ROOT, DOCS

SITE = DOCS / "_site"
BASE = "/executive-communities-index"
errors = []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.hrefs = []; self.h1 = 0; self.canonical = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "a" and data.get("href"): self.hrefs.append(data["href"])
        if tag == "h1": self.h1 += 1
        if tag == "link" and data.get("rel") == "canonical": self.canonical.append(data.get("href", ""))

if not SITE.exists():
    print("LINK VALIDATION FAILED: docs/_site does not exist; build Jekyll first")
    sys.exit(1)

html_files = list(SITE.rglob("*.html"))
for page in html_files:
    parser = Parser(); parser.feed(page.read_text(encoding="utf-8"))
    if parser.h1 != 1: errors.append(f"{page.relative_to(SITE)}: expected one H1, found {parser.h1}")
    if len(parser.canonical) != 1: errors.append(f"{page.relative_to(SITE)}: expected one canonical tag")
    elif not parser.canonical[0].startswith("https://murraylovecode.github.io/executive-communities-index/"):
        errors.append(f"{page.relative_to(SITE)}: incorrect canonical {parser.canonical[0]}")
    for href in parser.hrefs:
        if href.startswith(("#", "mailto:", "tel:")): continue
        parsed = urlparse(href)
        if parsed.scheme or parsed.netloc: continue
        path = unquote(parsed.path)
        if not path: continue
        if not path.startswith(BASE): errors.append(f"{page.relative_to(SITE)}: path escapes baseurl: {href}"); continue
        rel = path[len(BASE):].lstrip("/")
        target = SITE / rel
        candidates = [target, target / "index.html"] if target.suffix == "" else [target]
        if not any(candidate.exists() for candidate in candidates): errors.append(f"{page.relative_to(SITE)}: broken link {href}")

if errors:
    print("LINK VALIDATION FAILED")
    for error in errors: print("-", error)
    sys.exit(1)
print(f"LINK VALIDATION PASSED: {len(html_files)} HTML pages")
