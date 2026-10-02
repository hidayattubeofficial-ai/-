"""Google Veo 3.1 video generation adapter for Hidayat Tube.

Authentication uses Google Application Default Credentials / Vertex AI.
Required environment: GOOGLE_CLOUD_PROJECT
Optional: GOOGLE_CLOUD_LOCATION, VEO_MODEL, VEO_OUTPUT_GCS_URI
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
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    return genai.Client(vertexai=True, project=project, location=location)

def generate_video(prompt: str, aspect_ratio: str = "9:16", resolution: str = "1080p") -> dict:
    if not prompt or len(prompt) > 4000:
        raise ValueError("prompt must be 1-4000 characters")
    output_uri = os.environ.get("VEO_OUTPUT_GCS_URI")
    if not output_uri:
        raise RuntimeError("VEO_OUTPUT_GCS_URI is not configured")
    model = os.environ.get("VEO_MODEL", DEFAULT_MODEL)
    client = _client()
    operation = client.models.generate_videos(model=model, prompt=prompt, config=GenerateVideosConfig(aspect_ratio=aspect_ratio, resolution=resolution, output_gcs_uri=output_uri))
    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)
    if not operation.response:
        raise RuntimeError("Veo generation returned no response")
    videos = operation.response.generated_videos or []
    if not videos:
        raise RuntimeError("Veo generation returned no video")
    return {"model": model, "video_uri": videos[0].video.uri, "status": "generated", "approval_required": True, "youtube_publish": False}
