"""
ASK AJJI backend — FastAPI + SQLAlchemy.

Run locally:
    pip install -r requirements.txt
    cp .env.example .env      # then fill in GEMINI_API_KEY and JWT_SECRET
    uvicorn main:app --reload --port 8000

Then open http://127.0.0.1:8000/docs for interactive API docs.
See README.md for endpoint details and how this pairs with the
ask-ajji.html frontend (not included in this backend-only handoff).
"""
import os
import shutil
import uuid
from collections import defaultdict
from typing import Optional

from dotenv import load_dotenv

load_dotenv()  # must run before anything reads os.getenv, so do it first

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import schemas
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from seed_data import seed_if_empty, DOMAINS
from ai_pipeline import transcribe_and_analyze_audio, AIProcessingError

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASK AJJI API", version="0.2.0")

# Wide-open CORS for local development — tighten this to your real
# frontend origin(s) before deploying.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# The frontend (index.html) is served directly by this backend at "/" so
# it and the API share one origin — its fetch calls use a relative
# API_BASE ('') and just work, with no CORS gymnastics needed.
FRONTEND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")


@app.on_event("startup")
def on_startup():
    db = next(get_db())
    seed_if_empty(db)


@app.get("/")
def serve_frontend():
    if not os.path.exists(FRONTEND_PATH):
        raise HTTPException(status_code=404, detail="index.html not found next to main.py")
    return FileResponse(FRONTEND_PATH)


def story_to_out(story: models.Story) -> schemas.StoryOut:
    data = schemas.StoryOut.model_validate(story)
    data.audio_url = f"/uploads/{story.audio_path}"
    if story.photo_path:
        data.photo_url = f"/uploads/{story.photo_path}"
    return data


