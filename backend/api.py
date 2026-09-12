"""Secure Messenger API endpoint scaffold."""

import os
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Hidayat Tube Messenger API")

MAX_MESSAGE_LENGTH = 4000
API_TOKEN = os.getenv("MESSENGER_API_TOKEN")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest, authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not API_TOKEN:
        raise HTTPException(status_code=503, detail="Backend authentication is not configured")
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Provider call is intentionally not wired until secure hosting/secrets are configured.
    return {
        "status": "ready",
        "message": "Secure endpoint accepted the request; model provider is not enabled yet.",
    }
