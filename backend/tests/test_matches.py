from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_brief_matches():
    # Fetch briefs first
    res_briefs = client.get("/briefs")
    assert res_briefs.status_code == 200
    briefs = res_briefs.json()
    assert len(briefs) > 0
    brief_id = briefs[0]["id"]

    # Fetch matches for this brief
    res_matches = client.get(f"/briefs/{brief_id}/matches")
    assert res_matches.status_code == 200
    matches = res_matches.json()
    assert len(matches) > 0

    # Ensure match scores are 0..100 and descending sorted
    scores = [m["match_score"] for m in matches]
    for score in scores:
        assert 0 <= score <= 100
    assert scores == sorted(scores, reverse=True)

    # Check structure of top match
    top_match = matches[0]
    assert "creator" in top_match
    assert "score_breakdown" in top_match
    assert "match_reason" in top_match
    assert len(top_match["match_reason"]) > 0

def test_compute_creator_match_mathematical_edge_cases():
    from backend.services.matcher import compute_creator_match

    dummy_creator = {
        "id": "cr_test",
        "name": "Test Creator",
        "specialization": "AI Filmmaker",
        "rate_min_inr": 10000,
        "rate_max_inr": 30000,
        "availability": "available",
        "tools_verified": 1,
        "workflow_documented": 1,
        "past_work_linked": 1,
        "tools": [{"id": 1, "name": "Midjourney"}, {"id": 2, "name": "Runway"}],
        "skills": [{"id": 10, "name": "AI Film Direction"}],
        "content_types": [{"id": 100, "name": "Video Commercial"}]
    }

    # Case 1: Brief with NO tools or skills specified (Zero Requirements Case)
    empty_brief = {
        "content_type_id": 100,
        "required_tool_ids": [],
        "required_skill_ids": [],
        "budget_min_inr": 10000,
        "budget_max_inr": 30000
    }
    match1 = compute_creator_match(dummy_creator, empty_brief)
    # Should get full 30 for tools, 30 for skills, 15 for content_type, 15 for budget, 5 for avail, 5 for verif = 100%
    assert match1["match_score"] == 100
    assert match1["score_breakdown"]["tool_score"] == 30.0
    assert match1["score_breakdown"]["skill_score"] == 30.0

    # Case 2: Brief with un-matched tools
    no_match_brief = {
        "content_type_id": 999,
        "required_tool_ids": [991, 992],
        "required_skill_ids": [993],
        "budget_min_inr": 500000,
        "budget_max_inr": 1000000
    }
    match2 = compute_creator_match(dummy_creator, no_match_brief)
    assert match2["score_breakdown"]["tool_score"] == 0.0
    assert match2["score_breakdown"]["skill_score"] == 0.0
    assert match2["score_breakdown"]["content_type_score"] == 0.0

