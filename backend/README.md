# Secure Messenger Backend

This directory is reserved for the production Messenger API bridge.

## Requirements
- Server-side API credentials only.
- Frontend must call a controlled HTTPS endpoint; no API key in browser code.
- Authentication and rate limiting are required before public exposure.
- Validate and limit incoming message size.
- Return model responses without exposing provider credentials.
- Keep public release and YouTube publishing behind owner approval.

## Deployment
Deploy this backend on a server/runtime that supports environment secrets. Do not deploy credentials in repository files.

## Current bridge
Until this backend is deployed, GitHub Issue #2 remains the safe operational Messenger channel.
