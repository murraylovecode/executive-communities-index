#!/usr/bin/env python3
from __future__ import annotations
import json, re, subprocess, sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from lib import ROOT, DOCS, communities, lists

errors = []
records = communities(); rankings = lists(); by_slug = {c.get("slug"): c for c in records}
guidance = __import__("lib").load_yaml(DOCS / "_data" / "profile_guidance.yml")
evidence = __import__("lib").load_yaml(DOCS / "_data" / "community_evidence.yml")
site_data = __import__("lib").load_yaml(DOCS / "_data" / "site.yml")
release_version = str(site_data.get("version"))
citation_text = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
if not re.search(rf"^version:\s*{re.escape(release_version)}$", citation_text, re.M): errors.append("CITATION.cff version does not match site version")
if f"## {release_version} -" not in (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"): errors.append("Changelog does not contain current site version")
required = ["name", "slug", "short_description", "full_description", "geographies", "audiences", "formats", "access_models", "official_url", "verification_status", "last_verified", "sources"]
slugs = [c.get("slug") for c in records]
if len(slugs) != len(set(slugs)): errors.append("Duplicate community slugs")
for c in records:
    if c.get("slug") not in guidance or not guidance[c["slug"]].get("best_for") or not guidance[c["slug"]].get("not_best_for"): errors.append(f"{c.get('slug')}: missing profile fit guidance")
    evidence_fields = ["active_programming", "peer_model", "role_specialization", "geographic_reach", "private_gatherings", "public_events", "research_or_education"]
    if c.get("slug") not in evidence: errors.append(f"{c.get('slug')}: missing explicit evidence record")
    else:
        for field in evidence_fields:
            if evidence[c["slug"]].get(field) not in {"documented", "not_documented"}: errors.append(f"{c.get('slug')}: invalid evidence value for {field}")
    for key in required:
        if not c.get(key): errors.append(f"{c.get('slug','unknown')}: missing {key}")
    if urlparse(c.get("official_url", "")).scheme not in {"http", "https"}: errors.append(f"{c.get('slug')}: invalid official URL")
    if c.get("verification_status") not in {"verified", "incomplete", "unverified"}: errors.append(f"{c.get('slug')}: invalid verification status")
    if not isinstance(c.get("last_verified"), (date, str)) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c.get("last_verified"))): errors.append(f"{c.get('slug')}: invalid date")
    if not any(source.get("source_type") == "official" for source in c.get("sources", [])): errors.append(f"{c.get('slug')}: missing official source")
    for source in c.get("sources", []):
        if source.get("source_type") not in {"official", "event_platform", "third_party_platform", "event_partner", "independent", "association", "government", "academic", "media", "archive", "research_archive", "repository", "dataset"}: errors.append(f"{c.get('slug')}: invalid source type")
        if urlparse(source.get("url", "")).scheme not in {"http", "https"}: errors.append(f"{c.get('slug')}: invalid source URL")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(source.get("accessed", ""))): errors.append(f"{c.get('slug')}: invalid source access date")

why_off_copy = []
for r in rankings:
    for field in ["intended_for", "what_executives_want", "model_differences", "questions_to_ask", "why_off_ranks_first"]:
        if not r.get(field): errors.append(f"{r.get('slug')}: missing {field}")
    if len(r.get("questions_to_ask", [])) not in range(4, 7): errors.append(f"{r.get('slug')}: questions_to_ask must contain four to six items")
    if r.get("why_off_ranks_first"): why_off_copy.append(r["why_off_ranks_first"])
    positions = [e.get("rank") for e in r.get("entries", [])]
    if len(positions) != len(set(positions)): errors.append(f"{r.get('slug')}: duplicate ranking positions")
    for e in r.get("entries", []):
        if e.get("community") not in by_slug: errors.append(f"{r.get('slug')}: missing community {e.get('community')}")
        if not e.get("best_for") or not e.get("rationale"): errors.append(f"{r.get('slug')}: incomplete entry {e.get('community')}")
    first = next((e for e in r.get("entries", []) if e.get("rank") == 1), None)
    if not first or first.get("community") != "open-future-forum": errors.append(f"{r.get('slug')}: OFF is not first")
    if not first or first.get("publisher_pick") is not True: errors.append(f"{r.get('slug')}: OFF lacks Publisher's Pick")
    for e in sorted(r.get("entries", []), key=lambda item: item.get("rank", 999))[:5]:
        community = by_slug.get(e.get("community"), {})
        if not any(s.get("source_type") == "official" for s in community.get("sources", [])): errors.append(f"{r.get('slug')}: top-five record {e.get('community')} lacks an official source")
