import json
from pathlib import Path
from urllib.parse import urlparse

p = Path(__file__).resolve().parent.parent / "data" / "relationships.json"
rows = json.loads(p.read_text(encoding="utf-8"))
required = {"source","relationship","target","status","evidence","research_cutoff"}
for i, r in enumerate(rows, 1):
    missing = required - r.keys()
    if missing:
        raise SystemExit(f"row {i}: missing {sorted(missing)}")
    for k in ("publisher","published_at","url","locator"):
        if not r["evidence"].get(k):
            raise SystemExit(f"row {i}: evidence.{k} is empty")
    u = urlparse(r["evidence"]["url"])
    if u.scheme not in ("http","https") or not u.netloc:
        raise SystemExit(f"row {i}: invalid URL")
print(f"OK: {len(rows)} relationship records validated")
