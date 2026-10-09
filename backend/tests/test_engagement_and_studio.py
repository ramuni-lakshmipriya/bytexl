import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def get_demo_creator_cookie():
    res = client.post("/auth/login/demo", json={"role": "creator"})
    assert res.status_code == 200
    return res.cookies

def get_demo_brand_cookie():
    res = client.post("/auth/login/demo", json={"role": "brand"})
    assert res.status_code == 200
    return res.cookies

def test_creator_profile_update():
    cookies = get_demo_creator_cookie()
    payload = {
        "headline": "Lead AI Filmmaker & Generative Prompt Specialist",
        "bio": "Specializing in photorealistic commercial spots with Midjourney and Runway Gen-3.",
        "rate_min_inr": 20000,
        "rate_max_inr": 60000,
        "availability": "available",
        "location": "Bangalore, India",
        "languages": ["English", "Hindi"],
        "tools": ["Midjourney", "Runway Gen-3", "ElevenLabs"],
        "skills": ["AI Film Direction", "Prompt Styling"]
    }
    res = client.put("/creators/me", json=payload, cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    assert data["headline"] == payload["headline"]
    assert data["rate_min_inr"] == 20000

def test_portfolio_crud():
    cookies = get_demo_creator_cookie()
    
    # 1. Create Portfolio Item
    create_payload = {
        "title": "Automotive AI Commercial Spec",
        "media_type": "video",
        "duration_sec": 30,
        "aspect_ratio": "16:9",
        "workflow": "Midjourney v6 -> Runway Gen-3 -> DaVinci Resolve",
        "process_notes": "Prompt: Sleek electric sports car accelerating on wet neon highway, 8k resolution cinematic camera move",
        "commercial_use": "cleared",
        "year": 2026
    }
    res = client.post("/creators/me/portfolio", json=create_payload, cookies=cookies)
    assert res.status_code == 201
    item = res.json()
    item_id = item["id"]
    assert item["title"] == create_payload["title"]

    # 2. Update Portfolio Item
    update_payload = {
        "title": "Automotive AI Commercial Spec (4K Final)",
        "duration_sec": 45
    }
    res_up = client.put(f"/creators/me/portfolio/{item_id}", json=update_payload, cookies=cookies)
    assert res_up.status_code == 200
    updated_item = res_up.json()
    assert updated_item["title"] == update_payload["title"]

    # 3. Delete Portfolio Item
    res_del = client.delete(f"/creators/me/portfolio/{item_id}", cookies=cookies)
    assert res_del.status_code == 200

def test_starter_studio_project_saving():
    cookies = get_demo_creator_cookie()
    payload = {
        "title": "Cinematic AI Microfilm",
        "project_type": "Microfilm / Sci-Fi",
        "notes": "Target duration 60s with ElevenLabs voiceover"
    }
    res = client.post("/creators/me/studio-projects", json=payload, cookies=cookies)
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == payload["title"]
    assert data["status"] in ["in_progress", "completed"]

def test_brief_application_and_delivery_flow():
    creator_cookies = get_demo_creator_cookie()
    brand_cookies = get_demo_brand_cookie()

    # Fetch open briefs
    briefs_res = client.get("/briefs?status=open")
    assert briefs_res.status_code == 200
    briefs = briefs_res.json()
    assert len(briefs) > 0
    target_brief_id = briefs[0]["id"]

    # 1. Creator applies to brief
    app_payload = {
        "pitch": "I will deliver high-end 4K video clips using Midjourney v6 and Runway Gen-3 in 4 days.",
        "proposed_rate_inr": 25000,
        "estimated_days": 4
    }
    res_app = client.post(f"/briefs/{target_brief_id}/apply", json=app_payload, cookies=creator_cookies)
    assert res_app.status_code in [201, 400] # 400 if already applied in previous run

    if res_app.status_code == 201:
        app_data = res_app.json()
        app_id = app_data["id"]

        # 2. Brand reviews applicants
        res_apps = client.get(f"/briefs/{target_brief_id}/applications", cookies=brand_cookies)
        assert res_apps.status_code == 200

        # 3. Brand accepts applicant
        res_accept = client.put(f"/briefs/applications/{app_id}", json={"status": "accepted"}, cookies=brand_cookies)
        assert res_accept.status_code == 200
        assert res_accept.json()["status"] == "accepted"

        # 4. Creator submits delivery
        del_payload = {
            "delivery_url": "https://vimeo.com/gencraft-demo-delivery-12345",
            "delivery_notes": "4K master files and stems included."
        }
        res_del = client.post(f"/briefs/applications/{app_id}/deliver", json=del_payload, cookies=creator_cookies)
        assert res_del.status_code == 200
        assert res_del.json()["status"] == "delivered"

def test_no_match_filter_case():
    res = client.get("/creators?search=ZeroMatchTestQueryXyz99")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 0
    assert len(data["creators"]) == 0
