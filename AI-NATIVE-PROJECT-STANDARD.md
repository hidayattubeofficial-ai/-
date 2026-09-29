# AI-Native Project Standard

## Purpose
A reusable, security-first workflow for AI-assisted product design and development.

## Canonical lifecycle
Idea → Prototype → Review → Implement → Automated Checks → Security Check → Human Approval → Production

## Source of truth
- Working product is the implementation source of truth.
- Prototypes are for exploration and feedback.
- Keep a documented design system: typography, spacing, components, responsive rules, accessibility and interaction rules.

## Agent operating rules
1. Read current state before changing anything.
2. Define scope, non-goals and stop conditions.
3. Prefer the smallest reversible change.
4. Keep secrets out of source, logs and frontend bundles.
5. Run tests, build checks and security checks before approval.
6. Use branches/PRs for material changes.
7. Never bypass a human approval gate for high-impact actions.
8. If the same issue survives three focused prompts/attempts, stop and re-isolate the problem or escalate to human review.
9. Record important changes, errors, verification and rollback information.
10. Do not claim success until verification evidence exists.

## High-impact actions
These remain human-approved:
- Production deployment
- Public publishing
- YouTube publishing
- Payments, refunds or order mutations
- Credential/permission changes
- Hosting architecture changes

## Default workflow
READ-ONLY → CURRENT-STATE → SCOPE → DEPENDENCY-CHECK → BLAST-RADIUS → ROOT-CAUSE → MINIMAL-CHANGE → DRY-RUN → IMPLEMENT → TEST → SECURITY-CHECK → REGRESSION-GUARD → HUMAN-APPROVAL → VERIFY → AUDIT-TRAIL → REPORT

## Design workflow
Brief → AI prototype → UX review → implementation → real-product review → polish → accessibility/security → PR → approval

## Rollback
Every material change must identify a rollback path before implementation.

## Reuse
This document is intended to be portable to other repositories/projects. Copy it as the project-level standard, then add project-specific constraints without weakening these controls.
