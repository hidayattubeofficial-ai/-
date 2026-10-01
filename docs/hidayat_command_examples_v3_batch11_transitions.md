# Hidayat Video Command Library v3 — Expansion Batch

## Status
PRE-LOCK CANDIDATE — not canonical until final aggregate QA.

## Schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /morphtransition
**Purpose:** non-human scene/object elements کو controlled visual morph کے ذریعے جوڑنا.
**Prompt:** Create a 4-second controlled visual morph transition from [SCENE_A] to [SCENE_B], morphing compatible non-human visual forms while preserving scene continuity.
**Camera:** Stable or matched framing.
**Motion:** Smooth shape transformation between compatible visual elements.
**Lighting:** Consistent exposure through the transformation.
**Avoid:** No human identity morphing, anatomy changes, hard cuts, flicker, or geometry corruption.
**Format:** 4 seconds, 16:9 by default; 9:16 when requested.

## 2. /portaltransition
**Purpose:** portal-like visual passage سے scenes connect کرنا.
**Prompt:** Create a 4-second cinematic portal transition from [SCENE_A] to [SCENE_B], using a motivated portal-like opening that carries the camera naturally into the destination scene.
**Camera:** Forward-moving stabilized camera.
**Motion:** Continuous approach and passage through the portal.
**Lighting:** Portal illumination remains physically motivated and exposure controlled.
**Avoid:** No random portals, exposure flash, hard cut, or subject morphing.
**Format:** 4 seconds, 16:9 by default; 9:16 when requested.

## 3. /flashtransition
**Purpose:** brief controlled flash سے scene change کرنا.
**Prompt:** Create an 1-second controlled flash transition from [SCENE_A] to [SCENE_B], using a motivated burst of light to bridge the scenes.
**Camera:** Stable matched framing.
**Motion:** Minimal movement; flash drives the transition.
**Lighting:** Brief controlled illumination with smooth falloff.
**Avoid:** No harsh clipping, strobe, visible hard cut, or random exposure jump.
**Format:** 1 second, 9:16 by default; 16:9 or 1:1 when requested.

## 4. /speedramp
**Purpose:** generic scene میں controlled speed-ramp camera/action effect بنانا.
**Prompt:** Create an 8-second cinematic speed-ramp shot of [SUBJECT] in [SCENE], moving from controlled slow motion into faster natural action and back with continuous physical timing.
**Camera:** Stabilized tracking or locked camera as appropriate.
**Motion:** Smooth temporal acceleration and deceleration.
**Lighting:** Consistent exposure and motion blur response.
**Avoid:** No teleporting, frozen motion, impossible acceleration, or anatomy deformation.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## QA
- 4/4 candidate commands have complete schema fields.
- Safety constraints included.
- Human approval remains required before publishing.
- This batch does not modify the locked 173-command registry.
