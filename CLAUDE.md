# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single-page marketing site for **I Hate My Rates** (insurance comparison: auto, home, bundle, renters, life, business). The whole site is one file, `index.html` (~690 KB, originally exported as `I Hate My Rates website – I Hate My Rates v2.html`). It is a self-unpacking bundle exported from a design tool, not hand-written HTML. There is no package.json, build step, linter or test suite. It deploys to Vercel as a static site (`vercel.json`) from the GitHub repo `S3LabsAI/Ihate-my-rates`; pushes to `main` go to production.

**Preview:** open the file in a browser. It needs JavaScript and `DecompressionStream`, so use a current Chrome, Safari or Firefox. Nothing renders with JS disabled.

## How the bundle works

The outer document is only a loader. The real page is stored in `<script>` data islands:

- `__bundler/template`: the actual page HTML, stored as a **JSON-encoded string**. Asset references inside it are bare UUIDs (for example `src="16bcec7d-..."`).
- `__bundler/manifest`: a JSON map `uuid -> {mime, data (base64), compressed (gzip bool)}` holding every asset: the two PNG logos, the support runtime JS, React/ReactDOM 18.3.1 UMD, and the Archivo / JetBrains Mono woff2 subsets.
- `__bundler/ext_resources`: maps the original CDN URLs (jsdelivr React 18.3.1) to manifest UUIDs.
- `__bundler/page_order`: nested iframe pages. It is empty here.

At load, the bootstrap script decodes the manifest into blob/data URLs, replaces each UUID in the template, and swaps the template in as `document.documentElement`. The support runtime (manifest asset `b6f0ab93-…`, loaded by the template's first `<script src>`) then renders the `<x-dc>` component with React.

**Editing workflow:** `python3 tools/bundle.py unpack` writes the decoded template to `build/template.html` (git-ignored); edit that, then `python3 tools/bundle.py pack` writes it back into `index.html` with `</` escaped.

**Scroll headline animation:** `src/shred.html` is the source for the sliced-letter effect on the hero H1 and the "Cheap rate.", "How we shop it." and "Low price." H2s. It is pasted into the template `<head>` between the `<!-- shred:start -->` and `<!-- shred:end -->` markers. Two runtime quirks shaped it: the x-dc runtime discards anything in `<body>` outside `<x-dc>` and drops unknown attributes such as `data-*`, so the script lives in `<head>` and finds the headings by tag and text, then tags them itself. The real heading text stays in the DOM (hidden with `-webkit-text-fill-color` while an `aria-hidden` overlay animates) and is shown again once assembled. It is skipped under `prefers-reduced-motion`.

**Editing:** the template is an escaped JSON string inside a 690 KB line-oriented file, so don't make text replacements in the outer file blindly. Do this instead: parse the `__bundler/template` island with `json.loads`, edit the decoded HTML, then write it back with `json.dumps`. Make sure the result contains no literal `</script>` (escape it as `<\/script>`). Edit assets the same way: base64-decode, gunzip if `compressed`, change, re-encode. Keep the UUIDs stable. Keep the OFL font-license comment at the top of the file, because it is required when the file is redistributed.

## Template language (`<x-dc>` component format)

The decoded template has this structure:

- `<helmet>…</helmet>`: content that goes in `<head>` (the `@font-face` rules and a small global `<style>`).
- The markup body, with **inline styles everywhere**. No class-based CSS.
- `<script type="text/x-dc" data-dc-script data-props='…'>`: the component logic.

The template syntax:

- `{{ expr }}` interpolates values returned from `renderVals()`.
- `<sc-if value="{{ bool }}">` and `<sc-for list="{{ arr }}" as="item">` handle conditionals and loops. Inside a loop, read fields as `{{ item.field }}`. Conditionals take only booleans, so `renderVals` precomputes flags such as `s0..s4`, `headA/B/C` and `tb.on/off`.
- `sc-camel-on-click`, `sc-camel-on-change`, `sc-camel-max-length` and similar attributes map to React camelCase props (`onClick`, `maxLength`, and so on).
- `style-hover` and `style-focus` set inline style overrides for those pseudo-states.
- `hint-placeholder-val` and `hint-placeholder-count` only control how the design editor previews the page. Keep them in sync when you add `sc-if` or `sc-for` blocks.
- `data-props` declares editor-exposed props. Right now that's `headline`, an enum of three hero headlines that switches the H1 through `headA/B/C`.

How the logic is written:

- It's a `class Component extends DCLogic` with React-style `state` and `setState`.
- `renderVals()` returns every value and handler the template uses.
- The scenario copy for the "Price vs. value" section is in the top-level `SCEN` object. The "How it works" steps and the FAQs are inline arrays in `renderVals()`.

## Page structure and behavior

The page runs top to bottom:

1. Sticky header with the logo PNG
2. Hero (`#top`) with a 4-step quote widget: type → ZIP → monthly premium slider → contact → thank-you
3. `#value`: Auto/Home/Bundle tabs comparing a cheap policy with the right policy on out-of-pocket cost after a claim
4. `#how`: five steps
5. FAQ accordion
6. CTA band
7. Footer with the disclaimer

**The quote widget has no backend.** Validation is client-side only: a 5-digit ZIP, plus a name, an email matching `.+@.+\..+` and a phone with ≥10 digits. "Submitting" only moves to step 4. Footer links (Privacy, Terms, Licensing, Contact) are `href="#"` placeholders.

## Design tokens (inline, keep consistent)

- **Colors:**
  - Background `#F2EFE8`
  - Ink `#111`
  - Accent `#FF3B1F`
  - Rules and panels `#E6E1D6` and `#CFC9BC`
  - Muted text `#BDB8AE`, `#8a857c` and `#444`/`#666`
  - Dark sections `#111` with `#3a3a3a` borders
- **Type:** Archivo is a variable-width face. Headlines use weight 900, uppercase, `font-stretch` 72–85% and tight line-height (.84–.95). JetBrains Mono (500/700) is used for labels and tags.
- **Layout:** borders are 2–3px solid `#111`. Corners are square, with no border-radius except the accent dot. Max width is 1320px, padding is `clamp(16px,4vw,40px)`, and sizes are fluid `clamp()` values.
