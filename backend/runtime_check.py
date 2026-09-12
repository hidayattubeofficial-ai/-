import os

required = ["OPENAI_API_KEY", "MESSENGER_AUTH_SECRET"]
missing = [name for name in required if not os.environ.get(name)]
if missing:
    raise SystemExit("Missing required environment variables: " + ", ".join(missing))

print("Backend configuration check: OK")