# ---------------------------------------------------------------- health
@app.get("/api/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------- AUTH
@app.post("/api/auth/register", response_model=schemas.Token, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")

    user = models.User(
        name=payload.name.strip(),
        email=payload.email.lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=str(user.id))
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@app.post("/api/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm gives us .username / .password — Swagger's
    # built-in "Authorize" button expects exactly this shape, so we treat
    # the "username" field as the email.
    user = db.query(models.User).filter(models.User.email == form_data.username.lower()).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(subject=str(user.id))
    return schemas.Token(access_token=token, user=schemas.UserOut.model_validate(user))


@app.get("/api/auth/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


# ---------------------------------------------------------------- DISCOVER
@app.get("/api/domains", response_model=list[schemas.DomainOut])
def list_domains():
    return DOMAINS


@app.get("/api/entries", response_model=list[schemas.CulturalEntryOut])
def list_entries(
    domain: Optional[str] = Query(None, description="e.g. 'Food & Recipes'"),
    subcategory: Optional[str] = Query(None),
    state: Optional[str] = Query(None, description="e.g. Maharashtra"),
    region: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="search name/description/state"),
    db: Session = Depends(get_db),
):
    query = db.query(models.CulturalEntry)
    if domain:
        query = query.filter(models.CulturalEntry.domain == domain)
    if subcategory:
        query = query.filter(models.CulturalEntry.subcategory == subcategory)
    if state:
        query = query.filter(models.CulturalEntry.state == state)
    if region:
        query = query.filter(models.CulturalEntry.region == region)
    if language:
        query = query.filter(models.CulturalEntry.language == language)
    if q:
        like = f"%{q}%"
        query = query.filter(
            models.CulturalEntry.name.ilike(like)
            | models.CulturalEntry.description.ilike(like)
            | models.CulturalEntry.state.ilike(like)
        )
    return query.order_by(models.CulturalEntry.domain, models.CulturalEntry.state).all()


@app.get("/api/entries/{entry_id}", response_model=schemas.CulturalEntryOut)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.get(models.CulturalEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@app.get("/api/festivals", response_model=list[schemas.FestivalOut])
def list_festivals(db: Session = Depends(get_db)):
    return db.query(models.Festival).all()


@app.get("/api/proverb-of-the-day", response_model=schemas.ProverbOut)
def proverb_of_the_day(db: Session = Depends(get_db)):
    proverb = db.query(models.Proverb).first()
    if not proverb:
        raise HTTPException(status_code=404, detail="No proverbs yet")
    return proverb


# ---------------------------------------------------------------- STATS
@app.get("/api/stats/cultural")
def cultural_stats(db: Session = Depends(get_db)):
    """
    Counts grouped by state -> category, e.g.:
        {"Maharashtra": {"Food & Recipes": 5, "Clothing & Draping": 3}}
    Combines the seeded CulturalEntry catalogue with completed, preserved
    Stories, so a newly processed story bumps its state/category count
    without any hardcoded numbers.
    """
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for state, domain in db.query(models.CulturalEntry.state, models.CulturalEntry.domain):
        if state and domain:
            counts[state][domain] += 1

    completed_stories = (
        db.query(models.Story.state, models.Story.category)
        .filter(models.Story.processing_status == "completed")
    )
    for state, category in completed_stories:
        if state and category:
            counts[state][category] += 1

    return {state: dict(categories) for state, categories in counts.items()}


# ---------------------------------------------------------------- PRESERVE
@app.post("/api/stories", response_model=schemas.StoryOut)
async def create_story(
    title: str = Form(...),
    contributor_name: Optional[str] = Form(None),
    audio: UploadFile = File(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    audio_filename = f"{uuid.uuid4().hex}_{audio.filename}"
    audio_path = os.path.join(UPLOAD_DIR, audio_filename)
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio.file, f)

    photo_filename = None
    if photo is not None:
        photo_filename = f"{uuid.uuid4().hex}_{photo.filename}"
        with open(os.path.join(UPLOAD_DIR, photo_filename), "wb") as f:
            shutil.copyfileobj(photo.file, f)

    story = models.Story(
        user_id=current_user.id,
        title=title.strip(),
        contributor_name=contributor_name,
        audio_path=audio_filename,
        photo_path=photo_filename,
        processing_status="processing",
    )
    db.add(story)
    db.commit()
    db.refresh(story)

    # ---- AI preservation pipeline (Gemini — see ai_pipeline.py) ----
    # If this fails, the story row and the original audio are kept —
    # only processing_status/processing_error change — so nothing the
    # contributor recorded is ever lost.
    try:
        result = transcribe_and_analyze_audio(audio_path)
        story.original_transcript = result["original_transcript"]
        story.language_detected = result["original_language"]
        story.english_translation = result["english_translation"]
        story.hindi_translation = result["hindi_translation"]
        story.marathi_translation = result["marathi_translation"]
        story.category = result["category"]
        story.subcategory = result["subcategory"]
        story.state = result["state"]
        story.region = result["region"]
        story.keywords = result["keywords"]
        story.summary = result["summary"]
        story.processing_status = "completed"
        story.processing_error = None
    except AIProcessingError as e:
        story.processing_status = "failed"
        story.processing_error = str(e)

    db.commit()
    db.refresh(story)
    return story_to_out(story)


@app.get("/api/stories", response_model=list[schemas.StoryOut])
def list_stories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    stories = (
        db.query(models.Story)
        .filter(models.Story.user_id == current_user.id)
        .order_by(models.Story.created_at.desc())
        .all()
    )
    return [story_to_out(s) for s in stories]


@app.get("/api/stories/{story_id}", response_model=schemas.StoryOut)
def get_story(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    story = db.get(models.Story, story_id)
    if not story or story.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Story not found")
    return story_to_out(story)


@app.delete("/api/stories/{story_id}")
def delete_story(
    story_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    story = db.get(models.Story, story_id)
    if not story or story.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Story not found")
    for path in (story.audio_path, story.photo_path):
        if path:
            full = os.path.join(UPLOAD_DIR, path)
            if os.path.exists(full):
                os.remove(full)
    db.delete(story)
    db.commit()
    return {"deleted": True}
