#!/usr/bin/env python3
"""Collect small, license-recorded nature video assets from Wikimedia Commons.

This is the no-key provider. Other free sources are documented in youtube/NATURE_SOURCES.md;
we do not scrape those sites blindly or bypass their access controls."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "youtube/backgrounds/nature")
OUT.mkdir(parents=True, exist_ok=True)
MAX_BYTES = 15 * 1024 * 1024
QUERIES = ["nature mp4", "forest mp4", "rain mp4", "mountain mp4"]

def get_json(url):
    req = Request(url, headers={"User-Agent": "HidayatTubeAssetCollector/1.0"})
    with urlopen(req, timeout=30) as r:
        return json.load(r)

saved = 0
seen = set()
for query in QUERIES:
    params = {"action":"query","generator":"search","gsrsearch":query,"gsrnamespace":"6",
              "gsrlimit":"10","prop":"imageinfo","iiprop":"url|mime|size|extmetadata","format":"json"}
    data = get_json("https://commons.wikimedia.org/w/api.php?" + urlencode(params))
    for page in (data.get("query", {}).get("pages", {}) or {}).values():
        infos = page.get("imageinfo") or []
        if not infos: continue
        info = infos[0]
        url, mime = info.get("url",""), info.get("mime","")
        if "video" not in mime or not url or url in seen: continue
        seen.add(url)
        size = int(info.get("size") or 0)
        if size <= 0 or size > MAX_BYTES: continue
        title = page.get("title","nature").replace("File:","").replace("/","_")
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in title)
        target = OUT / safe
        if target.suffix.lower() not in {".mp4",".webm",".ogv",".mov"}: continue
        if target.exists(): continue
        req = Request(url, headers={"User-Agent":"HidayatTubeAssetCollector/1.0"})
        with urlopen(req, timeout=120) as r, target.open("wb") as f: f.write(r.read())
        meta = {"source":"Wikimedia Commons","source_url":url,"page_title":page.get("title"),
                "downloaded_at":datetime.now(timezone.utc).isoformat(),
                "mime":mime,"size_bytes":size,
                "license_metadata":(info.get("extmetadata") or {}).get("LicenseShortName",{}).get("value"),
                "artist_metadata":(info.get("extmetadata") or {}).get("Artist",{}).get("value")}
        target.with_suffix(target.suffix + ".json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
        saved += 1
        if saved >= 3: break
    if saved >= 3: break

index = OUT / "INDEX.md"
lines = ["# Nature Asset Index", "", "Downloaded assets are accompanied by per-file JSON provenance records.", ""]
for p in sorted(OUT.iterdir()):
    if p.suffix.lower() in {".mp4",".webm",".ogv",".mov"}:
        lines.append(f"- `{p.name}` — see `{p.name}.json` for source and license metadata.")
index.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Nature assets collected: {saved}")
if saved == 0:
    raise SystemExit("No suitable small video asset found; build stopped rather than using an unverified source.")
