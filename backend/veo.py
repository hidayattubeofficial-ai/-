"""Google Veo 3.1 video generation adapter for Hidayat Tube.

Authentication uses Google Application Default Credentials (ADC) with the
Google Gen AI SDK in Vertex AI enterprise mode.

Required environment:
- GOOGLE_CLOUD_PROJECT
- GOOGLE_CLOUD_LOCATION (defaults to global)
- GOOGLE_GENAI_USE_ENTERPRISE=True
- VEO_OUTPUT_GCS_URI
Optional: VEO_MODEL
"""

import os
import time

from google import genai
from google.genai.types import GenerateVideosConfig

DEFAULT_MODEL = "veo-3.1-fast-generate-001"


def _client():
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise RuntimeError("GOOGLE_CLOUD_PROJECT is not configured")

    # Keep the SDK configuration environment-driven so credentials never
    # enter source control. Google Vertex AI examples use the global location.
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
    os.environ.setdefault("GOOGLE_GENAI_USE_ENTERPRISE", "True")
    return genai.Client()


def generate_video(
    prompt: str,
    aspect_ratio: str = "9:16",
    resolution: str = "1080p",
) -> dict:
    if not prompt or len(prompt) > 4000:
        raise ValueError("prompt must be 1-4000 characters")
    if aspect_ratio not in {"9:16", "16:9"}:
        raise ValueError("aspect_ratio must be 9:16 or 16:9")

    output_uri = os.environ.get("VEO_OUTPUT_GCS_URI")
    if not output_uri:
        raise RuntimeError("VEO_OUTPUT_GCS_URI is not configured")

    model = os.environ.get("VEO_MODEL", DEFAULT_MODEL)
    client = _client()

    operation = client.models.generate_videos(
        model=model,
        prompt=prompt,
        config=GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            output_gcs_uri=output_uri,
        ),
    )

    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)

    if not operation.response:
        raise RuntimeError("Veo generation returned no response")

    videos = operation.response.generated_videos or []
    if not videos:
        raise RuntimeError("Veo generation returned no video")

    return {
        "model": model,
        "video_uri": videos[0].video.uri,
        "status": "generated",
        "approval_required": True,
        "youtube_publish": False,
    }
