# ASK AJJI — backend

A FastAPI + SQLAlchemy backend for the ASK AJJI cultural heritage platform:
**Discover** (browse documented cultural knowledge) and **Preserve** (record
a voice story, transcribed/translated/classified by Gemini). Uses SQLite by
default (zero setup); swap in Postgres by setting `DATABASE_URL`.

This is a **backend-only** handoff — no frontend files are included or
modified. Everything below is testable through Swagger without a UI.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env — see below
uvicorn main:app --reload --port 8000
```

Open **http://127.0.0.1:8000/docs** for interactive Swagger docs, or
**http://127.0.0.1:8000/api/health** for a quick check.

### `.env` variables

| Variable | Required | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | Yes, for Preserve | Free-tier key from https://aistudio.google.com/apikey. Get requests fail with a clear error if unset — the rest of the API still works. |
| `JWT_SECRET` | Recommended | Signs login tokens. Generate with `python -c "import secrets; print(secrets.token_hex(32))"`. |
| `DATABASE_URL` | No | Defaults to local SQLite. Set to a Postgres URL to switch databases. |

On first run the app auto-creates `askajji.db` (SQLite) and seeds it with
~48 cultural entries across 8 categories and several states.

## Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | `/api/auth/register` | — | Create an account, returns a token |
| POST | `/api/auth/login` | — | Log in (OAuth2 form), returns a token |
| GET | `/api/auth/me` | ✅ | Current user's profile |
| GET | `/api/domains` | — | The 8 category cards (id, icon, color) |
| GET | `/api/entries?domain=&subcategory=&state=&region=&language=&q=` | — | Browse/search cultural entries |
| GET | `/api/entries/{id}` | — | One entry, including its `steps` |
| GET | `/api/festivals` | — | Festival calendar |
| GET | `/api/proverb-of-the-day` | — | Proverb of the day |
| GET | `/api/stats/cultural` | — | Counts grouped by state → category |
| POST | `/api/stories` | ✅ | Upload a story (multipart); Gemini processes it |
| GET | `/api/stories` | ✅ | **Your own** preserved stories, newest first |
| GET | `/api/stories/{id}` | ✅ | One of **your own** stories |
| DELETE | `/api/stories/{id}` | ✅ | Remove one of **your own** stories and its files |

`POST /api/stories` expects `multipart/form-data`:
- `title` (text, required)
- `contributor_name` (text, optional)
- `audio` (file, required)
- `photo` (file, optional)

`category`, `subcategory`, `state`, `region`, `original_transcript`,
`language_detected`, translations, `keywords`, and `summary` are **no
longer client-supplied** — Gemini fills them in from the audio itself.
This is a deliberate change from the original stub version, per the
Preserve flow spec (contributor just speaks, nothing typed).

Uploaded files are saved under `uploads/` and served back at
`/uploads/<filename>` — the URLs returned in `audio_url` / `photo_url`
are ready to drop into an `<audio>` or `<img>` tag once a frontend
connects.

## The Gemini pipeline (`ai_pipeline.py`)

```
audio file
   ↓  client.models.generate_content(model="gemini-2.5-flash", contents=[audio, prompt])
   ↓  response_mime_type="application/json"
structured JSON: {original_language, original_transcript, english_translation,
                  hindi_translation, marathi_translation, category, subcategory,
                  state, region, keywords, summary}
   ↓
Story row updated, processing_status="completed"
```

One Gemini request per story (not five separate calls), using
`gemini-2.5-flash` to stay on the free tier — no paid billing is enabled
anywhere in this code. If the request fails (missing key, network issue,
bad JSON back), `create_story` catches `AIProcessingError`, marks
`processing_status="failed"`, records `processing_error`, and **keeps the
original audio and the story row** — nothing is lost, and you can re-drive
processing later if you add a retry endpoint.

## Testing without a frontend (Swagger)

All of this happens at **http://127.0.0.1:8000/docs**.

1. **Register** — `POST /api/auth/register` → body `{"name": "...", "email": "...", "password": "..."}` (8+ chars). Copy the `access_token` from the response.
2. **Authorize** — click the padlock icon (top right of Swagger) → paste the token → Authorize. Every ✅ endpoint above now works from the docs UI.
3. **Login** (alternative to step 1 on a later run) — `POST /api/auth/login` takes a form with `username` = your email, `password` = your password.
4. **Get current user** — `GET /api/auth/me`.
5. **Get cultural entries** — `GET /api/entries` with no params, then try `?domain=Food%20%26%20Recipes` or `?q=saree`.
6. **Upload a story** — `POST /api/stories`, fill `title`, upload a small **10–20 second** audio clip (mp3/wav/m4a) as `audio`. Response includes `processing_status`.
   - If `processing_status` is `"failed"`, check `processing_error` — most commonly a missing/invalid `GEMINI_API_KEY`.
   - If `"completed"`, `original_transcript`, `english_translation`, `category`, etc. should be filled in.
7. **Retrieve your stories** — `GET /api/stories` — only stories from the account you're logged in as.
8. **Cultural statistics** — `GET /api/stats/cultural` — note the count for your story's `state`/`category`, upload another story classified the same way, and call it again to see the count increase.

### Example Gemini JSON response (what `ai_pipeline.py` parses)

```json
{
  "original_language": "Marathi",
  "original_transcript": "आज्जी नेहमी सांगायच्या...",
  "english_translation": "My grandmother used to say...",
  "hindi_translation": "मेरी दादी कहा करती थीं...",
  "marathi_translation": "माझी आज्जी नेहमी सांगायच्या...",
  "category": "Food & Recipes",
  "subcategory": "Sweets",
  "state": "Maharashtra",
  "region": "Western India",
  "keywords": ["puran poli", "jaggery", "Holi", "family recipe"],
  "summary": "A grandmother describes the family method for making puran poli, a jaggery-stuffed sweet flatbread made for Holi."
}
```

## Resetting the database in development

SQLite is a single file — delete it and restart the app to reseed from
scratch:

```bash
rm askajji.db
uvicorn main:app --reload --port 8000
```

Seeding is idempotent either way: `seed_if_empty()` only inserts
`CulturalEntry` / `Festival` / `Proverb` rows if their table is empty, so
restarting an already-seeded database never creates duplicates.

## Known limitations / what still needs the frontend

- No password-reset flow (out of scope for an MVP) — just register a new account if you forget a password in testing.
- No pagination on `/api/entries` or `/api/stories` — fine at hackathon scale, worth adding if the catalogue grows.
- No retry endpoint for a `"failed"` story — the row and audio persist, but re-running Gemini on it would need a small addition (e.g. `POST /api/stories/{id}/reprocess`) if you want it.
- `ai_pipeline.py` uses the current `google-genai` SDK surface as of this writing; since Google's SDK evolves quickly, if you hit an `AttributeError` around `types.Part` or `GenerateContentConfig`, check https://googleapis.github.io/python-genai/ for the latest signature.
- Frontend wiring (fetch calls from `ask-ajji.html` into these endpoints, using the token from login, building the multipart upload for Preserve) is intentionally **not done here** — connect it whenever the frontend source is available.
