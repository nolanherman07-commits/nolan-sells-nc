---
name: website-quality
description: Nolan's standard for every website Herman Technical Solutions builds (agent sites, listing sites, the HTS site). Use when building, redesigning, reviewing or shipping any website or landing page — it covers the motion toolkit (GSAP, Lenis, React Bits), the 20-point launch checklist and the 20-point design checklist, and how to verify them before saying a site is done.
---

# Website quality standard (Herman Technical Solutions)

Every site ships only after it passes **both checklists below** and the **verification** steps.
Navy and gold are the HTS brand (`#14213d` / `#070d1c` navy, `#d4af37` / `#f0d27a` gold). Client sites use the client's own brand.

## 1. Motion toolkit

Use these instead of hand-rolled scroll math.

| Tool | What it's for | Link |
|---|---|---|
| **GSAP** + ScrollTrigger | Every animation: reveals, pinned sections, scrubbed parallax, count-ups, magnetic buttons, feedback (shake, check marks) | https://github.com/greensock/GSAP |
| **Lenis** | Smooth, "buttery" scrolling | https://github.com/darkroomengineering/lenis |
| **React Bits** | Ready-made animated text, backgrounds and components — **only when the project is React** | https://github.com/DavidHDev/react-bits |

Plain HTML sites: `npm install gsap lenis` and bundle with esbuild into one file
(`npx esbuild src/main.js --bundle --minify --format=iife --outfile=js/site.js`).

Wire Lenis into GSAP's clock so ScrollTrigger and smooth scroll never disagree:

```js
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
gsap.registerPlugin(ScrollTrigger);
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (!reduced) {
  const lenis = new Lenis({ lerp: 0.1 });
  lenis.on("scroll", ScrollTrigger.update);
  gsap.ticker.add((t) => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);
}
```

Motion rules:
- Animate only `transform` and `opacity`. Never width/height/top/left.
- Don't let CSS `transition: transform` fight GSAP on the same element. GSAP owns transforms.
- Pin sideways galleries with ScrollTrigger (`pin`, `scrub`, `invalidateOnRefresh`), only on desktop (`ScrollTrigger.matchMedia`). Stack them on phones.
- Every animation has a `prefers-reduced-motion` fallback that shows the final state.
- Motion should mean something: arrival, feedback, progress. Not decoration.

**UI UX Pro Max** is installed next to this skill (`.claude/skills/ui-ux-pro-max`, MIT, from https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
Use it for design decisions and reviews, for example:
`python3 .claude/skills/ui-ux-pro-max/scripts/search.py "real estate agent website" --design-system`
or one concern at a time: `--domain ux`, `--domain typography`, `--domain color`, `--domain gsap`.
Its palette suggestions never override a brand: HTS stays navy and gold, client sites keep the client's colors.

Optional extra the owner sets up with their own key (don't install silently):
- **21st.dev Magic MCP** (component generator, needs a 21st.dev API key): `claude mcp add magic --scope user --env API_KEY="<key>" -- npx -y @21st-dev/magic@latest`

## 2. Launch checklist (functional)

1. **No horizontal scroll.** `document.documentElement.scrollWidth === innerWidth` at 390px and 1440px.
2. **No broken links.** Every `href` and `src` returns 200 (check external sites too).
3. **Mobile menu.** If nav links hide on phones, a menu button opens them (with `aria-expanded`, closes on Esc and on link tap).
4. **Favicon** (SVG + 180px apple-touch-icon).
5. **Page titles**: unique, specific, under ~60 characters.
6. **Meta description** on every page (plus Open Graph title, description and image with full URLs).
7. **Footer links**: site sections, live work, phone, text, email, back to top.
8. **Custom 404 page** (`404.html` at the repo root for GitHub Pages, with absolute links home).
9. **Copyright year** filled in by script, with the current year as the fallback text.
10. **Compressed images**: WebP, max ~1400px wide, `width`/`height` attributes, `loading="lazy"` below the fold, `img { height: auto }`.
11. **No broken buttons**: every button does something; anchors land below the fixed header.
12. **Success messages** after every form send (animated, focusable, says what happens next).
13. **Error messages** next to the field (`aria-invalid`, `aria-describedby`, `aria-live`), not only at the top.
14. **No placeholder text** (lorem, TODO, "your name here") unless it's clearly a mockup.
15. **No unused nav**: every nav link points to something that exists.
16. **No mobile overflow**: long words, wide tables and fixed widths checked at 390px.
17. **Clickable logo** goes home or back to the top.
18. **Clickable phone number** (`tel:`) and text link (`sms:`).
19. **Clickable email** (`mailto:`).
20. **Mobile optimised**: tap targets ≥ 44px, readable sizes, nothing hidden behind the header, works with one thumb.

Forms that use FormSubmit must check `res.success === "true"`. It answers HTTP 200 even when it didn't deliver.

## 3. Design checklist (visual polish)

1. **Delete filler badges**: no decorative icons or pills that say nothing.
2. **Drop redundant labels**: no eyebrow that repeats its headline.
3. **Unitalicize random words**: one intentional italic accent at most (e.g. the hero), not half of every headline.
4. **Mono only where needed** (code, data), never as decoration.
5. **Use a design system**: color, radius, spacing and type tokens as CSS variables; no one-off values.
6. **Show the actual product**: real screenshots of real sites, not stock mockups.
7. **Enlarge the main feature**: the thing you sell gets the most space.
8. **Group with spacing**, not boxes and lines.
9. **Make headlines specific**: say what it is or what they get.
10. **Emphasize the CTA**: one primary button style, used for the main action only.
11. **One accent colour** (gold for HTS), used with purpose.
12. **Keep icons consistent**: one icon set, one stroke weight, or no icons.
13. **Remove embellishments** that don't help (noise overlays, random shapes).
14. **Inner radius = outer radius − padding** (16px card with 10px padding → 6px image).
15. **Text contrast** ≥ 4.5:1 for body, 3:1 for large text.
16. **Wrap headlines properly**: `text-wrap: balance` on headings, `pretty` on paragraphs.
17. **Align by eye, not pixels**: optically centre icons, play buttons, quotes.
18. **Tabular numbers** (`font-variant-numeric: tabular-nums`) for stats, counters and prices.
19. **Loading states**: spinner and disabled button while sending; reserved space for images.
20. **Animate useful feedback**: drawn check mark on success, shake on an invalid field, press scale on buttons.

## 4. Verify before calling it done

Run the site locally and check with Playwright (Chromium is preinstalled):
- Desktop 1440×900 and iPhone 13: screenshots of the opening, hero, every section and the menu open.
- Zero `pageerror`s and zero 4xx/5xx responses.
- `scrollWidth` equals the viewport width on both sizes.
- Submit the form empty and with bad values: errors appear next to the fields.
- Every external link answers 200 (`curl -s -o /dev/null -w '%{http_code}' -L <url>`).
- After pushing, load the live URL and repeat the error and broken-image check.

Report honestly what passed, what didn't, and what you couldn't test.
