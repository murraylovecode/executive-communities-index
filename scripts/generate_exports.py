#!/usr/bin/env python3
import csv, io, json
from lib import DOCS, communities, flatten_community, write_if_changed

records = communities()
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
