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

## 3. Daily Report

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

## 4. Error Report

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

## 5. Remaining Work

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
- Generic webhook endpoint — optional notifications, only after a secret-based configuration is chosen.

**Security:** Never commit webhook URLs containing secrets or tokens to this repository.

---

## 6. Webhook / Notification Plan

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

## 7. Free Tools / Applications — Approval List

| Tool/category | Purpose | Status |
|---|---|---|
| GitHub Actions | Build/validate/package automation | Active |
| GitHub Artifacts | Review video/package storage | Active |
| GitHub Issues | Error + remaining-work tracking | Available |
| Canva | Visual/design workflow | Connected/available when needed |
| Webhook notifications | Optional run alerts | Not configured yet |

**Rule:** Do not install or connect a service merely because it is free. Add it only if it solves a real project need and does not weaken security.

---

## 8. Current Verified State

- Latest known run: **#56**
- Run #56: **Success / Green**
- Review artifact: **`islamic-content-review`**
- YouTube upload step: **Skipped intentionally**
- Review gate: **Success**
- Publishing remains blocked until final human approval.

---

## 9. Change Log

| Date | Run | Change | Result |
|---|---:|---|---|
| 2026-09-11 | #55 | Refined branded Short layout | Green |
| 2026-09-11 | #56 | Refined CTA: smaller/lower/less dominant | Green |

Add every important future change here.
