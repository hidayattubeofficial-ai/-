# Hidayat Video Command Library v3 — Expansion Batch

## Status
PRE-LOCK CANDIDATE — not canonical until final aggregate QA.

## Schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /jibshot
**Purpose:** پروفیشنل jib-style vertical camera movement سے cinematic reveal بنانا.
**Prompt:** Create an 8-second cinematic jib shot of [SUBJECT] in [SCENE], using a smooth articulated camera move that rises or lowers while preserving spatial scale.
**Camera:** Jib-mounted stabilized camera with controlled vertical arc.
**Motion:** Smooth combined lift/drop with gentle framing correction.
**Lighting:** Motivated scene lighting with stable exposure.
**Avoid:** No sudden altitude jumps, warped perspective, or subject scale changes.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 2. /dollyin
**Purpose:** smooth forward camera travel سے subject کی cinematic emphasis بڑھانا.
**Prompt:** Create an 8-second cinematic dolly-in toward [SUBJECT] in [SCENE], gradually increasing visual emphasis while preserving natural perspective and depth.
**Camera:** Stabilized forward dolly.
**Motion:** Smooth constant-speed or gently accelerating push-in.
**Lighting:** Consistent exposure and natural depth lighting.
**Avoid:** No digital zoom artifacts, subject deformation, or background warping.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 3. /dollyout
**Purpose:** smooth backward camera travel سے environment reveal کرنا.
**Prompt:** Create an 8-second cinematic dolly-out from [SUBJECT] in [SCENE], gradually revealing surrounding space with coherent perspective and scale.
**Camera:** Stabilized backward dolly.
**Motion:** Smooth pullback with controlled reveal.
**Lighting:** Maintain believable light direction and exposure.
**Avoid:** No teleporting camera, sudden scale changes, or warped environment.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 4. /truckleft
**Purpose:** camera کو subject کے نسبت بائیں جانب smoothly move کرنا.
**Prompt:** Create an 8-second cinematic truck-left shot of [SUBJECT] in [SCENE], maintaining consistent subject framing while the camera travels laterally left.
**Camera:** Stabilized lateral tracking camera.
**Motion:** Smooth leftward camera translation.
**Lighting:** Consistent environmental lighting and parallax.
**Avoid:** No orbiting unless requested, no lateral distortion, no subject duplication.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 5. /truckright
**Purpose:** camera کو subject کے نسبت دائیں جانب smoothly move کرنا.
**Prompt:** Create an 8-second cinematic truck-right shot of [SUBJECT] in [SCENE], maintaining consistent subject framing while the camera travels laterally right.
**Camera:** Stabilized lateral tracking camera.
**Motion:** Smooth rightward camera translation.
**Lighting:** Consistent environmental lighting and parallax.
**Avoid:** No unintended orbit, geometry warping, or framing jumps.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 6. /pedestalup
**Purpose:** camera کو vertical axis پر اوپر اٹھانا.
**Prompt:** Create an 8-second cinematic pedestal-up shot of [SUBJECT] in [SCENE], raising the camera vertically while keeping the composition coherent.
**Camera:** Stabilized vertical camera rig.
**Motion:** Smooth straight upward translation.
**Lighting:** Stable exposure and natural shadow behavior.
**Avoid:** No crane-like wide reveal unless requested, no perspective teleportation.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 7. /pedestaldown
**Purpose:** camera کو vertical axis پر نیچے لانا.
**Prompt:** Create an 8-second cinematic pedestal-down shot of [SUBJECT] in [SCENE], lowering the camera vertically while maintaining consistent framing and scale.
**Camera:** Stabilized vertical camera rig.
**Motion:** Smooth straight downward translation.
**Lighting:** Stable motivated lighting.
**Avoid:** No sudden drops, geometry warping, or scale distortion.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 8. /focuspull
**Purpose:** controlled focus shift سے visual attention منتقل کرنا.
**Prompt:** Create an 8-second cinematic focus-pull shot in [SCENE], smoothly shifting sharp focus from [SUBJECT] to a secondary visual element while preserving realistic depth of field.
**Camera:** Locked or gently stabilized lens.
**Motion:** Primary motion is a controlled focus shift.
**Lighting:** Soft natural highlights with realistic lens response.
**Avoid:** No focus pulsing, artificial halos, or duplicated details.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 9. /firstperson
**Purpose:** subjective first-person perspective میں cinematic movement دکھانا.
**Prompt:** Create an 8-second cinematic first-person shot moving through [SCENE], presenting the environment from a believable human eye-level perspective with coherent motion.
**Camera:** Eye-level stabilized subjective camera.
**Motion:** Natural head-level movement with restrained sway.
**Lighting:** Lighting follows the environment consistently.
**Avoid:** No floating viewpoint, impossible body perspective, or excessive shake.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 10. /macroshot
**Purpose:** generic subject کے انتہائی قریب detailed macro view بنانا.
**Prompt:** Create an 8-second cinematic macro shot of [SUBJECT] in [SCENE], revealing fine surface detail with shallow depth of field and precise controlled movement.
**Camera:** Macro lens on stabilized slider.
**Motion:** Very slow micro-slide or push-in.
**Lighting:** Soft directional light revealing texture without harsh glare.
**Avoid:** No invented micro-text, melted edges, or exaggerated texture.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## QA
- 10/10 candidate commands have complete schema fields.
- Safety constraints included.
- Human approval remains required before publishing.
- This batch does not modify the locked 173-command registry.
