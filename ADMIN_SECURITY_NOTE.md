# Admin security boundary

The admin page UI may provide a login gate, but frontend JavaScript cannot securely protect a production password or privileged actions. Production authentication must be enforced by the hosting/backend layer, with credentials stored as protected secrets or environment variables.

Rules:
- Never commit an admin password or API key.
- Keep privileged deployment actions server-side.
- Keep YouTube publishing behind explicit human approval.
- Record important actions in an auditable workflow/report.
