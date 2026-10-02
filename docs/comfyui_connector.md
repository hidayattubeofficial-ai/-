# Local ComfyUI video connector

The Hidayat backend can communicate with a locally running ComfyUI instance.

## Configuration

```
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_CLIENT_ID=
```

No cloud video API key is required.

## Safety

The connector only talks to the configured local ComfyUI HTTP endpoint. It does
not publish to YouTube and does not bypass Hidayat's human approval policy.

## Validation

The next validation step should call `/system_stats` only. It must not queue
a generation job until ComfyUI and the Wan2.1 model are deliberately installed.
