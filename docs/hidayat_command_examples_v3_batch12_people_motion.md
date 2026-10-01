# Hidayat Video Command Library v3 — Expansion Batch

## Status
PRE-LOCK CANDIDATE — not canonical until final aggregate QA.

## Schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /runsequence
**Purpose:** continuous cinematic running sequence کو نمایاں کرنا.
**Prompt:** Create an 8-second cinematic running sequence of [SUBJECT] through [SCENE], maintaining coherent foot contact, stride rhythm, and spatial progression across the shot.
**Camera:** Stabilized tracking camera.
**Motion:** Continuous forward running with believable acceleration.
**Lighting:** Motivated directional lighting with stable exposure.
**Avoid:** No sliding feet, extra limbs, teleporting, or identity morphing.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 2. /turnaround
**Purpose:** subject کا controlled full turn دکھانا.
**Prompt:** Create an 8-second cinematic turnaround of [SUBJECT] in [SCENE], smoothly rotating the subject through a natural full-body turn while preserving identity, clothing, and proportions.
**Camera:** Medium full-body stabilized framing.
**Motion:** Controlled continuous subject rotation.
**Lighting:** Consistent key and fill throughout the turn.
**Avoid:** No face morphing, costume changes, anatomy distortion, or pose jumps.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 3. /headturn
**Purpose:** natural head turn سے attention shift دکھانا.
**Prompt:** Create an 8-second cinematic head-turn shot of [SUBJECT] in [SCENE], with a natural gradual head movement toward a visual point of attention.
**Camera:** Stable portrait or medium framing.
**Motion:** Subtle controlled head rotation with natural neck mechanics.
**Lighting:** Soft motivated portrait lighting.
**Avoid:** No neck deformation, face morphing, or unnatural eye direction.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 4. /lookback
**Purpose:** walking/moving subject کا پیچھے دیکھنا دکھانا.
**Prompt:** Create an 8-second cinematic look-back shot of [SUBJECT] moving through [SCENE], naturally turning the head and upper body to look behind while maintaining gait and identity.
**Camera:** Tracking three-quarter camera.
**Motion:** Continuous movement with controlled backward glance.
**Lighting:** Consistent environmental lighting.
**Avoid:** No twisted spine, eye-line errors, or identity changes.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 5. /hairflip
**Purpose:** controlled natural hair movement کو cinematic بنانا.
**Prompt:** Create an 8-second cinematic hair-movement shot of [SUBJECT] in [SCENE], using a controlled natural hair flip driven by believable head motion and airflow.
**Camera:** Portrait camera with gentle tracking.
**Motion:** Single coherent hair movement synchronized with head motion.
**Lighting:** Soft directional highlights on hair.
**Avoid:** No extreme hair growth, strand fusion, face distortion, or identity change.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 6. /dance
**Purpose:** natural choreographed dance movement دکھانا.
**Prompt:** Create an 8-second cinematic dance shot of [SUBJECT] in [SCENE], using coherent full-body choreography, balanced footwork, and continuous body mechanics.
**Camera:** Stabilized medium-to-full-body camera.
**Motion:** Rhythmic coordinated dance movement.
**Lighting:** Lighting remains synchronized with the environment.
**Avoid:** No extra limbs, broken joints, sliding feet, or anatomy distortion.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 7. /posechange
**Purpose:** ایک pose سے دوسرے pose میں smooth transition.
**Prompt:** Create an 8-second cinematic pose-change shot of [SUBJECT] in [SCENE], transitioning smoothly between two natural poses while preserving identity, clothing, and body proportions.
**Camera:** Stable medium or full-body framing.
**Motion:** Continuous controlled pose transition.
**Lighting:** Consistent portrait or scene lighting.
**Avoid:** No teleporting limbs, clothing morphing, or anatomy distortion.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 8. /expressionchange
**Purpose:** facial expression میں gradual natural change دکھانا.
**Prompt:** Create an 8-second cinematic expression-change shot of [SUBJECT] in [SCENE], gradually shifting between natural facial expressions while preserving identity and facial structure.
**Camera:** Stable close-up portrait camera.
**Motion:** Subtle facial muscle and eye movement.
**Lighting:** Soft consistent facial lighting.
**Avoid:** No face morphing, identity change, or exaggerated deformation.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## QA
- 8/8 candidate commands have complete schema fields.
- Safety constraints included.
- Human approval remains required before publishing.
- This batch does not modify the locked 173-command registry.
