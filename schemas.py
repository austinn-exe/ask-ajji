from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---------- Auth / Users ----------

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Cultural entries ----------

class CulturalEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    domain: str
    subcategory: Optional[str] = None
    state: str
    region: Optional[str] = None
    language: Optional[str] = None
    name: str
    gender: Optional[str] = None
    description: str
    why_it_matters: str
    steps: list[str]
    image_url: Optional[str] = None
    source_url: Optional[str] = None


class DomainOut(BaseModel):
    id: str
    icon: str
    color: str


# ---------- Festivals & proverbs ----------

class FestivalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    month: str
    day: str
    description: str


class ProverbOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text_original: str
    language: str
    transliteration: str
    meaning: str


# ---------- Preserved stories ----------

class StoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    title: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    state: Optional[str] = None
    region: Optional[str] = None
    contributor_name: Optional[str] = None
    audio_url: Optional[str] = None  # set by story_to_out() after validation, not a DB column
    photo_url: Optional[str] = None
    original_transcript: Optional[str] = None
    language_detected: Optional[str] = None
    english_translation: Optional[str] = None
    hindi_translation: Optional[str] = None
    marathi_translation: Optional[str] = None
    keywords: Optional[list[str]] = None
    summary: Optional[str] = None
    processing_status: str
    processing_error: Optional[str] = None
    created_at: datetime
