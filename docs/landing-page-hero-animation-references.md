# Landing Page Hero Animation — Reference & Mood Board

Research notes for the "intro reel" / hero animation on the Potential landing page.

**Note on Pinterest:** Pinterest's API requires OAuth developer credentials (app ID/secret/access token) that aren't configured in this environment, and direct scraping of Pinterest board pages returns 403s to automated fetchers. The boards below are good starting points to open manually and pin from; everything else here was sourced via general web/design-award research (Awwwards, Codrops, case studies).

## Brand context (from the logo)

- Wordmark **"Potential"** — the capital **P** is solid red, the rest of the mark is black, single weight, geometric sans.
- Tagline: **"Every space. Delivered."** — reads as a logistics / space-as-a-service / proptech positioning (delivering/fulfilling physical space).
- Palette is intentionally minimal: red + black + white. Any hero animation should keep this restraint rather than introducing new colors — motion and negative space are the story, not extra color.
- The "P" as an isolated mark is a strong candidate for a standalone animated logo lockup (mask reveal, stroke draw-on, or the P "delivering" the rest of the wordmark into place).

## Pinterest boards to pull from directly

Open these manually (they're public boards, just not scrapable by automated tools) and save pins that match the categories below:

- Wordmark logo animation ideas — https://www.pinterest.com/ideas/wordmark-logo-animation/898245468331/
- Logo animation / kinetic typography — https://www.pinterest.com/sleepswim/logo-animation-kinetic-typography/
- Agency reels & motion graphics — https://www.pinterest.com/kieranm1/agency-reels-and-motion-graphics/
- Show reels — https://www.pinterest.com/renderfeed/show-reels/
- Agency show reels — https://www.pinterest.com/aidankenny111/agency-show-reels/

## Award-site references (Awwwards / Codrops)

| Reference | Why it's relevant |
|---|---|
| [Netlify — "5 Million Developers"](https://www.awwwards.com/inspiration/landing-page-intro-animation-5-million-developers) | Landing/intro animation built around a single bold statement, similar scale to a tagline-first hero. |
| [Hero Intro — "Solar Journey"](https://www.awwwards.com/inspiration/hero-intro-animation-solar-journey) | Text stagger + smooth transitions + GSAP + light 3D — good reference for a typographic-led (not asset-heavy) hero. |
| [Manuport Logistics](https://www.awwwards.com/sites/manuport-logistics-2) | Logistics-sector site; 3D animation built around "path"/movement as a recurring motif — directly relevant to a "delivery" narrative. |
| [Hero Section — "Mosey"](https://www.awwwards.com/inspiration/hero-section-animations-mosey) | Clean hero-section motion with 3D typography, minimal palette. |
| [Studio Freight — "Repeat" case study](https://www.awwwards.com/case-study-repeat-by-studio-freight.html) | Reference for build technique, not visual style: GSAP timelines + Lottie + parallax "wipe" transitions between sections — a good technical pattern for an intro reel that hands off into the rest of the page. |
| [TruckPress — Warehouse/Logistics/Transportation theme](https://www.awwwards.com/sites/truckpress-warehouse-logistics-transportation-wp-theme) | Closest industry match (warehousing/logistics) for layout and motion pacing conventions. |

## Concept directions for Potential's intro reel

1. **"P delivers the wordmark"** — the red P enters first (draw-on stroke or drop-in), then black letterforms assemble left-to-right as if being "delivered" into place, landing on the full wordmark + tagline fading in last. Reinforces "Every space. Delivered." literally through motion.
2. **Space/grid reveal** — a minimal grid or floor-plan-like line pattern (nodding to "space") draws in behind the wordmark, then dissolves/wipes away as the logo settles — evokes warehouse/floor-plan without needing photography.
3. **Mask/clip-path reveal** — SVG clip-path of the P mark expands to reveal a short looping background (subtle grid, dot pattern, or muted footage of space/warehouse interiors), then contracts back to solid red as the wordmark locks in. Matches the "Repeat" wipe-transition pattern above.

## Suggested technique stack

- **GSAP** (Timeline + SplitText) for the letter/word choreography — industry standard for this exact kind of sequenced reveal.
- **Lottie** if the intro is designed in After Effects first (fastest path to a polished "reel" feel without hand-coding every keyframe).
- **SVG `clip-path` / mask** for the P-shaped reveal or wipe transitions.
- **Lenis / ScrollSmoother** only if the intro is meant to hand off into a scroll-driven hero rather than autoplay-once.

## Suggested pacing (≈3–4s intro, autoplays once on load)

| Time | Beat |
|---|---|
| 0.0–0.6s | Red P draws on / drops in on empty canvas |
| 0.6–1.6s | Black letterforms of "otential" stagger in from the P outward |
| 1.6–2.2s | Brief hold on full wordmark |
| 2.2–3.0s | Tagline "Every space. Delivered." fades/slides in beneath |
| 3.0s+ | Wordmark settles into header position (or reel loops/fades to main hero content) |

## Next steps

- Pull 8–12 concrete pins from the Pinterest boards above into a shared board for team sign-off on visual direction.
- Pick one of the three concept directions before scaffolding any code.
- No frontend project exists in this repo yet — animation implementation should happen once the concept is approved and the base landing-page project is scaffolded.
