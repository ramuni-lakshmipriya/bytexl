import os
import time
import jwt
from typing import Optional, Dict
from collections import defaultdict
from fastapi import Request, HTTPException, Security, status
from fastapi.security import APIKeyCookie
from passlib.context import CryptContext
from backend.database import get_db

JWT_SECRET = os.environ.get("JWT_SECRET", "gencraft_secret_key_hackathon_2026")
JWT_ALGORITHM = "HS256"
SESSION_COOKIE_NAME = "gencraft_session"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cookie_sec = APIKeyCookie(name=SESSION_COOKIE_NAME, auto_error=False)

# Basic Rate Limiting: max 5 login attempts per minute per IP
login_attempts: Dict[str, list] = defaultdict(list)

def check_rate_limit(ip: str, max_attempts: int = 5, window_sec: int = 60):
    now = time.time()
    # Filter attempts within window
    attempts = [t for t in login_attempts[ip] if now - t < window_sec]
    login_attempts[ip] = attempts

    if len(attempts) >= max_attempts:
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Please wait 1 minute before trying again."
        )

def record_login_attempt(ip: str):
    login_attempts[ip].append(time.time())

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + (7 * 24 * 3600)  # 7 days
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

def get_current_user_optional(request: Request) -> Optional[dict]:
    # 1. Check httpOnly cookie first
    token = request.cookies.get(SESSION_COOKIE_NAME)

    # 2. Check Authorization Header if cookie not present
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return None

    payload = decode_jwt_token(token)
    if not payload or "sub" not in payload:
        return None

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (payload["sub"],))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    return dict(user)

def get_current_user(request: Request) -> dict:
    user = get_current_user_optional(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in first."
        )
    return user

def require_role(role: str):
    def role_checker(request: Request) -> dict:
        user = get_current_user(request)
        if user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. This action requires a '{role}' account."
            )
        return user
    return role_checker
