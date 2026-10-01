# Hidayat Video Command Library v2 — Batch 02: Vehicles Advanced

## Status
LOCKED v2 category — 10 commands

## Canonical schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /vehicletracking
**Purpose:** تیز رفتار گاڑی کو cinematic tracking camera کے ساتھ مسلسل follow کرنا۔
**Prompt:** Create an 8-second cinematic tracking shot of [SUBJECT] moving through [SCENE], with the camera maintaining a stable parallel follow and realistic speed, scale, reflections, and road contact.
**Camera:** Low parallel tracking camera, vehicle kept consistently framed.
**Motion:** Smooth matched-speed tracking with natural acceleration.
**Lighting:** Physically consistent environmental reflections and directional light.
**Avoid:** No floating vehicle, no wheel deformation, no invented badges/logos, no impossible camera movement.
**Format:** 8 seconds, 9:16 by default; 16:9 when requested.

## 2. /vehicleorbit
**Purpose:** گاڑی کے گرد controlled cinematic orbit کے ذریعے اس کی مکمل شکل نمایاں کرنا۔
**Prompt:** Create an 8-second cinematic orbit around [SUBJECT] in [SCENE], maintaining realistic vehicle proportions, wheel contact, reflections, and a controlled reveal of the full exterior.
**Camera:** Smooth low-to-mid-height orbit around the vehicle.
**Motion:** Constant controlled orbital movement while the vehicle remains grounded.
**Lighting:** Clean directional highlights with realistic surface reflections.
**Avoid:** No floating tires, no warped body panels, no invented badges/logos, no abrupt speed changes.
**Format:** 8 seconds, 9:16 by default.

## 3. /vehicleinterior
**Purpose:** گاڑی کے interior کو cinematic detail کے ساتھ دکھانا۔
**Prompt:** Create an 8-second cinematic interior shot of [SUBJECT] inside [SCENE], revealing the dashboard, steering area, seats, and material details with realistic depth and restrained camera movement.
**Camera:** Smooth interior dolly or slow pan at driver-eye height.
**Motion:** Controlled reveal across interior details.
**Lighting:** Natural ambient cabin light with believable highlights and shadows.
**Avoid:** No distorted dashboard, no duplicated controls, no floating objects, no invented logos.
**Format:** 8 seconds, 9:16 by default.

## 4. /vehiclelowangle
**Purpose:** low-angle framing سے گاڑی کو powerful cinematic presence دینا۔
**Prompt:** Create an 8-second low-angle cinematic shot of [SUBJECT] moving through [SCENE], emphasizing its silhouette, stance, wheel motion, and grounded road contact.
**Camera:** Very low front three-quarter camera.
**Motion:** Smooth forward tracking matched to vehicle speed.
**Lighting:** Directional highlights emphasizing contours without clipping.
**Avoid:** No unrealistic scale, no warped wheels, no floating vehicle, no invented badges/logos.
**Format:** 8 seconds, 9:16 by default.

## 5. /vehicleaerial
**Purpose:** aerial perspective سے گاڑی اور اس کے ماحول کو cinematic طور پر دکھانا۔
**Prompt:** Create an 8-second aerial cinematic shot of [SUBJECT] traveling through [SCENE], with a controlled drone-style camera that establishes both the vehicle and surrounding environment.
**Camera:** Elevated stabilized aerial camera.
**Motion:** Smooth follow or diagonal reveal with realistic parallax.
**Lighting:** Natural environmental lighting with consistent shadows.
**Avoid:** No impossible altitude changes, no vehicle duplication, no warped roads, no invented badges/logos.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 6. /vehiclecloseup
**Purpose:** گاڑی کی exterior details کو premium close-up میں نمایاں کرنا۔
**Prompt:** Create an 8-second macro-style cinematic close-up of [SUBJECT] in [SCENE], focusing on selected exterior details such as body texture, wheel, mirror, or headlight while preserving realistic materials and proportions.
**Camera:** Controlled close-up slider or macro tracking camera.
**Motion:** Slow precise lateral movement or micro push-in.
**Lighting:** Soft directional highlights with controlled reflections.
**Avoid:** No fake text, no invented logos, no melted materials, no duplicated details.
**Format:** 8 seconds, 9:16 by default.

## 7. /vehiclespeedramp
**Purpose:** گاڑی کی رفتار میں cinematic acceleration اور deceleration کو نمایاں کرنا۔
**Prompt:** Create an 8-second cinematic speed-ramp shot of [SUBJECT] moving through [SCENE], transitioning smoothly from controlled slow motion into realistic high-speed movement and back while preserving physical continuity.
**Camera:** Stabilized tracking camera with matched vehicle trajectory.
**Motion:** Smooth speed ramp with believable acceleration and wheel rotation.
**Lighting:** Consistent exposure and motion-blur response.
**Avoid:** No teleporting, no wheel freeze, no impossible acceleration, no body deformation, no invented badges/logos.
**Format:** 8 seconds, 9:16 by default.

## 8. /vehiclecornering
**Purpose:** موڑ کاٹتی ہوئی گاڑی کی controlled dynamic cinematic حرکت دکھانا۔
**Prompt:** Create an 8-second dynamic cornering shot of [SUBJECT] navigating a realistic turn in [SCENE], showing believable steering, suspension response, tire contact, and controlled camera tracking.
**Camera:** Low front three-quarter tracking angle.
**Motion:** Smooth arc following the corner with realistic body dynamics.
**Lighting:** Directional environmental light with consistent reflections.
**Avoid:** No sideways floating, no impossible tire angles, no road clipping, no invented badges/logos.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## 9. /vehiclesunset
**Purpose:** sunset ماحول میں گاڑی کا premium cinematic beauty shot بنانا۔
**Prompt:** Create an 8-second premium sunset beauty shot of [SUBJECT] in [SCENE], combining warm low-angle sunlight, controlled camera movement, realistic reflections, and a polished cinematic composition.
**Camera:** Slow front three-quarter dolly or orbit.
**Motion:** Gentle vehicle movement with smooth camera motion.
**Lighting:** Warm sunset key light with natural rim and long shadows.
**Avoid:** No overexposure, no artificial glow, no warped reflections, no invented badges/logos.
**Format:** 8 seconds, 16:9 or 9:16 as requested.

## 10. /vehiclewetroad
**Purpose:** گیلی سڑک، reflections اور cinematic atmosphere کے ساتھ گاڑی کا dramatic shot بنانا۔
**Prompt:** Create an 8-second cinematic shot of [SUBJECT] driving across a wet road in [SCENE], with realistic tire spray, road reflections, controlled camera tracking, and atmospheric depth.
**Camera:** Low tracking camera near road level.
**Motion:** Smooth matched-speed follow with believable tire spray.
**Lighting:** Soft overcast or controlled night lighting reflected naturally on the wet surface.
**Avoid:** No floating tires, no excessive spray, no mirror-like road without cause, no invented badges/logos, no body deformation.
**Format:** 8 seconds, 16:9 by default; 9:16 when requested.

## Batch QA
- 10/10 locked Vehicles Advanced commands covered.
- All are 8-second shot commands.
- Vehicle continuity and road contact safeguards included.
- No invented vehicle brand badges/logos.
- No new command names introduced.
