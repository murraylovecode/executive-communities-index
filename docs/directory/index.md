---
layout: standard-page
title: Executive Community Directory
lead: Canonical profiles of executive communities, CEO peer groups, role-based forums, and leadership networks.
description: Browse verified profiles, sources, audiences, access models, and ranking appearances for executive communities.
canonical: https://communities.openfutureforum.com/directory/
permalink: /directory/
reviewed: 2026-08-03
---
<div class="home-grid">{% assign sorted = site.data.communities | sort: "name" %}{% for community in sorted %}<a class="home-card" href="/communities/{{ community.slug }}/"><span>{{ community.name }}</span><p>{{ community.short_description }}</p><small>{{ community.verification_status }} · reviewed {{ community.last_verified }}</small></a>{% endfor %}</div>
