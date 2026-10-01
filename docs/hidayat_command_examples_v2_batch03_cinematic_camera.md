# Hidayat Video Command Library v2 — Batch 03: Cinematic Camera

## Status
LOCKED v2 category — 12 commands

## Canonical schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /dollyzoom
**Purpose:** perspective distortion کے ذریعے dramatic cinematic tension پیدا کرنا۔
**Prompt:** Create an 8-second cinematic dolly-zoom shot of [SUBJECT] in [SCENE], smoothly moving the camera while compensating the lens zoom so the subject remains framed and the background perspective visibly shifts.
**Camera:** Controlled dolly movement synchronized with inverse lens zoom.
**Motion:** Smooth forward or backward camera travel with matched zoom.
**Lighting:** Preserve stable exposure and realistic depth cues.
**Avoid:** No subject scaling artifacts, no background warping beyond natural perspective, no flicker.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 2. /rackfocus
**Purpose:** foreground اور background subjects کے درمیان cinematic focus transition بنانا۔
**Prompt:** Create an 8-second cinematic rack-focus shot in [SCENE], beginning sharply focused on [SUBJECT] and smoothly shifting focus to a secondary visual element while preserving realistic depth of field.
**Camera:** Locked or gently stabilized medium close-up.
**Motion:** Minimal camera movement; focus pull is the primary motion.
**Lighting:** Soft controlled highlights with natural lens response.
**Avoid:** No focus pulsing, no duplicated subjects, no artificial blur halos.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 3. /anamorphic
**Purpose:** anamorphic cinematic composition اور lens character حاصل کرنا۔
**Prompt:** Create an 8-second cinematic anamorphic shot of [SUBJECT] in [SCENE], using a wide cinematic composition, subtle lens character, natural depth, and restrained horizontal flare only when motivated by bright light sources.
**Camera:** Wide anamorphic-style lens with controlled composition.
**Motion:** Slow cinematic dolly or lateral movement.
**Lighting:** Directional cinematic lighting with restrained practical highlights.
**Avoid:** No excessive lens flare, no distorted faces, no artificial oval bokeh overuse.
**Format:** 8 seconds, 2.39:1 cinematic frame or 16:9 when requested.

