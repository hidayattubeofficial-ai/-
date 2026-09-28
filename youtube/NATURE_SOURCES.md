# Hidayat Tube — Free Nature Video Sources

Checked 28 September 2026.

## Approved source candidates

1. **Pexels Videos** — https://www.pexels.com/videos/
   - Pexels states its photos and videos are free to use, including commercial use, without required attribution.
   - Clip-level restrictions still apply to identifiable people, brands, trademarks, and other third-party rights.
   - API automation requires a Pexels API key; the builder does not hard-code or expose a key.

2. **Pixabay Videos** — https://pixabay.com/videos/
   - Pixabay provides a large free/royalty-free video collection, including nature footage.
   - Each asset must still be checked against Pixabay's current license and any third-party rights shown in the footage.

3. **Mixkit Nature Videos** — https://mixkit.co/free-stock-video/nature/
   - Mixkit lists free nature stock videos and states that clips under its Free Video License can be used in commercial projects.
   - Some Mixkit items can have a Restricted License, so the collector must not assume every clip has identical rights.

4. **Coverr** — https://coverr.co/
   - Coverr's current license permits free commercial and non-commercial use of its videos.
   - The license also warns that depicted people, brands, trademarks, properties, and landmarks can have separate rights.

5. **Wikimedia Commons** — https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia
   - Used by the automated collector because file-level license/author metadata can be recorded with each downloaded asset.
   - The collector only accepts small video files and writes a JSON provenance record beside each asset.

## Current automation rule

The automated builder currently uses **Wikimedia Commons as the no-key download provider**. Pexels/Pixabay/Mixkit/Coverr are documented as approved discovery sources, but their website pages are not scraped blindly. If API credentials are added later, the provider can be wired through a dedicated adapter with per-asset license/provenance records.

Every downloaded nature asset must keep:
- source name
- source URL
- asset/page title
- license information
- creator/artist metadata when available
- download date

Unverified or license-ambiguous footage must not enter the video build.

YouTube publishing remains OFF and human approval remains required.
