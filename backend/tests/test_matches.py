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
