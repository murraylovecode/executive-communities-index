#!/usr/bin/env python3
import copy, csv, io, json
from lib import DATA, DOCS, communities, flatten_community, load_yaml, write_if_changed

relationship_map = {"official": "official", "event_platform": "third-party-platform", "third_party_platform": "third-party-platform", "independent": "independent-editorial", "media": "independent-editorial", "association": "association", "repository": "research-archive", "archive": "research-archive", "research_archive": "research-archive", "dataset": "research-archive"}
guidance = load_yaml(DATA / "profile_guidance.yml")
records = copy.deepcopy(communities())
for item in records:
    formats = " ".join(item.get("formats", [])).lower()
    access = " ".join(item.get("access_models", [])).lower()
    sources = item.get("sources", [])
    for source in sources:
        relationship = relationship_map.get(source.get("source_type"), source.get("source_type", "third-party-platform").replace("_", "-"))
        if source.get("source_type") == "repository" and source.get("publisher") == "Open Future Forum": relationship = "publisher-controlled"
        source["source_relationship"] = relationship
    item.update({
        "geographic_reach": item.get("geographies", []),
        "primary_roles": item.get("audiences", [])[:2],
        "secondary_roles": item.get("audiences", [])[2:],
        "membership_model": item.get("access_models", []),
        "access_model": item.get("access_models", []),
        "private_gatherings": any(x in formats or x in access for x in ["private", "confidential", "invitation"]),
        "public_events": "events" in formats and "open" in access,
        "peer_groups": any(x in formats for x in ["peer", "forum", "roundtable"]),
        "coaching": "coaching" in formats,
        "education": any(x in formats for x in ["education", "learning", "training"]),
        "certification": any(x in formats for x in ["credential", "certification"]),
        "research": "research" in formats,
        "pricing_publicly_available": False,
        "current_program_evidence": [s["url"] for s in sources if any(x in " ".join(s.get("supports", [])).lower() for x in ["program", "format", "event", "activity"])],
        "best_for": guidance[item["slug"]]["best_for"],
        "not_best_for": guidance[item["slug"]]["not_best_for"],
        "official_sources": [s["url"] for s in sources if s["source_relationship"] == "official"],
        "independent_sources": [s["url"] for s in sources if s["source_relationship"] == "independent-editorial"],
        "partner_sources": [s["url"] for s in sources if s["source_relationship"] == "event-partner"],
        "archive_sources": [s["url"] for s in sources if s["source_relationship"] == "research-archive"],
    })
flat = [flatten_community(item) for item in records]
buffer = io.StringIO()
writer = csv.DictWriter(buffer, fieldnames=list(flat[0]), lineterminator="\n")
writer.writeheader(); writer.writerows(flat)
csv_path = DOCS / "data" / "communities.csv"
csv_text = buffer.getvalue()
if not csv_path.exists() or csv_path.read_bytes() != csv_text.encode("utf-8"):
    csv_path.write_bytes(csv_text.encode("utf-8"))
write_if_changed(DOCS / "data" / "communities.json", json.dumps(records, indent=2, ensure_ascii=False, default=str) + "\n")
print(f"Generated CSV and JSON for {len(records)} communities")
