# Hidayat Video Command Library v3 — Expansion Batch

## Status
PRE-LOCK CANDIDATE — not canonical until final aggregate QA.

## Schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /sunrise
**Purpose:** sunrise کے natural warm transition کو cinematic بنانا.
**Prompt:** Create an 8-second cinematic sunrise scene in [SCENE], with gradually warming light, long natural shadows, and a believable horizon glow.
**Camera:** Stable wide or medium camera.
**Motion:** Slow environmental reveal with subtle light progression.
**Lighting:** Natural sunrise illumination.
**Avoid:** No instant sun jumps, clipped highlights, or impossible shadow direction.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 2. /starlight
**Purpose:** star-filled night environment کو cinematic depth دینا.
**Prompt:** Create an 8-second cinematic starlight scene in [SCENE], featuring a clear star-filled sky and restrained low-light environmental detail.
**Camera:** Stable wide camera.
**Motion:** Minimal camera movement with subtle environmental motion.
**Lighting:** Natural low-light illumination with restrained sky glow.
**Avoid:** No excessive stars, artificial constellations, or daytime exposure.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 3. /daytonight
**Purpose:** day scene کو gradual night atmosphere میں منتقل کرنا.
**Prompt:** Create an 8-second cinematic day-to-night transition in [SCENE], gradually shifting daylight into believable twilight and night while preserving scene geometry.
**Camera:** Locked or stabilized matched composition.
**Motion:** Continuous temporal lighting transition.
**Lighting:** Physically plausible decreasing daylight and emerging practical lights.
**Avoid:** No geometry changes, hard exposure jump, or object teleportation.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 4. /nighttoday
**Purpose:** night scene کو gradual daylight میں منتقل کرنا.
**Prompt:** Create an 8-second cinematic night-to-day transition in [SCENE], gradually introducing dawn light while preserving the original environment and spatial continuity.
**Camera:** Locked or stabilized matched composition.
**Motion:** Continuous temporal lighting transition.
**Lighting:** Gradual dawn illumination and natural shadow emergence.
**Avoid:** No sudden sun placement, geometry changes, or exposure jump.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 5. /seasonchange
**Purpose:** ایک ہی environment میں seasonal transformation دکھانا.
**Prompt:** Create an 8-second cinematic seasonal-change sequence in [SCENE], transforming environmental cues such as foliage, snow, or light while preserving the underlying location and composition.
**Camera:** Locked or highly stabilized composition.
**Motion:** Gradual environmental transformation.
**Lighting:** Season-appropriate lighting changes with continuous exposure.
**Avoid:** No building/terrain morphing, random object replacement, or identity changes.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 6. /timewarp
**Purpose:** time progression کو accelerated cinematic effect میں دکھانا.
**Prompt:** Create an 8-second cinematic time-warp sequence of [SCENE], accelerating a coherent environmental progression such as clouds, traffic, shadows, or changing light while preserving spatial continuity.
**Camera:** Locked or stabilized time-lapse composition.
**Motion:** Accelerated temporal motion with coherent trajectories.
**Lighting:** Gradual physically plausible light progression.
**Avoid:** No teleporting objects, discontinuous shadows, or scene redesign.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 7. /carinterior
**Purpose:** گاڑی کے cabin/interior کو cinematic detail میں دکھانا.
**Prompt:** Create an 8-second cinematic car-interior shot of [SUBJECT] in [SCENE], revealing dashboard, controls, seats, and cabin materials with realistic depth and restrained camera movement.
**Camera:** Driver-eye or cabin-level stabilized camera.
**Motion:** Slow interior pan or dolly.
**Lighting:** Natural cabin light with believable reflections.
**Avoid:** No duplicated controls, distorted dashboard, or invented logos.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 8. /wheelshot
**Purpose:** vehicle wheel کی close-up cinematic detail دکھانا.
**Prompt:** Create an 8-second cinematic wheel detail shot of [SUBJECT] in [SCENE], emphasizing realistic wheel rotation, tire contact, surface detail, and road interaction.
**Camera:** Low close tracking camera.
**Motion:** Matched-speed wheel tracking or slow detail reveal.
**Lighting:** Directional highlights with realistic surface reflections.
**Avoid:** No wheel deformation, floating tire, or invented branding.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 9. /enginecloseup
**Purpose:** engine/mechanical detail کا cinematic close-up بنانا.
**Prompt:** Create an 8-second cinematic engine-detail close-up of [SUBJECT] in [SCENE], revealing mechanical components and material detail with realistic depth and controlled movement.
**Camera:** Macro-capable stabilized close camera.
**Motion:** Slow slider or micro push-in.
**Lighting:** Controlled highlights revealing metal and mechanical surfaces.
**Avoid:** No duplicated components, invented labels, or melted geometry.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 10. /exhaustshot
**Purpose:** vehicle exhaust کو cinematic detail کے ساتھ دکھانا.
**Prompt:** Create an 8-second cinematic exhaust detail shot of [SUBJECT] in [SCENE], showing realistic exhaust hardware, heat shimmer, and subtle vapor or emissions only when physically appropriate.
**Camera:** Low rear close-up camera.
**Motion:** Slow tracking or static detail framing.
**Lighting:** Directional highlights with realistic heat response.
**Avoid:** No excessive smoke, distorted exhaust geometry, or invented logos.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 11. /cockpit
**Purpose:** driver cockpit perspective میں cinematic vehicle shot بنانا.
**Prompt:** Create an 8-second cinematic cockpit perspective of [SUBJECT] in [SCENE], showing a believable driver viewpoint, controls, windshield perspective, and road movement.
**Camera:** Driver-eye stabilized camera.
**Motion:** Natural forward vehicle motion with subtle cabin vibration.
**Lighting:** Realistic dashboard and exterior light interaction.
**Avoid:** No duplicated controls, impossible road perspective, or invented labels.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 12. /highwaydrive
**Purpose:** highway پر cinematic driving sequence دکھانا.
**Prompt:** Create an 8-second cinematic highway-driving shot of [SUBJECT] traveling through [SCENE], maintaining realistic lane position, speed, road perspective, and vehicle contact.
**Camera:** Low or side stabilized tracking camera.
**Motion:** Matched-speed highway tracking.
**Lighting:** Natural daylight or night road lighting.
**Avoid:** No lane teleportation, floating vehicle, impossible traffic behavior, or invented badges.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 13. /mountaindrive
**Purpose:** mountain road پر cinematic driving دکھانا.
**Prompt:** Create an 8-second cinematic mountain-drive shot of [SUBJECT] navigating [SCENE], emphasizing winding road geometry, elevation, realistic steering, and environmental scale.
**Camera:** Front three-quarter stabilized tracking camera.
**Motion:** Smooth road-following motion through bends.
**Lighting:** Natural mountain light and atmospheric depth.
**Avoid:** No road clipping, impossible turns, floating vehicle, or invented badges.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 14. /citydrive
**Purpose:** urban road پر cinematic vehicle movement دکھانا.
**Prompt:** Create an 8-second cinematic city-drive shot of [SUBJECT] moving through [SCENE], with realistic lanes, traffic spacing, reflections, and urban scale.
**Camera:** Stabilized front or side tracking camera.
**Motion:** Smooth matched-speed urban travel.
**Lighting:** Motivated street and practical lighting.
**Avoid:** No duplicated traffic, impossible lane changes, or invented vehicle badges.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 15. /convoy
**Purpose:** multiple vehicles کی coordinated cinematic movement دکھانا.
**Prompt:** Create an 8-second cinematic convoy shot of [SUBJECT] traveling with multiple vehicles through [SCENE], maintaining varied but coherent spacing, trajectories, and road contact.
**Camera:** Elevated or tracking wide camera.
**Motion:** Coordinated convoy movement with natural spacing.
**Lighting:** Consistent environmental reflections and exposure.
**Avoid:** No cloned vehicles, collisions, floating tires, or invented badges/logos.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 16. /vehiclelaunch
**Purpose:** vehicle reveal یا dramatic launch کو cinematic بنانا.
**Prompt:** Create an 8-second cinematic vehicle launch shot of [SUBJECT] in [SCENE], beginning with a controlled reveal and building into realistic forward acceleration while preserving vehicle geometry and road contact.
**Camera:** Low front three-quarter stabilized camera.
**Motion:** Controlled reveal followed by believable acceleration.
**Lighting:** Directional highlights and stable exposure.
**Avoid:** No teleporting, impossible acceleration, wheel deformation, or invented badges.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## QA
- 16/16 candidate commands have complete schema fields.
- Safety constraints included.
- Human approval remains required before publishing.
- This batch does not modify the locked 173-command registry.
