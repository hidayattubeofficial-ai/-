"""Upload output/video.mp4 to the authenticated YouTube channel as PRIVATE."""
import os
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

VIDEO = Path("output/video.mp4")
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main() -> None:
    if not VIDEO.is_file():
        print("No output/video.mp4 found; private upload skipped.")
        return

    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")
    if not all((client_id, client_secret, refresh_token)):
        raise SystemExit(
            "Missing YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, or "
            "YOUTUBE_REFRESH_TOKEN GitHub Actions secret."
        )

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES,
    )

    youtube = build("youtube", "v3", credentials=credentials)
    title = "Daily Islamic Reminder"
    description = "Daily Islamic reminder. Please review references and content before making this video public."

    script = Path("output/script.md")
    if script.is_file():
        lines = script.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].startswith("# "):
            title = lines[0][2:].strip() or title
        description = script.read_text(encoding="utf-8").strip()

    body = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
            "categoryId": "22",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(str(VIDEO), mimetype="video/mp4", resumable=True),
    )
    response = request.execute()
    print(f"Private YouTube upload complete. Video ID: {response['id']}")


if __name__ == "__main__":
    main()
