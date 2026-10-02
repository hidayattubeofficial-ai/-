# Hidayat Free Local Video Engine

## Decision

The paid Google Veo integration was removed. The project now targets an open-source, local-first video engine.

Primary candidate: **Wan2.1 T2V-1.3B + ComfyUI**.

Why this candidate:
- Open-source model family with text-to-video and image-to-video support.
- The 1.3B text-to-video model is documented at about 8.19 GB VRAM and is intended for consumer-grade GPUs.
- Wan2.1 is integrated into ComfyUI, making it suitable for a visual workflow that Hidayat can call locally.
- No per-video API charge when inference runs on the user's own hardware.

Important: "free" means no model/API generation fee. Local inference still requires compatible hardware, disk space, electricity, and software setup.

## Hidayat policy

- Local-first: YES
- Paid video API: OFF
- Automatic YouTube publishing: OFF
- Human approval: REQUIRED
- Credentials in Git: NEVER
- Cloud generation: NOT REQUIRED

## Target architecture

Hidayat AI → local ComfyUI API → Wan2.1 → generated MP4 → Hidayat review/approval → optional manual export.

The first implementation should use a **validation-only** path before downloading large model weights. Do not start paid cloud generation and do not add large model files to this repository.

## Suggested local profile

- Engine: ComfyUI
- Model: Wan2.1 T2V-1.3B
- Initial output: 480p, short clip
- Vertical Hidayat Shorts: compose/resize to 9:16 after generation
- Later: Wan2.1 I2V for animating approved Hidayat branding images

## Source

Wan2.1 repository: https://github.com/Wan-Video/Wan2.1
