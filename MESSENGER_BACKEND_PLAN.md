# Messenger Backend Plan

## Status
The current `messenger.html` is a frontend interface. A secure backend/API bridge is still required for direct model requests.

## Requirements
- Keep API credentials server-side only (GitHub Secrets/environment configuration).
- Never place API keys in HTML, JavaScript, or other frontend source.
- Accept user messages through a controlled backend endpoint.
- Return model responses to the Messenger UI.
- Apply authentication/rate limiting before production exposure.
- Keep public release and YouTube publishing gated by owner approval.

## Current safe bridge
GitHub Issue #2 remains the operational fallback channel until a secure backend is deployed.
