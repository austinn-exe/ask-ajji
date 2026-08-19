"""
Gemini-powered AI preservation pipeline.

Takes one saved audio file and turns it into everything a Story row
needs: transcript, three translations, and a classification (category /
subcategory / state / region / keywords / summary) — in a single
Gemini request, so a hackathon-scale free-tier key is enough.

Public surface (this is all main.py touches):
    transcribe_and_analyze_audio(audio_path) -> dict
    AIProcessingError

Everything else here is an implementation detail.
"""
import concurrent.futures
import json
import mimetypes
import os

from google import genai
from google.genai import types

# Hard ceiling on the whole Gemini round-trip. Without this, a blocked/
# unreachable network (bad DNS, firewalled egress, etc.) can hang the
# request indefinitely instead of failing the story gracefully. Override
# with GEMINI_TIMEOUT_SECONDS for local tuning.
REQUEST_TIMEOUT_SECONDS = float(os.getenv("GEMINI_TIMEOUT_SECONDS", "45"))

# Must match seed_data.py's category strings exactly — a completed
# Story's `category` is one of these, and /api/stats/cultural groups
# CulturalEntry + Story together by that exact string.
CATEGORIES = [
    "Food & Recipes",
    "Clothing & Draping",
    "Folk Music & Songs",
    "Rituals & Traditions",
    "Festivals",
    "Traditional Practices",
    "Languages, Proverbs & Stories",
    "Games & Crafts",
]

MODEL_NAME = "gemini-2.5-flash"

_PROMPT = f"""You are helping preserve an Indian family's oral cultural heritage.
You will be given one short audio recording of a person (often an elder)
describing a recipe, a tradition, a song, a game, a piece of clothing, a
remedy, a proverb, or a memory/story.

Listen to the audio and respond with ONLY a single JSON object (no markdown
fences, no commentary) with exactly these keys:

- "original_language": the language the speaker used (e.g. "Marathi", "Hindi", "English").
- "original_transcript": a faithful transcript of the speech, in its original language and script.
- "english_translation": an English translation of the transcript.
- "hindi_translation": a Hindi translation of the transcript (Devanagari script).
- "marathi_translation": a Marathi translation of the transcript (Devanagari script).
- "category": exactly one of {json.dumps(CATEGORIES, ensure_ascii=False)}.
- "subcategory": a short, more specific label (e.g. "Sweets", "Street Food", "Lullaby"), or null if unclear.
- "state": the Indian state or union territory this tradition is most associated with, if it can be inferred from the recording; otherwise null.
- "region": a broader region such as "Western India", "South India", "North-East India", or null if unclear.
- "keywords": a short JSON array of 3-6 lowercase keyword strings.
- "summary": a 1-3 sentence English summary of what the recording describes.

If a field truly cannot be determined from the audio, use null (for strings)
or an empty array (for keywords) rather than guessing wildly. Keep translations
faithful to the meaning rather than literal word-for-word."""


class AIProcessingError(Exception):
    """Raised whenever the audio couldn't be transcribed/classified.

    main.py catches this specifically: the Story row and the original
    audio are always kept, only processing_status/processing_error change.
    """


def _get_client() -> "genai.Client":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() in ("", "your-gemini-api-key-here"):
        raise AIProcessingError(
            "GEMINI_API_KEY is not set — add a free-tier key from "
            "https://aistudio.google.com/apikey to your .env file."
        )
    return genai.Client(api_key=api_key)


def _guess_mime_type(audio_path: str) -> str:
    mime_type, _ = mimetypes.guess_type(audio_path)
    if mime_type:
        return mime_type
    # MediaRecorder in the browser produces webm with no reliable
    # extension guess on some systems — default to something Gemini
    # accepts rather than failing the whole request over a MIME guess.
    return "audio/webm"


def _extract_json(raw_text: str) -> dict:
    text = (raw_text or "").strip()
    # Defensive: strip ```json ... ``` fences if the model adds them
    # despite being asked for raw JSON.
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise AIProcessingError(f"Gemini returned non-JSON output: {e}") from e


def transcribe_and_analyze_audio(audio_path: str) -> dict:
    """
    Reads the audio file at audio_path, sends it to Gemini once, and
    returns a dict with the keys create_story() expects:
        original_transcript, original_language, english_translation,
        hindi_translation, marathi_translation, category, subcategory,
        state, region, keywords, summary
    Raises AIProcessingError on any failure (missing key, network error,
    bad/unparseable response, etc.) — callers should catch that and mark
    the story as failed rather than losing it.
    """
    if not os.path.exists(audio_path):
        raise AIProcessingError(f"Audio file not found on disk: {audio_path}")

    client = _get_client()

    try:
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
    except OSError as e:
        raise AIProcessingError(f"Could not read audio file: {e}") from e

    if not audio_bytes:
        raise AIProcessingError("Audio file is empty — nothing to transcribe.")

    mime_type = _guess_mime_type(audio_path)

    def _call():
        return client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                types.Part.from_bytes(data=audio_bytes, mime_type=mime_type),
                _PROMPT,
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )

    try:
        # Run in a worker thread so a hung connection can't block the
        # request past REQUEST_TIMEOUT_SECONDS, regardless of whether the
        # installed SDK version honors its own internal timeout options.
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
            response = pool.submit(_call).result(timeout=REQUEST_TIMEOUT_SECONDS)
    except concurrent.futures.TimeoutError as e:
        raise AIProcessingError(
            f"Gemini request timed out after {REQUEST_TIMEOUT_SECONDS:.0f}s — "
            "check your network connection and GEMINI_API_KEY."
        ) from e
    except Exception as e:  # noqa: BLE001 — SDK can raise several exception types
        raise AIProcessingError(f"Gemini request failed: {e}") from e

    raw_text = getattr(response, "text", None)
    if not raw_text:
        raise AIProcessingError("Gemini returned an empty response.")

    data = _extract_json(raw_text)

    category = data.get("category")
    if category not in CATEGORIES:
        # Don't hard-fail the whole story over a slightly-off category —
        # fall back to the closest safe bucket so stats/filters don't break.
        category = "Languages, Proverbs & Stories"

    keywords = data.get("keywords") or []
    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    return {
        "original_transcript": data.get("original_transcript") or "",
        "original_language": data.get("original_language"),
        "english_translation": data.get("english_translation"),
        "hindi_translation": data.get("hindi_translation"),
        "marathi_translation": data.get("marathi_translation"),
        "category": category,
        "subcategory": data.get("subcategory"),
        "state": data.get("state"),
        "region": data.get("region"),
        "keywords": [str(k) for k in keywords][:8],
        "summary": data.get("summary") or "",
    }