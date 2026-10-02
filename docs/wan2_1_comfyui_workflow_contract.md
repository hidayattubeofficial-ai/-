# Hidayat local Wan2.1 / ComfyUI workflow contract

This file is a **workflow contract**, not executable workflow JSON. It intentionally
contains no model weights, credentials, cloud endpoints, or generation trigger.

## Target

- Engine: local ComfyUI
- Model family: Wan2.1 text-to-video
- Initial profile: short vertical video, 9:16
- Validation before generation
- Human approval required
- YouTube publishing: OFF

## Required node stages

1. Load the installed Wan2.1 T2V checkpoint.
2. Encode the text prompt with the checkpoint's required text-conditioning path.
3. Create an empty latent/video representation at the selected frame count and resolution.
4. Run Wan2.1 sampling.
5. Decode the generated frames.
6. Assemble/export an MP4.
7. Save output to a local review directory.
8. Stop for human approval; do not publish automatically.

## Safety boundary

The Hidayat connector may submit a workflow only after the local engine has
passed its health check. This contract does not download checkpoints and does
not invoke generation by itself.

## Suggested first validation profile

- Aspect ratio: 9:16
- Low initial resolution suitable for the available local GPU
- Short clip
- One output
- Local review/export only

Exact node names and checkpoint loader parameters must be selected from the
installed Wan2.1 + ComfyUI package/version rather than guessed here.
