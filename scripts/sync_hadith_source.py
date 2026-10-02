#!/usr/bin/env python3
"""Download an official Dawat-e-Islami book PDF and record its checksum.

The downloader discovers the PDF link from the official book page instead of
hard-coding a guessed data URL. It writes only to the local source cache.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BOOK_URL = (
    "https://www.dawateislami.net/bookslibrary/ar/"
    "sahih-al-bukhari-jild-1/page-1"
)


def fetch(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Hidayat-Hadith-Source-Sync/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def discover_pdf(page_url: str, html: bytes) -> str:
    text = html.decode("utf-8", errors="ignore")
    candidates = re.findall(
        r'''(?:href|src)=["']([^"']+\.pdf(?:\?[^"']*)?)["']''',
        text,
        flags=re.IGNORECASE,
    )
    for candidate in candidates:
        url = urllib.parse.urljoin(page_url, candidate)
        if "dawateislami.net" in urllib.parse.urlparse(url).netloc:
            return url
    raise RuntimeError("official PDF link could not be discovered")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_BOOK_URL)
    parser.add_argument("--out", default="library/hadith/sahih-bukhari")
    args = parser.parse_args()

    page = fetch(args.url)
    pdf_url = discover_pdf(args.url, page)
    pdf = fetch(pdf_url)

    if not pdf.startswith(b"%PDF-"):
        raise RuntimeError("discovered source is not a valid PDF")
    if not pdf:
        raise RuntimeError("official PDF download is empty")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pdf_path = out / "sahih-al-bukhari-jild-1.pdf"
    pdf_path.write_bytes(pdf)

    sha256 = hashlib.sha256(pdf).hexdigest()
    manifest = {
        "book": "sahih-bukhari",
        "volume": 1,
        "source_provider": "Dawat-e-Islami / Al Madina Library",
        "source_page": args.url,
        "download_url": pdf_url,
        "sha256": sha256,
        "bytes": len(pdf),
        "verified_at": datetime.now(timezone.utc).isoformat(),
    }
    (out / "source-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"SOURCE_SYNC_OK sha256={sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
