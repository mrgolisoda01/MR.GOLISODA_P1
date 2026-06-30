# MR.GOLISODA — Burn / PJP Management

Single-page app (HTML/CSS/JS) served by Flask, with Supabase for persistence.

## Structure
```
mr_golisoda/
├── app.py                 # Flask server + /api/state persistence
├── requirements.txt
├── .env.example           # copy to .env and fill in
├── supabase/schema.sql    # run once in Supabase SQL editor
├── templates/index.html   # page shell
└── static/
    ├── css/app.css        # all styles
    └── js/app.js          # full app + Supabase bridge (cloudSave/cloudLoad)
```

## Setup
1. `python -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create a Supabase project → SQL editor → run `supabase/schema.sql`
4. `cp .env.example .env` and fill `SUPABASE_URL`, `SUPABASE_KEY`
5. `python app.py`  → open http://localhost:5000  (login: admin / admin)

Production: `gunicorn app:app`

## Persistence (Supabase)
- The app keeps its data in memory and mirrors it to Supabase via the Flask
  endpoint `/(GET|PUT) /api/state/<key>` (one JSON row, key `golisoda_main`).
- In `static/js/app.js`, `cloudLoad()` hydrates the stores on boot and
  `cloudSave()` pushes them. Wire `cloudSave()` after the actions that should
  persist (YOLO upload, PJP submit, expense approve, master edits) and call
  `await cloudLoad()` once before the first render in the boot sequence.
- Without `.env` configured the app still runs fully on its embedded seed data.

## Notes
- Embedded data: 33 franchises, 246 routes, real May-2026 burn, 77 logins.
- For true multi-user concurrency, give each entity its own table (next step);
  the single-blob model above is the simplest persistence and fine to start.
