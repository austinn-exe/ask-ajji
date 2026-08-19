from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """
    A registered contributor. Passwords are never stored directly —
    only password_hash (a bcrypt hash, set in auth.py's hash_password).
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stories = relationship("Story", back_populates="user")


class CulturalEntry(Base):
    """
    One item of documented traditional knowledge — a dish, a garment,
    a ritual, a game, a song, etc. `domain` is one of the 8 top-level
    categories the frontend's category strip shows; `steps` holds the
    ordered how-it's-done list shown in the detail modal.
    """
    __tablename__ = "cultural_entries"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(64), index=True, nullable=False)     # e.g. "Food & Recipes"
    subcategory = Column(String(120), nullable=True)             # e.g. "Sweets"
    state = Column(String(64), index=True, nullable=False)       # e.g. "Maharashtra"
    region = Column(String(64), nullable=True)                   # e.g. "Western India"
    language = Column(String(64), nullable=True)                 # e.g. "Marathi"
    name = Column(String(160), nullable=False)
    gender = Column(String(16), nullable=True)                   # Women | Men | null
    description = Column(Text, nullable=False)
    why_it_matters = Column(Text, nullable=False)
    steps = Column(JSON, nullable=False, default=list)            # ordered list[str]
    image_url = Column(String(500), nullable=True)
    source_url = Column(String(500), nullable=True)


class Festival(Base):
    __tablename__ = "festivals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(160), nullable=False)
    month = Column(String(8), nullable=False)   # e.g. "AUG"
    day = Column(String(4), nullable=False)     # e.g. "22"
    description = Column(Text, nullable=False)


class Proverb(Base):
    __tablename__ = "proverbs"

    id = Column(Integer, primary_key=True, index=True)
    text_original = Column(String(300), nullable=False)   # Devanagari / native script
    language = Column(String(32), nullable=False)          # e.g. "Marathi"
    transliteration = Column(String(300), nullable=False)
    meaning = Column(String(300), nullable=False)


class Story(Base):
    """
    A contributor's preserved piece of heritage — the output of the
    Preserve flow (record/upload audio, optional photo). Belongs to
    the user who submitted it (user_id). transcript/translation/
    category/keywords/summary are filled in by the Gemini pipeline
    in ai_pipeline.py; processing_status tracks whether that step
    has finished, is running, or failed.
    """
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(200), nullable=False)
    category = Column(String(64), nullable=True)      # filled by AI, or set manually
    subcategory = Column(String(120), nullable=True)
    state = Column(String(64), nullable=True)
    region = Column(String(64), nullable=True)
    contributor_name = Column(String(120), nullable=True)

    audio_path = Column(String(300), nullable=False)     # served from /uploads/...
    photo_path = Column(String(300), nullable=True)

    original_transcript = Column(Text, nullable=True)
    language_detected = Column(String(64), nullable=True)
    english_translation = Column(Text, nullable=True)
    hindi_translation = Column(Text, nullable=True)
    marathi_translation = Column(Text, nullable=True)
    keywords = Column(JSON, nullable=True, default=list)   # list[str]
    summary = Column(Text, nullable=True)

    processing_status = Column(String(16), nullable=False, default="processing")
    # one of: "processing" | "completed" | "failed"
    processing_error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="stories")
