# Hidayat Video Command Library — Expansion Pack Audit (Pre-Lock)

## Status
PRE-LOCK REVIEW — not canonical yet.

## Baseline
- Locked v1 base: 98 unique commands.
- Locked v2 registry: 75 additions, with the existing v2 index claiming 173 total.
- This candidate list contains 88 explicitly named commands.
- No candidate is internally duplicated.

## Exact duplicates with the locked v2 command batches
These must NOT be added again:
- /craneup
- /cranedown
- /rackfocus
- /lensflare
- /anamorphic
- /matchcut
- /seamlesstransition
- /zoomtransition
- /whiptransition
- /spintransition
- /walkcycle
- /waterfall
- /bluehour
- /moonlight
- /productreveal
- /productmacro
- /shorts
- /reels
- /tiktok
- /loop
- /satisfying
- /trendstyle
- /thumbnailshot

Result: 23 exact duplicates.

## New exact command names
After removing those 23 duplicates, 65 names remain as new exact command candidates:
- Cinematic Camera: /jibshot, /dollyin, /dollyout, /truckleft, /truckright, /pedestalup, /pedestaldown, /focuspull, /macroshot, /firstperson
- Transitions: /morphtransition, /portaltransition, /flashtransition, /speedramp
- People & Character Motion: /runsequence, /turnaround, /headturn, /lookback, /hairflip, /gesture, /dance, /posechange, /expressionchange
- Nature & Environment: /ocean, /mountain, /desert, /forest, /beach, /cityscape, /countryside, /underwater, /cloudscape
- Advanced Weather: /storm, /thunderstorm, /mist, /duststorm, /windstorm, /raindrops, /wetroad, /puddles
- Time & Atmosphere: /sunrise, /starlight, /daytonight, /nighttoday, /seasonchange, /timewarp
- Vehicles Advanced: /carinterior, /wheelshot, /enginecloseup, /exhaustshot, /cockpit, /highwaydrive, /mountaindrive, /citydrive, /convoy, /vehiclelaunch
- Product & Commercial: /productrotate, /floatingproduct, /luxurycommercial, /adcinematic, /packshot, /beforeafter, /unboxing, /showcase
- Social Media: /hookshot

## Semantic/conflict review required before any lock
1. /hookshot — previously excluded from the locked Social Media set because it overlaps /viralshot. Keep rejected unless a materially distinct contract is defined.
2. /speedramp — overlaps the behavior of /vehiclespeedramp. Consider a broader canonical speed-ramp camera/effect command only if its scope is explicitly generalized and does not duplicate the vehicle-specific command.
3. /wetroad — overlaps /vehiclewetroad. It can be retained only as a scene/environment overlay or generalized wet-surface command with a scope distinct from vehicle-specific usage.
4. /macroshot — overlaps /vehiclecloseup and /productmacro at the technique level. Define it as a generic macro-camera command only if its subject scope is clearly generic.
5. /floatingproduct — overlaps the locked /productfloating conceptually. Treat as a rename candidate, not a new command, unless the intended semantics are demonstrably different.
6. /runsequence — overlaps /runningaction conceptually. Requires a distinct sequence/editing behavior to justify a new command.
7. /turnaround — overlaps /turnandreveal conceptually. Requires a distinct full-turn behavior rather than a simple reveal.
8. /gesture — overlaps /gesturefocus conceptually. Requires a generic motion-only contract distinct from camera emphasis.
9. /storm — overlaps the weather domain of /stormfront and may overlap /rain or related weather commands. Scope must be explicit.
10. /mist — overlaps /fog and /mistymorning. Requires a distinct atmospheric purpose.
11. /mountain, /desert, /forest — overlap existing /desertlandscape, /mountainreveal, /forestcinematic. These should be treated as candidate aliases/simplifications unless their contracts are distinct.
12. /ocean — overlaps /oceanwave conceptually. Distinguish broad environment from wave-action command.
13. /carinterior — overlaps /vehicleinterior. This should not be added as a duplicate vehicle-interior concept.
14. /productrotate — overlaps /product360. Distinguish only if it represents a different camera/product-rotation behavior.
15. /beforeafter — requires explicit safety/continuity rules so transformations do not imply identity manipulation or deceptive before/after claims.

## Safety review flags
- /morphtransition must be restricted to scene/object transitions where morphing is physically or visually appropriate; do not use it to morph real-person identities or anatomy.
- People commands must preserve identity, anatomy, clothing continuity, and avoid deceptive identity manipulation.
- Product commands must preserve exact product geometry/materials and avoid invented logos/text.
- Vehicle commands must preserve grounded contact, realistic mechanics, and avoid invented badges/logos.
- Transition commands must avoid hard cuts, exposure jumps, geometry warping, and unintended identity morphing.

## Decision
DO NOT lock the full 88-command list as-is.

The next official expansion should be built only from candidates that pass:
1. exact duplicate check,
2. semantic conflict/alias check,
3. safety check,
4. schema completeness,
5. placeholder check,
6. duration/format check,
7. cross-category uniqueness check.

This audit is the pre-lock gate; it does not change the locked 173-command registry.
