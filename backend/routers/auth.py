import uuid
import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Request, Response, status, Query
from fastapi.responses import RedirectResponse
from backend.database import get_db
from backend.schemas import (
    UserOut, LoginRequest, DemoLoginRequest,
    CreatorSignupRequest, BrandSignupRequest, AuthConfigStatus
)
from backend.services.auth import (
    hash_password, verify_password, create_jwt_token,
    get_current_user, get_current_user_optional,
    check_rate_limit, record_login_attempt, SESSION_COOKIE_NAME
)
from backend.services.oauth import (
    get_oauth_config_status, get_authorization_url,
    parse_oauth_state, exchange_code_for_user_info,
    FRONTEND_URL
)

router = APIRouter(prefix="/auth", tags=["auth"])

def set_session_cookie(response: Response, user_id: str, role: str):
    token = create_jwt_token(user_id, role)
    # Set httpOnly cookie, 7 days expiration
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Set True in production with HTTPS
        max_age=7 * 24 * 3600
    )

@router.get("/config-status", response_model=AuthConfigStatus)
def auth_config_status():
    return AuthConfigStatus(**get_oauth_config_status())

@router.post("/login", response_model=UserOut)
def login(req: LoginRequest, request: Request, response: Response):
    client_ip = request.client.host if request.client else "127.0.0.1"
    check_rate_limit(client_ip)

    email = req.email.strip().lower()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not user["password_hash"] or not verify_password(req.password, user["password_hash"]):
        record_login_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password"
        )

    set_session_cookie(response, user["id"], user["role"])
    return UserOut(**dict(user))

@router.post("/login/demo", response_model=UserOut)
def login_demo(req: DemoLoginRequest, response: Response):
    conn = get_db()
    cursor = conn.cursor()

    target_email = "demo.creator@gencraft.demo" if req.role == "creator" else "demo.brand@gencraft.demo"
    cursor.execute("SELECT * FROM users WHERE email = ?", (target_email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=500, detail="Demo user account missing in database.")

    set_session_cookie(response, user["id"], user["role"])
    return UserOut(**dict(user))

@router.post("/signup/creator", response_model=UserOut, status_code=201)
def signup_creator(req: CreatorSignupRequest, response: Response):
    if not req.accept_terms:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions to sign up.")

    email = req.email.strip().lower()
    conn = get_db()
    cursor = conn.cursor()

    # Check duplicate email
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        if existing["role"] == "brand":
            raise HTTPException(
                status_code=400,
                detail="This email is already registered under a Brand account. Cannot sign up as Creator."
            )
        raise HTTPException(
            status_code=400,
            detail="Account with this email already exists. Please log in."
        )

    # 1. Create Creator row
    new_creator_id = f"cr_u_{uuid.uuid4().hex[:8]}"
    avatar = f"https://picsum.photos/seed/{new_creator_id}/200"

    cursor.execute("""
        INSERT INTO creators (
            id, name, headline, bio, location, avatar_url, specialization,
            experience_level, rate_min_inr, rate_max_inr, availability,
            languages, tools_verified, workflow_documented, past_work_linked
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'junior', 15000, 45000, 'available', 'English', 0, 0, 0)
    """, (
        new_creator_id, req.full_name.strip(),
        f"{req.specialization} specialist",
        f"Hi, I am {req.full_name.strip()}, a passionate AI creator specializing in {req.specialization}.",
        req.location or "Remote", avatar, req.specialization
    ))

    # Link selected tools
    for tool_name in req.tools:
        cursor.execute("SELECT id FROM tools WHERE name = ? OR CAST(id AS TEXT) = ?", (tool_name, tool_name))
        tool_row = cursor.fetchone()
        if tool_row:
            cursor.execute("INSERT OR IGNORE INTO creator_tools VALUES (?, ?)", (new_creator_id, tool_row["id"]))

    # 2. Create User row
    new_user_id = f"usr_{uuid.uuid4().hex[:8]}"
    pass_hash = hash_password(req.password)

    cursor.execute("""
        INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
        VALUES (?, ?, ?, 'creator', ?, NULL, ?, ?)
    """, (new_user_id, email, pass_hash, new_creator_id, req.full_name.strip(), avatar))

    conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (new_user_id,))
    user = cursor.fetchone()
    conn.close()

    set_session_cookie(response, user["id"], "creator")
    return UserOut(**dict(user))

