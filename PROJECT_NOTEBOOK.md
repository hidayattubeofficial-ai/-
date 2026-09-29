# Hidayat Tube Official — Project Notebook

**Repository:** `hidayattubeofficial-ai/-`  
**Branch:** `main`  
**Purpose:** One central notebook for the Islamic YouTube automation project.

---

## 1. Future Plan Book

### Content direction
- Quran reminders
- Authentic Hadith with source/reference
- Namaz and Islamic reminders
- Good deeds / daily naseehah
- 30-second YouTube Shorts as the default format
- Cinematic Islamic visuals
- Consistent Hidayat Tube Official branding

### Visual direction
- Include meaningful Islamic B-roll: Quran, tasbeeh, lantern, prayer/mosque imagery where appropriate.
- Keep Urdu text inside the safe area.
- Prefer maximum 2 text lines per scene.
- Avoid text overlap/cropping.
- Keep logo visible but not visually dominant.
- Use different visual concepts across videos rather than repeating one background.

### Publishing rule
- YouTube upload remains **OFF** until human review and final approval.
- Never make a video public automatically.
- Review references, Urdu text, audio, visuals and branding before publishing.

### Next milestones
- [ ] Review latest `islamic-content-review` artifact visually.
- [ ] Confirm logo/branding on final video.
- [ ] Confirm Quran/tasbeeh/lantern/prayer visuals where relevant.
- [ ] Confirm Urdu safe-area and readability.
- [ ] Confirm 30-second voice/content timing.
- [ ] Add final approval checklist.
- [ ] Only after approval, enable YouTube upload deliberately.

---

## 2. Code Book

### Main workflow
`.github/workflows/main.yml`

### Important scripts
- `scripts/prepare_content.py` — prepares the content package.
- `scripts/validate_content.py` — validates the package.
- `scripts/upload_private_youtube.py` — YouTube upload script; currently blocked by workflow gate.

### Core dependencies / tools
- Python
- FFmpeg
- Playwright Chromium
- Noto / Urdu fonts
- GitHub Actions

### Coding rules
1. Keep upload disabled during review.
2. Validate before artifact upload.
3. Do not expose API keys, OAuth tokens, or webhook secrets in code.
4. Prefer environment variables / GitHub Secrets for credentials.
5. Every visual/content change should produce a reviewable artifact.
6. Keep commits small and descriptive.

---

## 3. Hosting Plan — Netlify

- **GitHub Pages:** Cancelled / no longer the hosting plan.
- **Netlify:** Previously selected hosting target; this is superseded by the current Cloudflare setting below.
- GitHub remains the source-code repository and CI/automation system.
- Messenger backend remains a separate secure server-side deployment and must keep credentials server-side.
- Do not place API keys or backend secrets in the frontend.

---

## 4. Daily Report

Use this section once per work session.

### Template
**Date:** YYYY-MM-DD  
**Run(s):** #__  
**Status:** Green / Yellow / Red  

**Completed**
- 

**Changed**
- 

**Artifact**
- 

**Visual review**
- Branding: Pending / Pass / Fix
- Urdu safe area: Pending / Pass / Fix
- Islamic visual elements: Pending / Pass / Fix
- Audio/timing: Pending / Pass / Fix

**Publishing**
- YouTube upload: OFF / ON
- Human approval: Pending / Approved

**Next action**
- 

---

## 5. Error Report

### Template
**Date/time:**  
**Run:** #__  
**Commit:**  
**Component:**  
**Error:**  
**Expected:**  
**Actual:**  
**Likely cause:**  
**Fix applied:**  
**Verification:**  
**Regression risk:** Low / Medium / High  

### Rules
- Record the first real error, not only the final symptom.
- Record the exact run/commit.
- After fixing, rerun validation.
- Never mark an error resolved without verification.

---

## 6. Remaining Work

### Priority 1 — Before publishing
- [ ] Visual inspection of latest artifact.
- [ ] Verify branding/logo.
- [ ] Verify Urdu text safe area.
- [ ] Verify Islamic visual composition.
- [ ] Verify Hadith/Quran references.
- [ ] Verify voice timing.
- [ ] Human approval.

### Priority 2 — Automation improvements
- [ ] Automated daily status report artifact.
- [ ] Automated error summary when a run fails.
- [ ] Keep a changelog of visual/content revisions.
- [ ] Add validation for missing branding assets.
- [ ] Add validation for text overflow/cropping.
- [ ] Add validation that YouTube upload remains disabled in review builds.

