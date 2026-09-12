# Secure Messenger Backend Deployment

## Recommended runtime
Use a managed HTTPS server/runtime that supports environment secrets and server-side environment variables.

## Required environment
- `OPENAI_API_KEY`: provider credential, configured only in the hosting platform's secret manager.
- `MESSENGER_AUTH_SECRET`: application authentication secret, configured only in the hosting platform's secret manager.

## Production checks
1. HTTPS only.
2. Authentication enabled.
3. Rate limiting enabled.
4. Request/message size limits enabled.
5. CORS restricted to the Messenger site's approved origin.
6. Provider credentials never returned to clients or logged.
7. Health endpoint exposes status only, never secrets.
8. Deployment remains separate from YouTube publishing.

## Deployment gate
This repository contains configuration/documentation only. Do not place real secrets in repository files, and do not expose the endpoint publicly until authentication and hosting configuration have been verified.