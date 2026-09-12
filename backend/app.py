import os
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)
MAX_MESSAGE_LENGTH = 4000


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
