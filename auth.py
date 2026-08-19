"""
Authentication helpers.

Three jobs live here:
  1. Password hashing (bcrypt via passlib) — never store plain text.
  2. JWT creation/verification — a signed token proves "this request
     is from user X" without the server keeping session state.
  3. get_current_user — a FastAPI dependency that protected endpoints
     add as a parameter; it reads the "Authorization: Bearer <token>"
     header, verifies it, and hands back the matching User row (or
     raises 401 if anything is wrong).

Nothing here is Ask-Ajji-specific — it only depends on database.py
and models.py, so main.py just imports what it needs.
"""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
import models

# --- config -----------------------------------------------------------
# JWT_SECRET signs tokens so they can't be forged or edited client-side.
# Set a real value in .env for anything beyond local dev; this fallback
# only exists so the app doesn't crash if someone forgets to set it.
JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-insecure-secret-change-me")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days — fine for a hackathon demo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Tells FastAPI/Swagger where to send the login form and how to read
# the resulting token back out of the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- password hashing ---------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


# --- JWT ------------------------------------------------------------
def create_access_token(subject: str) -> str:
    """subject is the user id (as a string) — the thing the token vouches for."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    """Returns the user id encoded in the token, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# --- FastAPI dependency ---------------------------------------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    """
    Add `user: models.User = Depends(get_current_user)` to any endpoint
    to require login — FastAPI runs this first, and the endpoint only
    executes if it returns a valid user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception
    user = db.get(models.User, int(user_id))
    if user is None:
        raise credentials_exception
    return user
