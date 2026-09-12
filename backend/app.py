import os
from collections import defaultdict
from time import monotonic

from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)
MAX_MESSAGE_LENGTH = 4000
WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 20
_hits = defaultdict(list)


def authorized(req):
    expected = os.environ.get("MESSENGER_AUTH_SECRET")
    supplied = req.headers.get("Authorization", "")
    return bool(expected) and supplied == f"Bearer {expected}"


def rate_limited(key):
    now = monotonic()
    recent = [t for t in _hits[key] if now - t < WINDOW_SECONDS]
    _hits[key] = recent
    if len(recent) >= MAX_REQUESTS_PER_WINDOW:
        return True
    recent.append(now)
    return False


def get_client():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return OpenAI(api_key=key)


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "messenger-backend"})


@app.post("/api/chat")
def chat():
    if not authorized(request):
        return jsonify({"error": "unauthorized"}), 401
    client_key = request.headers.get("X-Client-Key", "anonymous")[:128]
    if rate_limited(client_key):
        return jsonify({"error": "rate_limited"}), 429
    body = request.get_json(silent=True) or {}
    message = body.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "message is required"}), 400
    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": "message is too long"}), 413
    try:
        response = get_client().responses.create(
            model=os.environ.get("OPENAI_MODEL", "gpt-5.6-luna"),
            input=message.strip(),
        )
        return jsonify({"response": response.output_text})
    except Exception:
        return jsonify({"error": "backend request failed"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