@router.post("/signup/brand", response_model=UserOut, status_code=201)
def signup_brand(req: BrandSignupRequest, response: Response):
    if not req.accept_terms:
        raise HTTPException(status_code=400, detail="You must accept the terms and conditions to sign up.")

    email = req.work_email.strip().lower()
    conn = get_db()
    cursor = conn.cursor()

    # Check duplicate email
    cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        if existing["role"] == "creator":
            raise HTTPException(
                status_code=400,
                detail="This email is already registered under a Creator account. Cannot sign up as Brand."
            )
        raise HTTPException(
            status_code=400,
            detail="Account with this email already exists. Please log in."
        )

    # 1. Create Brand row
    new_brand_id = f"br_u_{uuid.uuid4().hex[:8]}"
    logo = f"https://api.dicebear.com/7.x/initials/svg?seed={req.company_name.replace(' ', '')}"

    cursor.execute("""
        INSERT INTO brands (id, name, industry, description, logo_url, is_agency)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        new_brand_id, req.company_name.strip(), req.industry or "Creative Agency",
        f"Brand account for {req.company_name.strip()}", logo, 1 if req.is_agency else 0
    ))

    # 2. Create User row
    new_user_id = f"usr_{uuid.uuid4().hex[:8]}"
    pass_hash = hash_password(req.password)

    cursor.execute("""
        INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
        VALUES (?, ?, ?, 'brand', NULL, ?, ?, ?)
    """, (new_user_id, email, pass_hash, new_brand_id, req.contact_name.strip(), logo))

    conn.commit()

    cursor.execute("SELECT * FROM users WHERE id = ?", (new_user_id,))
    user = cursor.fetchone()
    conn.close()

    set_session_cookie(response, user["id"], "brand")
    return UserOut(**dict(user))

@router.get("/me", response_model=UserOut)
def get_me(request: Request):
    user = get_current_user(request)
    return UserOut(**user)

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=SESSION_COOKIE_NAME, httponly=True, samesite="lax")
    return {"status": "ok", "message": "Logged out successfully"}

@router.get("/{provider}/start")
def oauth_start(provider: str, role: str = Query("creator", pattern="^(creator|brand)$")):
    if provider not in ["google", "facebook", "instagram"]:
        raise HTTPException(status_code=400, detail="Unsupported OAuth provider")
    auth_url = get_authorization_url(provider, role)
    return RedirectResponse(url=auth_url)

@router.get("/{provider}/callback")
def oauth_callback(provider: str, code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
    if error or not code:
        if provider == "instagram":
            return RedirectResponse(url=f"{FRONTEND_URL}/login?oauth_error=instagram_test_mode")
        return RedirectResponse(url=f"{FRONTEND_URL}/login?oauth_error=cancelled")

    parsed_state = parse_oauth_state(state) if state else None
    role = parsed_state.get("role", "creator") if parsed_state else "creator"

    user_info = exchange_code_for_user_info(provider, code)
    if not user_info:
        if provider == "instagram":
            return RedirectResponse(url=f"{FRONTEND_URL}/login?oauth_error=instagram_test_mode")
        return RedirectResponse(url=f"{FRONTEND_URL}/login?oauth_error=exchange_failed")

    email = user_info.get("email", "").lower()
    provider_user_id = user_info["provider_user_id"]
    display_name = user_info.get("display_name", "OAuth User")
    avatar_url = user_info.get("avatar_url") or f"https://picsum.photos/seed/{provider_user_id}/200"

    conn = get_db()
    cursor = conn.cursor()

    # 1. Check if OAuth account linked
    cursor.execute("""
        SELECT u.* FROM users u
        JOIN oauth_accounts oa ON u.id = oa.user_id
        WHERE oa.provider = ? AND oa.provider_user_id = ?
    """, (provider, provider_user_id))
    user = cursor.fetchone()

    if not user and email:
        # 2. Check if user with same email exists
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = ?", (email,))
        user = cursor.fetchone()

    if user:
        # Check role mismatch
        if user["role"] != role:
            conn.close()
            return RedirectResponse(
                url=f"{FRONTEND_URL}/{role}/signup?oauth_error=role_mismatch&existing_role={user['role']}"
            )
        target_user_id = user["id"]
    else:
        # 3. First-time OAuth signup -> Create user + creator/brand
        target_user_id = f"usr_oa_{uuid.uuid4().hex[:8]}"

        if role == "creator":
            c_id = f"cr_oa_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT INTO creators (id, name, headline, bio, location, avatar_url, specialization, experience_level, rate_min_inr, rate_max_inr, availability)
                VALUES (?, ?, 'Generative AI Creator', 'AI video creator joining via OAuth.', 'Remote', ?, 'AI Filmmaker', 'junior', 15000, 45000, 'available')
            """, (c_id, display_name, avatar_url))

            cursor.execute("""
                INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
                VALUES (?, ?, NULL, 'creator', ?, NULL, ?, ?)
            """, (target_user_id, email or f"{provider_user_id}@{provider}.user", c_id, display_name, avatar_url))
        else:
            b_id = f"br_oa_{uuid.uuid4().hex[:8]}"
            cursor.execute("""
                INSERT INTO brands (id, name, industry, description, logo_url, is_agency)
                VALUES (?, ?, 'Creative Agency', 'Brand profile created via OAuth', ?, 0)
            """, (b_id, display_name, avatar_url))

            cursor.execute("""
                INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
                VALUES (?, ?, NULL, 'brand', NULL, ?, ?, ?)
            """, (target_user_id, email or f"{provider_user_id}@{provider}.user", b_id, display_name, avatar_url))

    # Link OAuth account record
    cursor.execute("""
        INSERT OR IGNORE INTO oauth_accounts (id, user_id, provider, provider_user_id, email)
        VALUES (?, ?, ?, ?, ?)
    """, (f"oa_{uuid.uuid4().hex[:8]}", target_user_id, provider, provider_user_id, email))

    conn.commit()
    conn.close()

    # Create session response
    token = create_jwt_token(target_user_id, role)
    response = RedirectResponse(url=f"{FRONTEND_URL}/dashboard")
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=7 * 24 * 3600
    )
    return response