### Priority 3 — Optional free services
Use free-tier services only where they genuinely reduce work. Do not add unnecessary external dependencies.

Potential categories:
- GitHub Actions — CI/build/report automation.
- GitHub Issues — error/task tracking.
- GitHub Discussions — longer project notes if enabled.
- GitHub Actions artifacts — review packages.
- Cloudflare — current website hosting/deployment target.
- Generic webhook endpoint — optional notifications, only after a secret-based configuration is chosen.

**Security:** Never commit webhook URLs containing secrets or tokens to this repository.

---

## 7. Webhook / Notification Plan

### Recommended design
`GitHub Actions → notification webhook → phone/chat notification`

Trigger only for:
- workflow failure
- workflow success (optional)
- artifact ready (optional)

### Required secret
Store the webhook URL as a GitHub Actions Secret, for example:
`NOTIFICATION_WEBHOOK_URL`

Never put the actual URL in this notebook or workflow source.

### Safe rollout
1. Choose one notification provider.
2. Create its free-tier webhook.
3. Add the URL to GitHub Secrets.
4. Add a small notification step to the workflow.
5. Test with a controlled event.
6. Keep YouTube publishing independent from notifications.

---

## 8. Free Tools / Applications — Approval List

| Tool/category | Purpose | Status |
|---|---|---|
| GitHub Actions | Build/validate/package automation | Active |
| GitHub Artifacts | Review video/package storage | Active |
| GitHub Issues | Error + remaining-work tracking | Available |
| Canva | Visual/design workflow | Connected/available when needed |
| Cloudflare | Website hosting | Current / active target |
| Webhook notifications | Optional run alerts | Not configured yet |

**Rule:** Do not install or connect a service merely because it is free. Add it only if it solves a real project need and does not weaken security.

---

## 9. Current Verified State

- Latest known run: **#56**
- Run #56: **Success / Green**
- Review artifact: **`islamic-content-review`**
- YouTube upload step: **Skipped intentionally**
- Review gate: **Success**
- Publishing remains blocked until final human approval.

---

## 10. Change Log

| Date | Run | Change | Result |
|---|---:|---|---|
| 2026-09-11 | #55 | Refined branded Short layout | Green |
| 2026-09-11 | #56 | Refined CTA: smaller/lower/less dominant | Green |
| 2026-09-12 | — | Cancelled GitHub Pages hosting plan; selected Netlify | Recorded |
| 2026-09-12 | — | Current hosting setting clarified: Cloudflare is the actual website host; Netlify is not the active hosting target | Recorded |

Add every important future change here.

---

## 11. Current Project Settings — IMPORTANT / OVERRIDES OLDER NOTES

### Public website
- **Actual website hosting target:** Cloudflare.
- Public homepage is `index.html`.
- Public site must show the Hidayat Tube Official experience only.
- Admin controls, GitHub Actions, Project Files, Security panels, backend controls, and internal deployment information must **NOT** appear above or inside the public homepage hero section.
- Login/Register UI belongs to the public site; authentication/backend connection is a separate concern.

### Admin / backend separation
- Admin panel is separate from the public homepage.
- Backend and Messenger are separate from the public homepage.
- Never mix admin/backend controls into the public hero or normal visitor-facing UI.

### Cloudflare deployment state
- Cloudflare currently has a Worker with static assets for `hidayattubeofficial`.
- Current public Worker hostname: `hidayattubeofficial.hidayattubeofficial.workers.dev`.
- No custom domain is currently configured in the verified Cloudflare dashboard state.
- The existing repository workflow was restored to its original Cloudflare Pages workflow after an incorrect temporary Worker/Wrangler change.
- Known deployment failure was **Cloudflare API authentication (HTTP 403)** at the Pages deployment step; the site build/preparation step itself completed successfully.
- Do not claim that the deployment issue is fixed until a successful Cloudflare deployment is verified.

### Change-control rule
- **Do not change GitHub workflow files, deployment configuration, or hosting architecture without explicit user approval.**
- Do not make an unsolicited workflow replacement merely to work around a hosting mismatch.
- Before any future deployment change, first explain the current state and proposed change, then wait for explicit approval.

### Repository safety
- Never expose or copy secret/token values into this notebook.
- GitHub Secrets cannot be read through the available GitHub integration; only configuration references can be documented.
- Keep public-site files, admin files, and backend files logically separated.