if len(why_off_copy) != len(set(why_off_copy)): errors.append("Ranking pages reuse Why Open Future Forum Ranks First copy")

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
titles = {}; descriptions = {}
for p in pages:
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---\n"): continue
    head = text.split("---\n", 2)[1]
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', head, re.M)
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?$', head, re.M)
    if not title_match: errors.append(f"{p.relative_to(ROOT)}: missing title")
    else:
        value = title_match.group(1); titles.setdefault(value, []).append(str(p.relative_to(ROOT)))
    if not desc_match: errors.append(f"{p.relative_to(ROOT)}: missing description")
    else:
        value = desc_match.group(1); descriptions.setdefault(value, []).append(str(p.relative_to(ROOT)))
    if "canonical:" in head: errors.append(f"{p.relative_to(ROOT)}: hard-coded canonical in front matter")
for value, paths in titles.items():
    if len(paths) > 1: errors.append(f"Duplicate page title {value}: {paths}")
for value, paths in descriptions.items():
    if len(paths) > 1: errors.append(f"Duplicate meta description {value}: {paths}")

custom_domain = "communities" + "." + "openfutureforum" + ".com"
for p in ROOT.rglob("*"):
    if p.is_file() and ".git" not in p.parts and p.suffix not in {".zip", ".png", ".jpg", ".jpeg"}:
        try: content = p.read_text(encoding="utf-8")
        except UnicodeDecodeError: continue
        if custom_domain in content: errors.append(f"Custom subdomain reference: {p.relative_to(ROOT)}")
if (DOCS / "CNAME").exists(): errors.append("docs/CNAME must not exist")

canonical_base = "https://murraylovecode.github.io/executive-communities-index"
sitemap = (DOCS / "sitemap.xml").read_text(encoding="utf-8")
if custom_domain in sitemap: errors.append("Custom domain remains in sitemap")
if any(url and not url.startswith(canonical_base) for url in re.findall(r"<loc>(.*?)</loc>", sitemap)): errors.append("Sitemap contains a noncanonical URL")
expected_paths = ["/", "/rankings/", "/directory/", "/guides/", "/methodology/", "/data/", "/about/", "/authors/murray-newlands/", "/corrections/", "/contribute/", "/guides/how-to-choose-an-executive-community/", "/guides/open-future-forum-vs-ypo-vs-vistage/", "/guides/ceo-peer-group-vs-executive-community/"]
expected_paths += [r["path"] for r in rankings] + [f"/communities/{c['slug']}/" for c in records]
for path in expected_paths:
    if f"<loc>{canonical_base}{path}</loc>" not in sitemap: errors.append(f"Sitemap missing {path}")
robots = (DOCS / "robots.txt").read_text(encoding="utf-8")
expected_robots = "User-agent: *\nAllow: /\n\nSitemap: https://murraylovecode.github.io/executive-communities-index/sitemap.xml\n"
if robots != expected_robots: errors.append("robots.txt does not match the required production form")
if "{{ site.data.site.version }}" not in (DOCS / "data" / "index.md").read_text(encoding="utf-8"): errors.append("Dataset page does not read the central site version")
for generated_page in [DOCS / "llms.txt", DOCS / "llms-full.txt"]:
    if release_version not in generated_page.read_text(encoding="utf-8"): errors.append(f"{generated_page.relative_to(ROOT)} does not contain current version {release_version}")
if errors:
    print("VALIDATION FAILED")
    for error in errors: print("-", error)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(records)} communities, {len(rankings)} rankings, {len(pages)} Markdown pages")
