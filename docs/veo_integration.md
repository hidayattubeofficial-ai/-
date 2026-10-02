# Hidayat Tube — Veo 3.1 Integration

Veo is an external video-generation provider; it is not installed locally as an APK. The backend adapter uses Google Vertex AI and the veo-3.1-fast-generate-001 model by default.

## Policy
- Video generation creates a draft asset.
- Human approval remains REQUIRED before publishing.
- YouTube publishing remains OFF.
- Never commit Google credentials or API keys.

## Required runtime configuration
- GOOGLE_CLOUD_PROJECT
- GOOGLE_CLOUD_LOCATION (default us-central1)
- VEO_OUTPUT_GCS_URI
- Google Application Default Credentials supplied by the hosting environment.

## Defaults
- Aspect ratio: 9:16
- Resolution: 1080p
- Model: veo-3.1-fast-generate-001

## References
- https://deepmind.google/models/veo/
- https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/veo/3-1-generate