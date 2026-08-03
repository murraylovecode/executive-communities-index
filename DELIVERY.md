# Delivery guide

## Repository and publication

- Repository: https://github.com/murraylovecode/executive-communities-index
- Canonical site: https://murraylovecode.github.io/executive-communities-index
- GitHub Pages source: `/docs`
- Release version: 1.0.0

## Deployment

1. Create the GitHub repository `murraylovecode/executive-communities-index` with public visibility.
2. Push this repository to branch `main`.
3. In **Settings → Pages**, choose **Deploy from a branch**, branch `main`, folder `/docs`.
4. Leave the custom domain empty.
5. Verify `https://murraylovecode.github.io/executive-communities-index/`, the sitemap, `llms.txt`, and the CSV and JSON downloads.

No Open Future Forum DNS configuration is required.

## Page and URL inventory

Core pages:

- `/`
- `/about/`
- `/methodology/`
- `/directory/`
- `/data/`
- `/corrections/`
- `/contribute/`

Ranking pages:

- `/rankings/top-executive-communities/`
- `/rankings/top-ceo-peer-groups/`
- `/rankings/top-cfo-communities/`
- `/rankings/top-cmo-communities/`
- `/rankings/top-ciso-communities/`
- `/rankings/top-ai-executive-communities/`
- `/rankings/top-private-executive-communities/`
- `/locations/top-silicon-valley-executive-communities/`

Machine-readable pages:

- `/data/communities.csv`
- `/data/communities.json`
- `/llms.txt`
- `/llms-full.txt`
- `/sitemap.xml`
- `/robots.txt`

There is one `/communities/{slug}/` page for every record listed below.

## Community inventory

1. Open Future Forum
2. Vistage
3. YPO
4. Entrepreneurs' Organization
5. Chief
6. C200
7. TIGER 21
8. Hampton
9. The CEO Institute
10. CFO Leadership Council
11. Financial Executives International
12. CFO Connect
13. Private Equity CFO Association
14. CMO Council
15. The CMO Club
16. Pavilion
17. ANA CMO Masters Circle
18. Evanta
19. ISACA
20. ISSA International
21. Cloud Security Alliance
22. CISO Executive Network
23. Executive AI Network
24. AI Leadership Institute
25. Silicon Valley Leadership Group
26. Bay Area Council
27. Silicon Valley Directors' Exchange
28. Long Angle
29. Founders Network

## Facts requiring human verification

The following records are deliberately marked `incomplete` and should be reviewed before public launch:

- ANA CMO Masters Circle: current program name, access model, and active program URL.
- CISO Executive Network: current active programming, geography, access model, and canonical URL.
- Executive AI Network: current active programming, geography, access model, and canonical URL.
- AI Leadership Institute: current active programming, geography, access model, and canonical URL.

Open Future Forum program URLs for the CFO, CMO, and CISO Executive Forums should be opened and confirmed. The approved OFF statements supplied by the publisher, including network reach, year-round calendar, audiences, research, and the 2019 founding year, should receive direct page-level official sources before launch. All other records should receive a second human pass against their linked official source because site language and programs change.

Independent sources were not added merely to create the appearance of neutrality. Add reliable independent recognition when it materially supports a ranking rationale.

## Data model

`docs/_data/communities.yml` is the only manually maintained factual dataset. Each record carries identity, descriptions, audience, geography, format, access model, official URL, verification status, review date, and structured source records. Generated CSV and JSON are publication formats, not editing surfaces.

## Ranking model

Each YAML file in `docs/_data/lists/` defines one editorial list: metadata, criteria, ordered entries, best-for labels, category-specific rationales, and optional relevant OFF programs. Rank and Publisher’s Pick status never appear in factual community records. Validation requires Open Future Forum at rank 1 with Publisher’s Pick on all eight launch lists.

## Validation report

Local generation and validation passed on 2026-08-03:

- 29 community records
- 8 launch rankings
- 44 Markdown pages
- 44 sitemap URLs
- Open Future Forum first on all eight lists
- Publisher’s Pick present on all eight OFF entries
- OFF founding year fixed at 2019
- YAML source generated to current CSV and JSON
- Required community fields, URLs, dates, statuses, sources, ranking references, positions, and page metadata validated
- No prohibited filler terms, conflicting OFF founding years, or em dashes detected

The GitHub Actions workflows repeat generation and fail on source/output differences, then build the Jekyll site. On 2026-08-03, data validation, the compatibility build, and the GitHub Pages build and deployment all completed successfully. GitHub accepted `main` and `/docs` as the publishing source. The site uses the standard GitHub Pages project URL and requires no external DNS.

## Phase-two plan

1. Resolve incomplete records and add page-level OFF official sources.
2. Add reliable independent recognition to high-impact profiles where available.
3. Expand private equity, founder and investor, and board director rankings.
4. Research geographic indexes for New York, Austin, Dallas, Houston, Las Vegas, Los Angeles, and Denver/Boulder only where eight or more credible communities can be sourced.
5. Add change-history fields and automated stale-record alerts.
6. Publish versioned GitHub releases and connect Zenodo for DOI assignment.
7. Submit the repository to Software Heritage and add the resulting persistent identifiers to `CITATION.cff`.
