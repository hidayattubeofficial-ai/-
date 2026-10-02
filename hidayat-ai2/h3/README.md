# MiniMax H3 — Optional Media Backend

MiniMax H3 is kept as an **optional media-generation backend** for Hidayat AI 2. It is not the local Ollama runtime.

## Boundary

- Hidayat AI 2 reasoning/runtime: local Ollama at `http://127.0.0.1:11434`
- FM Computer API: `http://127.0.0.1:8080`
- MiniMax H3: optional audio-video generation backend
- YouTube auto-publish: OFF
- Human approval: REQUIRED

## Why it is separate

The official MiniMax H3 release is a large multimodal video/audio model. Its official local deployment guidance uses H3-Base checkpoints with SGLang, vLLM, or Diffusers; the published repository documents multi-GPU deployment. Therefore H3 is **not** added to the Ollama dependency path and is not installed into the normal Hidayat AI 2 runtime.

H3 can generate 4–15 second audio-video clips, including text-to-audio-video and reference-based workflows, with outputs up to 2K through the broader H3 workflow.

## Hidayat integration flow

```
Hidayat AI 2
    |
    +--> Ollama (local reasoning / orchestration)
    |
    +--> H3 adapter (optional media generation)
              |
              +--> human review
              |
              +--> approved artifact
```

No automatic YouTube publishing is introduced by this boundary.

## Official resources

- GitHub: https://github.com/MiniMax-AI/MiniMax-H3
- Hugging Face: https://huggingface.co/MiniMaxAI/MiniMax-H3
- Official MiniMax H3 information: https://www.minimax.io/news/minimax-h3-open-source

## Next implementation boundary

When a local H3 machine is available, add a small adapter under this directory rather than changing the core Ollama runtime. The adapter should:
1. accept a validated Hidayat video prompt;
2. call the selected H3 backend;
3. save the generated media as a review artifact;
4. record metadata/hash in the local audit trail;
5. require explicit human approval before any publication workflow.

Do not download the ~500 GB public model repository or add H3 to the default CI/build path merely to enable this boundary.