## 4. /parallaxpush
**Purpose:** foreground، subject اور background کے درمیان layered parallax کے ساتھ cinematic push-in بنانا۔
**Prompt:** Create an 8-second cinematic parallax push toward [SUBJECT] in [SCENE], revealing distinct foreground, midground, and background depth layers with smooth perspective separation.
**Camera:** Stabilized forward dolly.
**Motion:** Slow continuous push-in with natural parallax.
**Lighting:** Layered directional light emphasizing depth.
**Avoid:** No flat-plane movement, no warped architecture, no subject deformation.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 5. /craneup
**Purpose:** crane movement کے ذریعے shot کو زمین سے بلند cinematic perspective تک لے جانا۔
**Prompt:** Create an 8-second cinematic crane-up shot of [SUBJECT] in [SCENE], starting at a grounded perspective and smoothly rising to reveal the surrounding environment while maintaining coherent spatial scale.
**Camera:** Stabilized vertical crane movement.
**Motion:** Smooth upward rise with slight reveal.
**Lighting:** Consistent environmental light and natural shadow progression.
**Avoid:** No teleporting, no sudden altitude changes, no scale distortion.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 6. /cranedown
**Purpose:** بلند perspective سے subject کی طرف controlled cinematic descent کرنا۔
**Prompt:** Create an 8-second cinematic crane-down shot from an elevated view toward [SUBJECT] in [SCENE], gradually revealing detail while preserving realistic spatial relationships.
**Camera:** Stabilized descending crane.
**Motion:** Smooth vertical descent with controlled framing.
**Lighting:** Natural exposure maintained throughout the move.
**Avoid:** No abrupt camera jumps, no geometry warping, no exposure flicker.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 7. /arcshot
**Purpose:** subject کے گرد partial arc movement سے cinematic depth اور dimensionality بڑھانا۔
**Prompt:** Create an 8-second cinematic arc shot around [SUBJECT] in [SCENE], moving smoothly from one three-quarter angle to another while maintaining consistent subject scale and spatial continuity.
**Camera:** Stabilized lateral arc around the subject.
**Motion:** Smooth partial orbit with controlled parallax.
**Lighting:** Maintain motivated key and rim lighting as the camera changes angle.
**Avoid:** No subject morphing, no background tearing, no abrupt perspective shifts.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 8. /dronedive
**Purpose:** aerial camera کو controlled descent میں لا کر dramatic reveal پیدا کرنا۔
**Prompt:** Create an 8-second cinematic drone dive toward [SUBJECT] in [SCENE], descending smoothly from an elevated perspective into a closer composition with realistic scale and motion.
**Camera:** Stabilized aerial camera descending toward the subject.
**Motion:** Controlled diagonal dive with smooth deceleration.
**Lighting:** Natural aerial exposure with coherent shadows.
**Avoid:** No impossible acceleration, no collision, no warped terrain, no duplicated subject.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 9. /dronerise
**Purpose:** subject سے دور اٹھتے ہوئے environment reveal کرنا۔
**Prompt:** Create an 8-second cinematic drone rise from [SUBJECT] in [SCENE], gradually ascending and widening the composition to reveal the surrounding environment with natural scale and perspective.
**Camera:** Stabilized aerial lift.
**Motion:** Smooth vertical rise with gentle pullback.
**Lighting:** Consistent natural light and shadow direction.
**Avoid:** No sudden altitude jump, no terrain warping, no subject duplication.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 10. /lensflare
**Purpose:** motivated lens flare کے ذریعے cinematic highlight اور atmosphere شامل کرنا۔
**Prompt:** Create an 8-second cinematic shot of [SUBJECT] in [SCENE], using a subtle motivated lens flare from a strong light source while preserving realistic exposure, subject detail, and composition.
**Camera:** Stable cinematic framing with gentle movement.
**Motion:** Slow controlled push or lateral drift.
**Lighting:** Strong motivated backlight producing restrained optical flare.
**Avoid:** No oversized artificial flare, no obscured subject, no color contamination, no exposure clipping.
**Format:** 8 seconds, 16:9 or 9:16 as requested.

## 11. /shallowdof
**Purpose:** shallow depth of field سے subject کو cinematic isolation دینا۔
**Prompt:** Create an 8-second cinematic shallow-depth-of-field shot of [SUBJECT] in [SCENE], keeping the main subject sharply defined while the background falls naturally out of focus with realistic lens behavior.
**Camera:** Medium telephoto or portrait-style lens.
**Motion:** Slow controlled push-in or lateral drift.
**Lighting:** Soft directional key with natural background highlights.
**Avoid:** No cutout-like edges, no artificial blur halos, no focus errors on the main subject.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 12. /steadicamreveal
**Purpose:** smooth stabilized walking camera کے ذریعے layered cinematic reveal بنانا۔
**Prompt:** Create an 8-second cinematic Steadicam reveal of [SUBJECT] in [SCENE], moving smoothly from an obscured foreground element into a clear composition while preserving natural human-scale camera motion.
**Camera:** Stabilized Steadicam-style camera at human eye level.
**Motion:** Smooth forward walk with a controlled reveal.
**Lighting:** Motivated scene lighting with stable exposure.
**Avoid:** No robotic motion, no excessive shake, no geometry warping, no abrupt framing changes.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## Batch QA
- 12/12 locked Cinematic Camera commands covered.
- All are 8-second shot commands.
- rackfocus uses the corrected canonical command spelling.
- anamorphic uses the corrected canonical format.
- No new command names introduced.
- Camera behavior remains physically coherent and compatible with the master prompt contract.
