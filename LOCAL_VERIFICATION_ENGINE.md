# Local Verification Engine

## Purpose

The Local Verification Engine is the first verification boundary for this repository. It catches code, security, policy, test, and build problems before a change is pushed to GitHub.

## Canonical pre-PR flow

```
Local AI/Code Verification
        ↓
Local Security Scan
        ↓
Local Tests
        ↓
Local Policy Check
        ↓
Local Build
        ↓
GREEN gate
        ↓
GitHub PR
        ↓
GitHub lightweight/final CI
        ↓
Human Approval
        ↓
Production / Cloudflare / YouTube actions
```

## Canonical command

The default is intentionally **change-scope only**:

```text
python scripts/local_verify.py
```

Equivalent explicit form:

```text
python scripts/local_verify.py --changed-only
```

This prevents an existing, intentional Cloudflare deployment workflow from being mistaken for a new policy violation.

For a full repository audit:

```text
python scripts/local_verify.py --full
```

Optional modes:

```text
python scripts/local_verify.py --security-only
python scripts/local_verify.py --build
```

`--full` and `--changed-only` are mutually exclusive.

## Policy model

### Hard-fail

The policy gate rejects automatic YouTube publishing markers when they are present in the verification scope, including:

- `upload_private_youtube.py`
- `youtube.videos().insert`

### Informational

Cloudflare deployment configuration is **not itself a policy violation**. The repository may contain an approval-gated deployment workflow.

The verifier reports Cloudflare deployment markers such as `wrangler deploy` or Cloudflare deployment actions as informational only, and it never executes them.

## Safety

- YouTube publishing remains OFF during review.
- No local verification command publishes to YouTube.
- No local verification command deploys to Cloudflare.
- No local verification command pushes Git changes.
- Production actions remain separate approval-gated operations.
- A GREEN result is not a substitute for GitHub CI or human approval.

## Environment portability

The implementation discovers the repository root from the current Git checkout and uses only Python standard-library functionality for the verifier itself.

Missing tools are reported explicitly when a selected test/build command requires them.

## Change-control

Existing GitHub workflows and deployment configuration are not rewritten as part of the verification gate unless explicitly approved.
