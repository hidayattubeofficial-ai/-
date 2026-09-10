"""Validate the reviewable Islamic content package before it is archived."""
from pathlib import Path

OUT = Path("output")
SCRIPT = OUT / "script.md"
METADATA = OUT / "metadata.txt"

errors = []

if not SCRIPT.exists():
    errors.append("Missing output/script.md")
if not METADATA.exists():
    errors.append("Missing output/metadata.txt")

if SCRIPT.exists():
    text = SCRIPT.read_text(encoding="utf-8").strip()
    if len(text) < 100:
        errors.append("script.md is unexpectedly short")
    if "نوٹ:" not in text:
        errors.append("Human verification note is missing")

if METADATA.exists():
    metadata = METADATA.read_text(encoding="utf-8")
    if "status: REVIEW_REQUIRED" not in metadata:
        errors.append("Content must remain REVIEW_REQUIRED until human approval")

if errors:
    print("Content validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Content validation passed. Human review is still required before publishing.")
