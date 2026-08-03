#!/usr/bin/env python3
from lib import DOCS, communities, lists, write_if_changed

base = "https://communities.openfutureforum.com"
urls = ["/", "/directory/", "/methodology/", "/data/", "/about/", "/corrections/", "/contribute/"]
urls += [r["path"] for r in lists()]
urls += [f"/communities/{c['slug']}/" for c in communities()]
body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
body += [f"  <url><loc>{base}{path}</loc></url>" for path in urls]
body += ["</urlset>", ""]
write_if_changed(DOCS / "sitemap.xml", "\n".join(body))
print(f"Generated sitemap with {len(urls)} URLs")
