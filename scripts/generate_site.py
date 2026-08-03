#!/usr/bin/env python3
from lib import DOCS, communities, lists, front_matter, write_if_changed

for item in communities():
    meta = {
        "layout": "community", "title": item["name"],
        "description": item["short_description"] + ". Verified profile, sources, access model, and ranking appearances.",
        "canonical": f"https://murraylovecode.github.io/executive-communities-index/communities/{item['slug']}/",
        "permalink": f"/communities/{item['slug']}/", "section": "communities",
        "community_slug": item["slug"], "reviewed": str(item["last_verified"]),
    }
    write_if_changed(DOCS / "communities" / f"{item['slug']}.md", front_matter(meta))

for ranking in lists():
    directory = "locations" if ranking["page_type"] == "location-ranking" else "rankings"
    meta = {
        "layout": "ranking", "title": ranking["title"], "description": ranking["description"],
        "canonical": "https://murraylovecode.github.io/executive-communities-index" + ranking["path"],
        "permalink": ranking["path"], "section": directory,
        "list_key": ranking["slug"], "reviewed": str(ranking["reviewed"]),
    }
    write_if_changed(DOCS / directory / f"{ranking['slug']}.md", front_matter(meta))
print("Generated canonical community and ranking pages")
