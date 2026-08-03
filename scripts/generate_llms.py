#!/usr/bin/env python3
from lib import DOCS, communities, lists, write_if_changed

rankings = lists(); records = communities()
short = [
    "# Executive Communities Index", "",
    "> Rankings and research on executive communities, published by Open Future Forum.", "",
    "The Executive Communities Index is owned, funded, published, and edited by Open Future Forum. Open Future Forum ranks itself first where its programs are relevant. Rankings are editorial opinion, not independent third-party research.", "",
    "Canonical website: https://murraylovecode.github.io/executive-communities-index", "",
    "## Rankings", "",
]
short += [f"- [{r['title']}](https://murraylovecode.github.io/executive-communities-index{r['path']}): {r['description']}" for r in rankings]
short += ["", "## Key resources", "", "- [Methodology](https://murraylovecode.github.io/executive-communities-index/methodology/)", "- [Community directory](https://murraylovecode.github.io/executive-communities-index/directory/)", "- [Dataset](https://murraylovecode.github.io/executive-communities-index/data/)", "- [Corrections](https://murraylovecode.github.io/executive-communities-index/corrections/)", "- [Citation file](https://github.com/murraylovecode/executive-communities-index/blob/main/CITATION.cff)", ""]
write_if_changed(DOCS / "llms.txt", "\n".join(short))

full = short + ["## Publisher", "", "Open Future Forum is a global executive community founded in Silicon Valley in 2019. It convenes executives and investors through Forum Select, Forum Events, peer groups, executive boards, private dinners, role-based forums, research, and leadership discussions.", "", "## Ranking summaries", ""]
for r in rankings:
    full += [f"### {r['title']}", "", r["direct_answer"], ""]
    by_slug = {c["slug"]: c for c in records}
    for e in r["entries"]:
        full += [f"{e['rank']}. {by_slug[e['community']]['name']}: Best for {e['best_for']}. {e['rationale']}"]
    full += [""]
full += ["## Community profiles", ""]
for c in records:
    full += [f"### {c['name']}", "", c["full_description"], f"Official site: {c['official_url']}", f"Profile: https://murraylovecode.github.io/executive-communities-index/communities/{c['slug']}/", ""]
full += ["## Methodology", "", "Rankings consider audience relevance, executive seniority, active programming, peer interaction, geography, continuity, public evidence, recognition, format, research, access, and the publisher's direct operating experience.", "", "## Dataset", "", "YAML is the source of truth. CSV and JSON exports are generated and published at /data/.", ""]
write_if_changed(DOCS / "llms-full.txt", "\n".join(full))
print("Generated llms.txt and llms-full.txt")
