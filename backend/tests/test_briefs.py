from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_create_brief_validation():
    # Login as brand user first
    login_res = client.post("/auth/login/demo", json={"role": "brand"})
    cookie = login_res.cookies["gencraft_session"]

    # Valid brief
    valid_payload = {
        "title": "Test AI Reel Campaign",
        "campaign_goal": "Drive brand engagement",
        "description": "Short 15-second product reel",
        "content_type_id": 1,
        "style": "Modern",
        "aspect_ratio": "9:16",
        "duration_sec": 15,
        "deliverables_count": 2,
        "budget_min_inr": 20000,
        "budget_max_inr": 40000,
        "commercial_use": "full_buyout",
        "usage_region": "India",
        "required_tool_ids": [1, 2],
        "required_skill_ids": [1, 3]
    }
    res = client.post("/briefs", json=valid_payload, cookies={"gencraft_session": cookie})
    assert res.status_code == 201
    data = res.json()
    assert data["title"] == valid_payload["title"]
    assert len(data["required_tools"]) == 2

    # Invalid aspect ratio
    invalid_aspect = valid_payload.copy()
    invalid_aspect["aspect_ratio"] = "21:9"
    res_bad = client.post("/briefs", json=invalid_aspect, cookies={"gencraft_session": cookie})
    assert res_bad.status_code == 400

    # Invalid budget range
    invalid_budget = valid_payload.copy()
    invalid_budget["budget_min_inr"] = 50000
    invalid_budget["budget_max_inr"] = 20000
    res_budget = client.post("/briefs", json=invalid_budget, cookies={"gencraft_session": cookie})
    assert res_budget.status_code == 400

def test_brief_draft_fallback():
    res = client.post("/briefs/draft", json={"prompt": "I need a 15s TikTok reel using Midjourney and Runway for a sneaker brand with 30000 budget"})
    assert res.status_code == 200
    data = res.json()
    assert data["aspect_ratio"] == "9:16"
    assert data["duration_sec"] == 15
    assert len(data["required_tool_ids"]) >= 1