### Current rollback setting
- The mistaken temporary `worker.js`, `wrangler.toml`, and Wrangler-based workflow change were removed from `main`.
- The original Cloudflare Pages workflow was restored.
- **Current instruction:** leave the workflow unchanged unless the user explicitly approves a deployment fix.


---

## 12. Prompt Code Master Dictionary — DEDUPLICATED

- Master dictionary file: `PROMPT_CODE_MASTER.md`
- Status: **Saved / deduplicated / active reference**
- Purpose: reusable prompt shorthand for FM AI, development, research, content, business, publishing, QA, security and operations.
- Duplicate/near-duplicate labels are consolidated; combinations are treated as workflows, not separate official commands.
- These are custom/community prompt labels, **not official hidden ChatGPT commands**.
- FM AI should use this file as its prompt/workflow vocabulary reference.
- Safety rule: FM AI must preserve the existing human-approval gate and must not bypass security or approval controls.

### Core FM AI vocabulary
`SOURCE-OF-TRUTH-LOCK` • `CURRENT-STATE` • `READ-ONLY` • `MINIMAL-CHANGE` • `DRY-RUN` • `HUMAN-APPROVAL` • `REGRESSION-GUARD` • `HEALTH-CHECK` • `AUDIT-TRAIL` • `ROLLBACK`

### Master workflows
- Safe technical: READ-ONLY → CURRENT-STATE → BACKUP-FIRST → DEPENDENCY-CHECK → BLAST-RADIUS → ROOT-CAUSE → MINIMAL-CHANGE → DRY-RUN → HUMAN-APPROVAL → IMPLEMENT → TEST → REGRESSION-GUARD → VERIFY → CHANGE-REPORT → ROLLBACK
- FM AI: FM-AUDIT → SOURCE-OF-TRUTH-LOCK → CURRENT-STATE → FM-ROOT-CAUSE → MINIMAL-CHANGE → DRY-RUN → FM-APPROVAL → FM-IMPLEMENT → FM-TEST → SECURITY-CHECK → FM-HEALTH → REGRESSION-GUARD → AUDIT-TRAIL → FM-REPORT
- Agent: MISSION → SCOPE → NON-GOALS → INPUTS → SOURCES → TOOLS → PERMISSIONS → CONSTRAINTS → SUCCESS-CONDITION → STOP-CONDITION → PLAN → HUMAN-IN-LOOP → EXECUTE → VERIFY → AUDIT-TRAIL → REPORT

### Integration status
- `PROMPT_CODE_MASTER.md` has been added to the repository.
- The dictionary is now the canonical project reference for FM AI prompt shorthand.
- Do not create another duplicate master dictionary unless explicitly requested; update this canonical file instead.


## 13. Local Verification Engine — PROJECT STANDARD

- **Architecture:** Local AI/Code Verification → Local Security Scan → Local Tests → Local Policy Check → Local Build → GREEN → GitHub PR → GitHub final CI → Human Approval → production actions.
- Local verification is the first failure boundary; GitHub CI is intentionally lightweight/final verification where practical.
- Local verification must be portable and must not depend on a hard-coded developer OS/repository path.
- Local verification must fail closed for security/policy violations and must never publish to YouTube or deploy to Cloudflare.
- YouTube publishing remains OFF until human approval.
- GitHub workflow/deployment files remain protected by the existing explicit-approval change-control rule.
- Canonical specification: `LOCAL_VERIFICATION_ENGINE.md`.
- **Current status:** Architecture integrated; local machine execution is not claimed from GitHub. The local runner should be executed from the user's checked-out repository.


## 14. Local Verification PR — Current State

- PR: #4 — **Add portable local verification gate**
- Branch: `local-verification-engine`
- Status: **OPEN / DRAFT / NOT MERGED**
- Scope: adds only `scripts/local_verify.py`; existing GitHub workflows and deployment configuration are unchanged.
- Safety: the verifier performs no git push, YouTube upload, or Cloudflare deploy.
- Cloudflare observation: Cloudflare's Git integration attempted a deployment for PR commit `a173087` and reported failure. This is separate from the local verifier and does **not** establish that local verification failed.
- Current action: keep PR #4 isolated and do not merge until local execution is performed on the user's checked-out repository and the deployment behavior is separately understood.
- **Do not modify `.github/workflows/cloudflare-deploy.yml` or hosting architecture without explicit approval.**
