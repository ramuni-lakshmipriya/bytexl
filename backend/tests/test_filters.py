from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_meta():
    response = client.get("/meta")
    assert response.status_code == 200
    data = response.json()
    assert "tools" in data
    assert "skills" in data
    assert "content_types" in data
    assert len(data["tools"]) >= 18
    assert len(data["skills"]) >= 20

def test_get_creators_all():
    response = client.get("/creators")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 20
    assert len(data["creators"]) == data["total"]

def test_creators_empty_result_sora_3d_modeling():
    """Test Sora + 3D modeling empty result case as mandated in requirements."""
    response = client.get("/creators?tools=Sora&skills=3D modeling")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert len(data["creators"]) == 0

def test_creators_tools_any_vs_all():
    # Any
    res_any = client.get("/creators?tools=Midjourney&tools=Runway&match_tools=any")
    assert res_any.status_code == 200
    total_any = res_any.json()["total"]

    # All
    res_all = client.get("/creators?tools=Midjourney&tools=Runway&match_tools=all")
    assert res_all.status_code == 200
    total_all = res_all.json()["total"]

    assert total_any >= total_all

def test_creators_sorting():
    res_rate = client.get("/creators?sort_by=rate_asc")
    assert res_rate.status_code == 200
    creators = res_rate.json()["creators"]
    rates = [c["rate_min_inr"] for c in creators if c["rate_min_inr"] is not None]
    assert rates == sorted(rates)
