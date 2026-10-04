# Local Verification Engine

## Purpose

The Local Verification Engine is the first verification boundary for this repository. It is designed to catch code, security, policy, test, and build problems before a change is pushed to GitHub.

## Canonical flow

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

## Responsibilities

### Local
- Inspect the current repository state.
- Validate changed files and project structure.
- Run available local tests and static checks.
- Run security checks before push.
- Enforce project policy gates.
- Run the relevant local build.
- Produce a clear GREEN/RED verification report.
- Stop on failure; do not push or publish automatically.

### GitHub
- Treat the PR as the review boundary.
- Run only the final CI/security checks required to verify the submitted change.
- Keep cloud/API-heavy work out of ordinary local-failure retries where practical.
- Preserve human approval before production actions.

## Hard safety gates

The Local Verification Engine must fail closed when:
- required checks cannot be established;
- a policy check detects an attempt to enable automatic YouTube publishing;
- secrets/tokens are introduced into tracked source;
- a required test/build step fails;
- a high-confidence security violation is detected.

A local GREEN result means only that the local verification suite passed. It is not a substitute for GitHub CI or human approval.

## Publishing policy

- YouTube publishing remains OFF during review.
- No local verification command may publish to YouTube.
- No local verification command may deploy to Cloudflare.
- Production actions remain separate approval-gated operations.

## Environment portability

The repository should not hard-code a developer's absolute OS path.

The implementation should discover the repository root from the current Git checkout and support Windows, macOS, and Linux where the required tools are installed.

If a tool is unavailable, the verifier should report the missing dependency explicitly rather than silently skipping a required gate.

## Suggested command

```text
python scripts/local_verify.py
```

Optional future modes may include:

```text
python scripts/local_verify.py --changed-only
python scripts/local_verify.py --security-only
python scripts/local_verify.py --build
```

These modes should only be added when their exact project commands are defined and tested.

## Source of truth

This document defines the verification architecture. The live repository implementation is the operational source of truth.

## Change-control rule

Do not replace or rewrite existing GitHub workflows as part of Local Verification work without explicit approval. The current GitHub workflow and deployment configuration remain protected by the project's change-control rules.
