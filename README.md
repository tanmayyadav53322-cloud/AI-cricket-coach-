# AI Cricket Coach

An AI-powered cricket video analysis and training platform for cricket players.
Static frontend (`index.html`) + a small Vercel serverless API (`/api`) that calls
Google's Gemini to actually analyze uploaded videos, + Supabase for accounts,
profiles and private video storage.

## Structure
- `index.html` — the app (home, profile, dashboard, analyze, results, plan), with SEO metadata and JSON-LD
- `api/` — Vercel serverless functions:
  - `analyze-video.js` — POST: starts a job (uploads the video to Gemini's Files API)
  - `analyze-video/[jobId].js` — GET: polls Gemini and runs the analysis once the file is ready
  - `videos/[videoId].js` — DELETE: removes a stored video + its analysis row
  - `_lib/` — Supabase auth helper, the Gemini system prompt, the Gemini API wrapper, and
    a "shape.js" normalizer that guarantees safe defaults even if Gemini's JSON is imperfect
- Content hub: `how-it-works.html`, `ai-cricket-video-analysis.html`, `batting-analysis.html`,
  `bowling-analysis.html`, `cricket-drills.html`, `cricket-technique.html`, `cricket-glossary.html`,
  `faq.html`, `blog/index.html`, `about.html`
- `assets/style.css`, `robots.txt`, `sitemap.xml`, `llms.txt`, `scripts/`
- `supabase/setup.sql` — tables, RLS policies, private storage bucket (safe to re-run)

## How analysis works
1. The browser uploads the video straight to a private Supabase Storage bucket and creates a
   short-lived signed URL for it (the video is never uploaded a second time to your server).
2. `POST /api/analyze-video` receives that signed URL, creates a row in the `analyses` table,
   and starts uploading the video to Gemini's Files API.
3. The browser polls `GET /api/analyze-video/{jobId}` every few seconds. Once Gemini's file is
   ready, one poll performs the actual `generateContent` call (with the full cricket-analysis
   system prompt in `api/_lib/prompt.js`) and stores the structured JSON result.
4. Every request runs as the signed-in user (their own Supabase access token is sent as a
   Bearer header) — the backend never uses a Supabase service-role key, so the same
   row-level-security policies protect it as protect the browser.

## Setup

### 1. Supabase
Run `supabase/setup.sql` in the Supabase SQL Editor (safe to re-run). It's already using
project `qzxslpattuzeqwwahzxm` with the publishable key embedded in `index.html` and
`api/_lib/supabase.js` — both are safe to expose publicly.

### 2. Gemini
Get an API key at https://aistudio.google.com/apikey. You'll add it as an environment
variable in the next step — never put it in `index.html` or commit it to git.

### 3. Deploy (Vercel required)
This project needs a host that runs the `/api` serverless functions alongside the static
files — **Vercel** is the easiest fit for this repo as-is (Netlify or another provider would
need the API rewritten for their function format).

```
npm i -g vercel
cd ai-cricket-coach
npm install
vercel --prod
```
Then in the Vercel dashboard: Project → Settings → Environment Variables → add `GEMINI_API_KEY`
(see `.env.example`), and redeploy.

### 4. Before you launch
- **Domain:** every URL uses the placeholder `https://aicricketcoach.app`. Run
  `python3 scripts/set-domain.py https://your-domain.com`, then
  `python3 scripts/build-sitemap.py https://your-domain.com`.
- **Add `assets/og-image.png`** (1200x630) — referenced for social previews but not included.

## Known limits (not verified against a live deploy)
- **Timeouts:** `vercel.json` sets `maxDuration: 60`. A slow Gemini response on a long video
  could exceed this on some Vercel plans — if you see timeouts, either upgrade your plan's
  function duration limit or shorten `MAX` video length.
- **First `analyzing` poll does no work on purpose** (it just flips the status) so the
  progress bar visibly advances before the slower generation call — this roughly doubles the
  minimum poll count but costs no extra Gemini calls.
- **JSON reliability:** `api/_lib/shape.js` fills in safe defaults for any field Gemini omits
  or gets a type wrong, so a slightly imperfect response still renders instead of crashing.
- I could not run this end-to-end (no network access in the environment that built it) — if
  something doesn't match the real Gemini or Supabase JS SDK behavior exactly, check the
  Vercel function logs first; most of the code paths log the underlying error with `console.error`.

## Status
Accounts, profiles, video recording/upload, validation and now real AI analysis (Gemini) are
wired up end-to-end. Update the About/FAQ/Limitations copy once you've verified it end-to-end
in production — they currently say analysis is "under development."
