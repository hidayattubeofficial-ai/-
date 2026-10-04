""""Select the next unused Hidayat Tube content item.

The selector only manages the locked channel theme. It does not create fiqh/fatwa
rulings and it does not publish to YouTube.
"""
from pathlib import Path
import json
import os
import shlex

ROOT = Path(".")
CATALOG = ROOT / "youtube/content/catalog.json"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

requested_category = os.getenv("REQUESTED_CATEGORY", "auto").strip().lower()
requested_topic = os.getenv("REQUESTED_TOPIC", "AUTO").strip()

items = json.loads(CATALOG.read_text(encoding="utf-8"))["items"]

used = set()
for manifest in (ROOT / "youtube/manifests").rglob("*.txt"):
    text = manifest.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if line.startswith("content_id:"):
            used.add(line.split(":", 1)[1].strip())

if requested_category not in {"auto", "neki", "namaz", "quran", "hadith", "naat"}:
    raise SystemExit("Unsupported category")

pool = [x for x in items if requested_category == "auto" or x["category"] == requested_category]
if requested_topic and requested_topic.upper() != "AUTO":
    exact = [x for x in pool if x["topic_ur"] == requested_topic or x["topic_en"] == requested_topic]
    if exact:
        pool = exact

available = [x for x in pool if x["content_id"] not in used]
if not available:
    raise SystemExit(f"No unused content remains for category: {requested_category}")

item = available[0]
env = OUT / "selection.env"
env.write_text(
    f"SELECTED_CATEGORY={shlex.quote(str(item['category']))}\n"
    f"SELECTED_CONTENT_ID={shlex.quote(str(item['content_id']))}\n"
    f"SELECTED_TOPIC_UR={shlex.quote(str(item['topic_ur']))}\n"
    f"SELECTED_TOPIC_EN={shlex.quote(str(item['topic_en']))}\n",
    encoding="utf-8",
)
print(json.dumps(item, ensure_ascii=False, indent=2))
"