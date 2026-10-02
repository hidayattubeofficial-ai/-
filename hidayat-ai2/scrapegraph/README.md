# Hidayat AI 2 — ScrapeGraphAI Local Adapter

This adapter adds AI-assisted web extraction without changing the Hidayat AI 2 runtime architecture.

## Locked runtime

- ScrapeGraphAI: isolated optional tool
- LLM: Ollama only
- Ollama endpoint: `http://127.0.0.1:11434`
- No hosted ScrapeGraph API key
- No automatic YouTube publishing
- Human approval remains required

ScrapeGraphAI supports natural-language extraction and local Ollama models through `SmartScraperGraph`. citeturn0search0

## Install

From this directory:

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Ollama must already be running locally and the selected model must be available. The upstream project documents the Ollama integration and local-model workflow. citeturn0search0

## Example

```bash
python scrape_local.py \\
  "https://example.com" \\
  "Extract the page title, main description, and all visible links as JSON"
```

The adapter validates the URL and returns the extraction result as JSON. It does not publish, modify, or upload the scraped content.

## Hidayat use cases

- official-source research and verification
- ecommerce product/catalog extraction
- website content analysis
- research input for Hidayat AI agents

For protected, private, or access-controlled sites, use only authorized access.
