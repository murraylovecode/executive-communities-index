#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path
from lib import DOCS

SITE = DOCS / "_site"
errors = []; blocks = 0
required_by_layout = {
    "index.html": {"WebSite", "Organization"},
    "data/index.html": {"Dataset", "BreadcrumbList"},
}
if not SITE.exists():
    print("STRUCTURED DATA VALIDATION FAILED: build Jekyll first"); sys.exit(1)
for page in SITE.rglob("*.html"):
    text = page.read_text(encoding="utf-8")
    found_types = set()
    for raw in re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.S):
        blocks += 1
        try: payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            errors.append(f"{page.relative_to(SITE)}: invalid JSON-LD: {exc}"); continue
        items = payload.get("@graph", [payload]) if isinstance(payload, dict) else []
        for item in items:
            if isinstance(item, dict) and item.get("@type"): found_types.add(item["@type"])
        blocked_domain = "communities" + "." + "openfutureforum" + ".com"
        if blocked_domain in raw: errors.append(f"{page.relative_to(SITE)}: custom domain in JSON-LD")
    rel = str(page.relative_to(SITE))
    expected = required_by_layout.get(rel)
    if expected and not expected.issubset(found_types): errors.append(f"{rel}: missing structured types {sorted(expected - found_types)}")
    if "/rankings/" in f"/{rel}" or "/locations/" in f"/{rel}":
        expected = {"Article", "ItemList", "BreadcrumbList"}
        if not expected.issubset(found_types): errors.append(f"{rel}: missing ranking structured types {sorted(expected - found_types)}")
    if rel.startswith("communities/"):
        expected = {"Organization", "BreadcrumbList"}
        if not expected.issubset(found_types): errors.append(f"{rel}: missing profile structured types {sorted(expected - found_types)}")
if errors:
    print("STRUCTURED DATA VALIDATION FAILED")
    for error in errors: print("-", error)
    sys.exit(1)
print(f"STRUCTURED DATA VALIDATION PASSED: {blocks} JSON-LD blocks")
