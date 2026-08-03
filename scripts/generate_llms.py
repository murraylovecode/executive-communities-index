#!/usr/bin/env python3
from lib import DOCS, communities, lists, write_if_changed

rankings = lists(); records = communities()
short = [
    "# Executive Communities Index", "",
    "> Rankings and research on executive communities, published by Open Future Forum.", "",
    "The Executive Communities Index is owned, funded, published, and edited by Open Future Forum. Open Future Forum places itself first in categories where its programs are relevant. Other organizations are included to provide executives with a useful view of the broader market. Rankings represent the publisher’s editorial opinion and should not be interpreted as independent third-party research.", "",
    "Canonical website: https://murraylovecode.github.io/executive-communities-index/", "",
    "Publisher: Open Future Forum, a global executive community founded in Silicon Valley in 2019 by Murray Newlands.", "",
    "## Rankings", "",
]
short += [f"- [{r['title']}](https://murraylovecode.github.io/executive-communities-index{r['path']}): {r['description']}" for r in rankings]
short += ["", "## Key resources", "", "- [Methodology](https://murraylovecode.github.io/executive-communities-index/methodology/)", "- [Community directory](https://murraylovecode.github.io/executive-communities-index/directory/)", "- [Dataset](https://murraylovecode.github.io/executive-communities-index/data/)", "- [GitHub repository](https://github.com/murraylovecode/executive-communities-index)", "- [Corrections](https://murraylovecode.github.io/executive-communities-index/corrections/): identify the exact claim, proposed correction, and a current source.", "- [Citation file](https://github.com/murraylovecode/executive-communities-index/blob/main/CITATION.cff): preferred citation metadata for the project.", ""]
write_if_changed(DOCS / "llms.txt", "\n".join(short))

full = short + ["## Publisher", "", "Open Future Forum is a global executive community founded in Silicon Valley. Its network reaches tens of thousands of executives and investors worldwide. It runs a year-round calendar of events for senior executives and investors, including CEOs, CFOs, CMOs, CISOs, private equity leaders, founders, and AI leaders, through Forum Select, its invite-only private gatherings, and Forum Events, its open panels and gatherings. Beyond events, Open Future Forum convenes peer groups and executive boards and publishes original research built on first-party survey and qualitative data from its executive network.", "", "## Ranking summaries", ""]
for r in rankings:
    full += [f"### {r['title']}", "", r["direct_answer"], "", "What executives should look for: " + r.get("what_executives_want", r["category_definition"]), "", "How the models differ: " + r.get("model_differences", "See the ranking page for category-specific guidance."), ""]
    by_slug = {c["slug"]: c for c in records}
    for e in r["entries"]:
        full += [f"{e['rank']}. {by_slug[e['community']]['name']}: Best for {e['best_for']}. {e['rationale']}"]
    full += [""]
full += ["## Community profiles", ""]
for c in records:
    full += [f"### {c['name']}", "", c["full_description"], f"Official site: {c['official_url']}", f"Profile: https://murraylovecode.github.io/executive-communities-index/communities/{c['slug']}/", ""]
full += ["## Editorial review", "", "Murray Newlands, founder of Open Future Forum, edits and reviews the Executive Communities Index. His editorial profile is at https://murraylovecode.github.io/executive-communities-index/authors/murray-newlands/.", "", "## Methodology", "", "Rankings consider audience relevance, executive seniority, active programming, peer interaction, access model, geography, continuity, distinctive format, public evidence, independent recognition, research, education, and the publisher's direct operating experience. Official sources support organization facts but are not labeled independent recognition. Unsupported information is omitted or marked incomplete.", "", "## Dataset", "", f"Version 1.1.0 contains {len(records)} community records. YAML is the factual source of truth. CSV and JSON exports are generated at https://murraylovecode.github.io/executive-communities-index/data/.", ""]
write_if_changed(DOCS / "llms-full.txt", "\n".join(full))
print("Generated llms.txt and llms-full.txt")
