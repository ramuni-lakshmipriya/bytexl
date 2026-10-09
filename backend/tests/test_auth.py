from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_demo_logins():
    # Demo Creator Login
    res_cr = client.post("/auth/login/demo", json={"role": "creator"})
    assert res_cr.status_code == 200
    data_cr = res_cr.json()
    assert data_cr["role"] == "creator"
    assert data_cr["email"] == "demo.creator@gencraft.demo"
    assert "gencraft_session" in res_cr.cookies

    # Demo Brand Login
    res_br = client.post("/auth/login/demo", json={"role": "brand"})
    assert res_br.status_code == 200
    data_br = res_br.json()
    assert data_br["role"] == "brand"
    assert data_br["email"] == "demo.brand@gencraft.demo"
    assert "gencraft_session" in res_br.cookies

def test_password_login_success_and_failure():
    # Valid login for demo creator
    res_ok = client.post("/auth/login", json={
        "email": "demo.creator@gencraft.demo",
        "password": "DemoCreator123!"
    })
    assert res_ok.status_code == 200
    assert res_ok.json()["role"] == "creator"

    # Invalid password -> 400 with generic error
    res_bad = client.post("/auth/login", json={
        "email": "demo.creator@gencraft.demo",
        "password": "WrongPassword123!"
    })
    assert res_bad.status_code == 400
    assert res_bad.json()["detail"] == "Invalid email or password"

import uuid

def test_signup_creator_and_brand():
    # Signup new creator
    uid = uuid.uuid4().hex[:6]
    c_email = f"test.creator.{uid}@gencraft.demo"
    res_c_signup = client.post("/auth/signup/creator", json={
        "full_name": "Test New Creator",
        "email": c_email,
        "password": "Password123!",
        "specialization": "AI Filmmaker",
        "tools": ["Midjourney", "Runway"],
        "location": "Mumbai, IN",
        "accept_terms": True
    })
    assert res_c_signup.status_code == 201
    assert res_c_signup.json()["role"] == "creator"
    assert res_c_signup.json()["creator_id"] is not None

    # Signup new brand
    b_email = f"test.brand.{uid}@gencraft.demo"
    res_b_signup = client.post("/auth/signup/brand", json={
        "contact_name": "Test Brand Admin",
        "work_email": b_email,
        "password": "Password123!",
        "company_name": "Test Brand Agency",
        "industry": "Marketing",
        "is_agency": True,
        "accept_terms": True
    })
    assert res_b_signup.status_code == 201
    assert res_b_signup.json()["role"] == "brand"
    assert res_b_signup.json()["brand_id"] is not None

def test_duplicate_email_prevention():
    # Try signing up creator with an existing brand email
    res_dup = client.post("/auth/signup/creator", json={
        "full_name": "Duplicate User",
        "email": "demo.brand@gencraft.demo",
        "password": "Password123!",
        "specialization": "AI Animator",
        "accept_terms": True
    })
    assert res_dup.status_code == 400
    assert "already registered under a Brand account" in res_dup.json()["detail"]

def test_authorization_wrong_role_brief_posting():
    # Login as Creator
    login_res = client.post("/auth/login/demo", json={"role": "creator"})
    cookie = login_res.cookies["gencraft_session"]

    # Creator attempts to POST /briefs -> Should get 403 Forbidden
    brief_payload = {
        "title": "Unauthorized Brief",
        "content_type_id": 1,
        "aspect_ratio": "16:9",
        "commercial_use": "full_buyout"
    }
    res = client.post("/briefs", json=brief_payload, cookies={"gencraft_session": cookie})
    assert res.status_code == 403
    assert "requires a 'brand' account" in res.json()["detail"]

def test_brand_authorized_brief_posting():
    # Login as Brand
    login_res = client.post("/auth/login/demo", json={"role": "brand"})
    cookie = login_res.cookies["gencraft_session"]

    # Brand attempts to POST /briefs -> Should succeed 201 Created
    brief_payload = {
        "title": "Authorized Brand Campaign Brief",
        "content_type_id": 1,
        "aspect_ratio": "16:9",
        "duration_sec": 30,
        "budget_min_inr": 20000,
        "budget_max_inr": 60000,
        "commercial_use": "full_buyout"
    }
    res = client.post("/briefs", json=brief_payload, cookies={"gencraft_session": cookie})
    assert res.status_code == 201
    data = res.json()
    assert data["brand_id"] == "br_01"  # Derived from logged-in brand
