# I Hate My Rates — website

Marketing site for **ihatemyrates.com** (insurance comparison: auto, home, bundle, renters, life, business).

## Structure

- `index.html` — the whole site. It is a self-unpacking bundle exported from a design tool (the page HTML, JS runtime, React 18.3.1 and fonts are embedded as data islands). See `CLAUDE.md` for how it works and how to edit it safely.
- `vercel.json` — static hosting config (clean URLs, security headers, no-cache on the HTML).

## Local preview

Open `index.html` in a current Chrome, Safari or Firefox, or serve the folder:

```bash
python3 -m http.server 8000
```

## Deployment

Static site on Vercel, no build step. Pushes to `main` deploy to production; other branches and PRs get preview deployments.
