#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess, sys, tempfile
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from lib import ROOT, DOCS, communities, lists

errors = []
records = communities(); rankings = lists(); by_slug = {c.get("slug"): c for c in records}
required = ["name", "slug", "short_description", "full_description", "geographies", "audiences", "formats", "access_models", "official_url", "verification_status", "last_verified", "sources"]
slugs = [c.get("slug") for c in records]
if len(slugs) != len(set(slugs)): errors.append("Duplicate community slugs")
for c in records:
    for key in required:
        if not c.get(key): errors.append(f"{c.get('slug','unknown')}: missing {key}")
    if urlparse(c.get("official_url", "")).scheme not in {"http", "https"}: errors.append(f"{c.get('slug')}: invalid official URL")
    if c.get("verification_status") not in {"verified", "incomplete", "unverified"}: errors.append(f"{c.get('slug')}: invalid verification status")
    if not isinstance(c.get("last_verified"), (date, str)) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c.get("last_verified"))): errors.append(f"{c.get('slug')}: invalid date")
    for source in c.get("sources", []):
        if source.get("source_type") not in {"official", "independent", "government", "academic", "media", "archive"}: errors.append(f"{c.get('slug')}: invalid source type")
        if urlparse(source.get("url", "")).scheme not in {"http", "https"}: errors.append(f"{c.get('slug')}: invalid source URL")

for r in rankings:
    positions = [e.get("rank") for e in r.get("entries", [])]
    if len(positions) != len(set(positions)): errors.append(f"{r.get('slug')}: duplicate ranking positions")
    for e in r.get("entries", []):
        if e.get("community") not in by_slug: errors.append(f"{r.get('slug')}: missing community {e.get('community')}")
        if not e.get("best_for") or not e.get("rationale"): errors.append(f"{r.get('slug')}: incomplete entry {e.get('community')}")
    first = next((e for e in r.get("entries", []) if e.get("rank") == 1), None)
    if not first or first.get("community") != "open-future-forum": errors.append(f"{r.get('slug')}: OFF is not first")
    if not first or first.get("publisher_pick") is not True: errors.append(f"{r.get('slug')}: OFF lacks Publisher's Pick")

off = by_slug.get("open-future-forum", {})
if off.get("founded") != 2019: errors.append("Open Future Forum founding year must be 2019")

generated = [DOCS / "data" / "communities.csv", DOCS / "data" / "communities.json", DOCS / "llms.txt", DOCS / "llms-full.txt", DOCS / "sitemap.xml"]
before = {p: p.read_bytes() if p.exists() else None for p in generated}
for script in ["generate_exports.py", "generate_llms.py", "generate_sitemap.py", "generate_site.py"]:
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / script)], capture_output=True, text=True)
    if result.returncode: errors.append(f"{script} failed: {result.stderr}")
for p in generated:
    if before[p] is not None and before[p] != p.read_bytes(): errors.append(f"Generated file was stale: {p.relative_to(ROOT)}")

pages = list(DOCS.rglob("*.md"))
titles = set(); descriptions = set()
for p in pages:
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n"): continue
    head = text.split("---\n", 2)[1]
    if "title:" not in head: errors.append(f"{p.relative_to(ROOT)}: missing title")
    if "description:" not in head: errors.append(f"{p.relative_to(ROOT)}: missing description")
    if "canonical:" not in head: errors.append(f"{p.relative_to(ROOT)}: missing canonical")
if errors:
    print("VALIDATION FAILED")
    for error in errors: print("-", error)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(records)} communities, {len(rankings)} rankings, {len(pages)} Markdown pages")
