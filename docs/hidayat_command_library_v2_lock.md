# Hidayat Video Command Library v2 — Master Lock

**Status:** LOCKED / SAVE POINT  
**Version:** v2  
**Total unique commands:** 173 / 173  
**Bonus lighting presets:** 4 (not counted)  
**v2 additions:** 75  
**Base v1:** 98  

## Locked schema

Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

- Production prompt language: English
- Purpose language: Urdu
- Shot duration: 8 seconds
- Transition duration: 1–4 seconds
- Shot placeholders: `[SUBJECT]`, `[SCENE]`
- Transition placeholders: `[SCENE_A]`, `[SCENE_B]`, `[SUBJECT_A]`, `[SUBJECT_B]`, `[DETAIL_A]`

## Final category totals

| Category | v1 | v2 Add | Total |
|---|---:|---:|---:|
| Vehicles | 10 | +10 | 20 |
| Sports & Fitness | 10 | 0 | 10 |
| Fashion & Music | 6 | 0 | 6 |
| Film & Characters | 14 | 0 | 14 |
| Views & Environment | 10 | +10 | 20 |
| Camera Movement | 30 | +12 | 42 |
| Weather, Lighting & Effects | 18 | +6 | 24 |
| NEW Transitions | 0 | +8 | 8 |
| NEW People & Motion | 0 | +9 | 9 |
| NEW Time & Atmosphere | 0 | +7 | 7 |
| NEW Product & Commercial | 0 | +6 | 6 |
| NEW Social Media | 0 | +7 | 7 |
| **TOTAL** | **98** | **+75** | **173** |

## Verified and approved v2 batches

### Nature & Environment — Batch 5 — 10
`/ocean`, `/waterfall`, `/mountain`, `/desert`, `/forest`, `/beach`, `/cityscape`, `/countryside`, `/underwater`, `/cloudscape`

### People & Character Motion — Batch 6 — 9
`/walkcycle`, `/turnaround`, `/headturn`, `/lookback`, `/hairflip`, `/gesture`, `/dance`, `/posechange`, `/expressionchange`

### Product & Commercial — 6
`/productmacro`, `/floatingproduct`, `/luxurycommercial`, `/adcinematic`, `/beforeafter`, `/unboxing`

### Social Media — 7
`/shorts`, `/reels`, `/tiktok`, `/loop`, `/satisfying`, `/trendstyle`, `/thumbnailshot`

## Safety lock

- People & Motion: no identity morphing; no distorted anatomy.
- Product & Commercial: no brand logos; no trademarked elements.
- Vehicles: no brand badges/logos.
- Transitions: seam-specific negatives such as no visible cut, no exposure jump, no morphing artifacts.
- Human approval remains required.
- YouTube publishing remains OFF.

## Current export rule

The final `hidayat_command_library_v2.md` and `hidayat_command_library_v2.json` must contain the exact 98-command v1 source plus the locked 75-command v2 additions.

**Do not invent or reconstruct missing v1/v2 production prompts from totals or command names.**

## Recovery note

The current repository tree did not expose a canonical v1 98-command source. GitHub code/commit searches performed on 2026-10-01 did not recover the canonical library. Therefore this lock preserves all verified project state without fabricating the missing source.

## Required final export

1. `hidayat_command_library_v2.md`
2. `hidayat_command_library_v2.json`
3. Updated stats block
4. Updated schema block
5. Safety block
6. Version history (v1 → v2)
7. Uniqueness / placeholder / schema audit

This file is the master save-point until the exact canonical source is recovered.
