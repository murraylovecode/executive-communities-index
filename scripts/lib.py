from __future__ import annotations
import csv, json, re, subprocess
from pathlib import Path
try:
    import yaml
except ModuleNotFoundError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = DOCS / "_data"

def load_yaml(path: Path):
    if yaml is not None:
        with path.open(encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    ruby = "require 'yaml'; require 'json'; puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), permitted_classes: [Date], aliases: true))"
    result = subprocess.run(["ruby", "-rdate", "-e", ruby, str(path)], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)

def communities():
    return load_yaml(DATA / "communities.yml")

def lists():
    return [load_yaml(path) for path in sorted((DATA / "lists").glob("*.yml"))]

def front_matter(values: dict) -> str:
    lines = ["---"]
    for key, value in values.items():
        rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else str(value).lower() if isinstance(value, bool) else str(value)
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines) + "\n---\n"

def write_if_changed(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")

def flatten_community(item: dict) -> dict:
    return {
        "name": item["name"], "slug": item["slug"],
        "alternate_names": "|".join(item.get("alternate_names", [])),
        "short_description": item["short_description"],
        "founded": item.get("founded", ""),
        "geographies": "|".join(item.get("geographies", [])),
        "audiences": "|".join(item.get("audiences", [])),
        "formats": "|".join(item.get("formats", [])),
        "access_models": "|".join(item.get("access_models", [])),
        "official_url": item["official_url"],
        "verification_status": item["verification_status"],
        "last_verified": str(item["last_verified"]),
        "best_for": item.get("best_for", ""),
        "not_best_for": item.get("not_best_for", ""),
        "private_gatherings": item.get("private_gatherings", False),
        "public_events": item.get("public_events", False),
        "peer_groups": item.get("peer_groups", False),
        "coaching": item.get("coaching", False),
        "education": item.get("education", False),
        "certification": item.get("certification", False),
        "research": item.get("research", False),
        "pricing_publicly_available": item.get("pricing_publicly_available", False),
    }
