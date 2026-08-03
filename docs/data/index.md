---
layout: standard-page
title: Executive Communities Dataset
lead: Download the factual community records behind the index.
description: Machine-readable YAML, CSV, and JSON data for the Executive Communities Index, with licensing and citation details.
permalink: /data/
reviewed: "2026-08-03"
---
{% include disclosure.html %}

## Dataset overview

The Executive Communities Index Dataset is a versioned, openly maintained collection of factual records about executive communities, peer groups, role-based forums, and leadership networks. Open Future Forum publishes the dataset alongside its separate editorial ranking files.

| Field | Value |
|---|---|
| Publisher | Open Future Forum |
| Version | {{ site.data.site.version }} |
| Release date | {{ site.data.site.release_date }} |
| Record count | {{ site.data.communities | size }} |
| Geographic coverage | Global, United States, Silicon Valley, San Francisco Bay Area, Europe, Australia, New Zealand, Canada, and online communities |
| Role coverage | CEOs, CFOs, CMOs, CISOs, founders, investors, board directors, finance leaders, security leaders, marketing leaders, and AI leaders |
| License | Creative Commons Attribution 4.0 for data and editorial records |

## Downloads

- [Source YAML](https://github.com/murraylovecode/executive-communities-index/blob/main/docs/_data/communities.yml)
- [CSV export]({{ site.baseurl }}/data/communities.csv)
- [JSON export]({{ site.baseurl }}/data/communities.json)

YAML is the only manually maintained factual source. CSV and JSON are generated automatically, and validation fails when the exports are stale. Editorial ranking records are maintained separately in `docs/_data/lists/`.

## Fields and methodology

Records include organization names and aliases, descriptions, verified founding details when available, geography, audience, formats, access models, official URLs, verification status, review dates, reviewers, and structured sources. Ranking position and Publisher’s Pick status are deliberately excluded from factual records. See the [complete ranking and source methodology]({{ site.baseurl }}/methodology/).

## Citation, corrections, and versions

Cite the project as “Executive Communities Index, Open Future Forum, version {{ site.data.site.version }} ({{ site.data.site.release_date }}).” Full citation metadata is in [CITATION.cff](https://github.com/murraylovecode/executive-communities-index/blob/main/CITATION.cff). Review the [version history](https://github.com/murraylovecode/executive-communities-index/blob/main/CHANGELOG.md) or [report a dataset correction]({{ site.baseurl }}/corrections/).

The dataset and editorial data are licensed under CC BY 4.0. Code is licensed under MIT. Third-party names and trademarks remain the property of their respective owners.

<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Dataset","name":"Executive Communities Index Dataset","version":"{{ site.data.site.version }}","datePublished":"{{ site.data.site.release_date }}","dateModified":"{{ site.data.site.reviewed }}","description":"Structured records of executive communities, audiences, geographies, access models, formats, verification status, and sources.","url":"{{ page.url | absolute_url }}","license":"https://creativecommons.org/licenses/by/4.0/","creator":{"@type":"Organization","name":"Open Future Forum","url":"https://openfutureforum.com"},"distribution":[{"@type":"DataDownload","encodingFormat":"text/csv","contentUrl":"{{ '/data/communities.csv' | absolute_url }}"},{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":"{{ '/data/communities.json' | absolute_url }}"}]},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"{{ '/' | absolute_url }}"},{"@type":"ListItem","position":2,"name":"Dataset","item":"{{ page.url | absolute_url }}"}]}]}</script>
