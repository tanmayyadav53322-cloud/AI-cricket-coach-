# AI Cricket Coach

A mobile-first web app for cricket players to record or upload a technique video,
review it, and (once a computer-vision backend is connected) get AI coaching
feedback, drills, and a 7-day training plan.

This is a static, single-page app (`index.html`) with no build step. Backend
data (accounts, profiles, uploaded videos) is handled by Supabase.

## What's real today

- **Accounts:** email/password sign up and sign in (Supabase Auth)
- **Profile:** saved to the `profiles` table, synced per account
- **Video upload:** recorded/selected videos are validated (length, size,
  resolution, brightness) and uploaded to a private Supabase Storage bucket
- **History:** analyses are saved in the `analyses` table
- **Camera:** real device camera recording via `getUserMedia` + `MediaRecorder`
  when served over HTTPS, with a phone-camera-app fallback everywhere else

## What's NOT connected yet

- **AI / computer-vision analysis.** There is no model wired up. The app is
  built to call `POST {API_BASE}/api/analyze-video` (see the comment above
  `const API_BASE` in `index.html` for the exact request/response contract),
  but `API_BASE` is `null` until you point it at a real service. Until then,
  the app is honest about this and shows "Analysis unavailable" /
  "AI video analysis is not configured yet."

## 1. Set up Supabase

1. Open your project at https://supabase.com/dashboard (project ref:
   `qzxslpattuzeqwwahzxm`).
2. Go to **SQL Editor → New query**, paste the contents of
   `supabase/setup.sql`, and run it. This creates:
   - `profiles` and `analyses` tables with row-level security
     (each user can only see/edit their own rows)
   - a private Storage bucket named `cricket-videos` with matching policies
3. (Optional) Under **Authentication → Providers → Email**, turn email
   confirmation off if you want new accounts to be usable immediately
   without clicking a confirmation link.

The app already has your project URL and publishable (anon) key hard-coded
in `index.html` — search for `SUPABASE_URL` / `SUPABASE_ANON_KEY` if you ever
need to point it at a different project.

## 2. Deploy

This is a single static HTML file, so any static host works. Pick one:

**Vercel**
```
npm i -g vercel
cd ai-cricket-coach
vercel --prod
```

**Netlify**
```
npm i -g netlify-cli
cd ai-cricket-coach
netlify deploy --prod
```

**GitHub Pages**
1. Push this folder to a GitHub repo.
2. Repo Settings → Pages → deploy from the `main` branch, root folder.

Camera recording and Supabase both require **HTTPS** (or `localhost` for
local testing) — all three options above serve HTTPS by default.

## 3. Test locally (optional)

```
cd ai-cricket-coach
python3 -m http.server 8000
```
Then open `http://localhost:8000` in Chrome on your computer. For testing
on an Android phone, use one of the HTTPS deploy options above instead —
phones can't reach your computer's `localhost`.

## Connecting a real AI analysis backend later

Build any backend that implements the contract documented above
`const API_BASE` in `index.html`, then set `API_BASE` to its URL. The
frontend already handles the full upload → processing → results flow,
including polling a job status endpoint, so no other frontend changes
should be needed for a basic integration.
