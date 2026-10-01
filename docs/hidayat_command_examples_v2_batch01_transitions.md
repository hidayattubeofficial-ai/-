# Hidayat Video Command Library v2 — Batch 01: Transitions

## Status
LOCKED v2 category — 8 commands

## Canonical schema
Command → Purpose → Prompt → Camera → Motion → Lighting → Avoid → Format

## 1. /matchcut
**Purpose:** دو مختلف مناظر کے درمیان ایک جیسی شکل یا composition کے ذریعے ہموار cinematic transition بنانا۔

**Prompt:** Create a seamless 2-second match-cut transition from [SCENE_A] to [SCENE_B], aligning a visually similar shape, position, or composition so the transition feels intentional and cinematic. Preserve [SUBJECT_A] and [SUBJECT_B] identity and key attributes without morphing.

**Camera:** Locked-off or precisely matched framing before and after the transition.
**Motion:** Minimal camera motion; transition driven by matched composition.
**Lighting:** Preserve the lighting logic of each scene without an exposure jump.
**Avoid:** No visible hard cut, no identity morphing, no exposure jump, no geometry warping, no flicker.
**Format:** 2 seconds, 9:16 vertical by default; 16:9 or 1:1 when requested.

## 2. /whiptransition
**Purpose:** تیز whip-pan حرکت کے ذریعے ایک منظر سے دوسرے منظر میں energetic transition بنانا۔

**Prompt:** Create a seamless 2-second whip-pan transition from [SCENE_A] to [SCENE_B], using a fast controlled horizontal camera sweep with natural motion blur that resolves cleanly into the second scene. Preserve subject continuity where applicable.

**Camera:** Fast horizontal pan.
**Motion:** Controlled whip movement with natural directional blur.
**Lighting:** Maintain believable exposure across the motion blur.
**Avoid:** No visible cut, no stutter, no exposure flash, no warped subjects, no artificial smear.
**Format:** 2 seconds, 9:16 by default.

## 3. /zoomtransition
**Purpose:** زوم اِن یا زوم آؤٹ کے ذریعے دو مناظر کو مسلسل cinematic movement میں جوڑنا۔

**Prompt:** Create a seamless 2-second zoom transition from [SCENE_A] into [SCENE_B], using a continuous controlled push or pull that naturally reveals the second scene. Keep [SUBJECT_A] and [SUBJECT_B] visually coherent without morphing.

**Camera:** Controlled optical-style push-in or pull-out.
**Motion:** Continuous zoom with smooth acceleration and deceleration.
**Lighting:** Keep exposure stable through the transition.
**Avoid:** No visible cut, no digital warping, no exposure jump, no subject deformation.
**Format:** 2 seconds, 9:16 by default.

## 4. /spintransition
**Purpose:** تیز rotational camera movement کے ذریعے energetic scene change بنانا۔

**Prompt:** Create a seamless 2-second rotational transition from [SCENE_A] to [SCENE_B], rotating the camera around the visual axis and resolving smoothly into the new composition. Maintain consistent subject geometry and scene direction.

**Camera:** Controlled 180–360-degree rotational move as appropriate to the shot.
**Motion:** Smooth continuous rotation with natural motion blur.
**Lighting:** Preserve plausible light direction and exposure.
**Avoid:** No visible cut, no spinning distortion, no geometry morphing, no flicker.
**Format:** 2 seconds, 9:16 by default.

## 5. /objectwipe
**Purpose:** کسی foreground object کے frame cross کرنے سے دوسرے منظر کو naturally reveal کرنا۔

**Prompt:** Create a seamless 2-second object-wipe transition where [DETAIL_A] or a foreground object passes across the lens and naturally reveals [SCENE_B]. Keep the wipe physically believable and preserve subject continuity.

**Camera:** Stable or lightly tracking camera.
**Motion:** Foreground object crosses the full frame at controlled speed.
**Lighting:** Match the object and scene exposure during the wipe.
**Avoid:** No visible cut, no transparent object artifacts, no exposure flash, no unnatural object deformation.
**Format:** 2 seconds, 9:16 by default.

## 6. /lightflash
**Purpose:** مختصر controlled light flash کے ذریعے cinematic scene transition بنانا۔

**Prompt:** Create a seamless 1-second light-flash transition from [SCENE_A] to [SCENE_B], using a brief motivated burst of light that fills the frame and naturally resolves into the second scene.

**Camera:** Hold framing stable through the transition.
**Motion:** Minimal camera motion; visual change is driven by the motivated light burst.
**Lighting:** Brief controlled flash with smooth falloff into the destination scene.
**Avoid:** No harsh clipping, no random strobe, no visible cut, no exposure jump beyond the intended flash.
**Format:** 1 second, 9:16 by default.

## 7. /blurtransition
**Purpose:** motion blur کے ذریعے پہلے منظر کو نرم انداز میں dissolve-like transition میں بدلنا۔

**Prompt:** Create a seamless 2-second blur transition from [SCENE_A] to [SCENE_B], progressively increasing natural motion blur until the frame becomes visually soft, then resolving cleanly into the second scene.

**Camera:** Smooth controlled camera movement.
**Motion:** Progressive directional blur with a clean recovery.
**Lighting:** Keep tonal balance consistent during the blur.
**Avoid:** No artificial smearing, no ghosting artifacts, no visible cut, no flicker, no subject morphing.
**Format:** 2 seconds, 9:16 by default.

## 8. /seamlesstransition
**Purpose:** واضح cut کے بغیر دو مختلف scenes کو مسلسل cinematic flow میں جوڑنا۔

**Prompt:** Create a seamless 3-second transition from [SCENE_A] to [SCENE_B], using continuous camera movement and environmental continuity to make the scene change feel physically motivated. Preserve [SUBJECT_A] and [SUBJECT_B] without identity morphing.

**Camera:** Continuous motivated camera movement that connects both compositions.
**Motion:** Smooth movement with consistent direction and speed.
**Lighting:** Preserve plausible lighting continuity while allowing natural scene differences.
**Avoid:** No visible cut, no morphing, no geometry warping, no exposure jump, no discontinuity artifacts.
**Format:** 3 seconds, 9:16 by default; 16:9 or 1:1 when requested.

## Batch QA
- 8/8 locked transition commands covered.
- Duration remains within the v2 transition range of 1–4 seconds.
- Required transition safeguards are included: no visible cut, no exposure jump, no morphing artifacts.
- Placeholders use the locked transition vocabulary.
- No new command names introduced.
