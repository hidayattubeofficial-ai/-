"""Prepare a safe, reviewable content package for the Islamic YouTube workflow."""
from pathlib import Path
from datetime import datetime, timezone

OUT = Path("output")
OUT.mkdir(exist_ok=True)

TOPIC = "Daily Islamic Reminder"

SCRIPT = f"""# {TOPIC}\n\nالسلام علیکم ورحمۃ اللہ وبرکاتہ۔\n\nآج کا مختصر اسلامی پیغام: نیکی کے چھوٹے کاموں کو معمولی نہ سمجھیں۔ اخلاص کے ساتھ کیا گیا اچھا عمل انسان کی زندگی میں برکت کا ذریعہ بن سکتا ہے۔\n\nاپنے دن میں ایک نیکی کا انتخاب کریں، اسے اخلاص کے ساتھ کریں، اور دوسروں کے لیے بھی آسانی پیدا کریں۔\n\nنوٹ: اشاعت سے پہلے قرآن و حدیث کے اصل حوالہ جات مستند ذریعے سے انسانی طور پر verify کیے جائیں۔\n"""

metadata = f"""topic: {TOPIC}\ncreated_utc: {datetime.now(timezone.utc).isoformat()}\nstatus: REVIEW_REQUIRED\n"""

(OUT / "script.md").write_text(SCRIPT, encoding="utf-8")
(OUT / "metadata.txt").write_text(metadata, encoding="utf-8")
print("Content package prepared. Human review is required before publishing.")
