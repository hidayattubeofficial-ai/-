"""Hidayat AI 2 local ScrapeGraphAI adapter using Ollama only."""
import argparse
import json
import os
from urllib.parse import urlparse

from scrapegraphai.graphs import SmartScraperGraph

DEFAULT_MODEL = os.getenv("SCRAPEGRAPH_MODEL", "ollama/llama3.2")
DEFAULT_OLLAMA = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")


def validate_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("Invalid source URL: use http:// or https://")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structured data locally with ScrapeGraphAI + Ollama.")
    parser.add_argument("url", help="Source webpage URL")
    parser.add_argument("prompt", help="Natural-language extraction request")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--ollama", default=DEFAULT_OLLAMA)
    args = parser.parse_args()

    source = validate_url(args.url)
    config = {
        "llm": {
            "model": args.model,
            "base_url": args.ollama,
            "temperature": 0,
            "format": "json",
        },
        "verbose": False,
        "headless": True,
    }
    graph = SmartScraperGraph(prompt=args.prompt, source=source, config=config)
    result = graph.run()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
