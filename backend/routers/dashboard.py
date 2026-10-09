from fastapi import APIRouter, Depends, HTTPException, Request
from backend.database import get_db
from backend.services.auth import get_current_user
from backend.routers.creators import build_creator_dict
from backend.routers.briefs import fetch_brief_detail_by_id
from backend.services.matcher import compute_creator_match

router = APIRouter(prefix="", tags=["dashboard"])

def calculate_creator_completeness(creator_dict: dict) -> int:
    score = 20  # Base for signup
    if creator_dict.get("headline"): score += 10
    if creator_dict.get("bio") and len(creator_dict["bio"]) > 50: score += 15
    if creator_dict.get("tools") and len(creator_dict["tools"]) > 0: score += 15
    if creator_dict.get("skills") and len(creator_dict["skills"]) > 0: score += 15
    if creator_dict.get("portfolio_count", 0) > 0: score += 15
    if creator_dict.get("tools_verified") or creator_dict.get("workflow_documented"): score += 10
    return min(100, score)

@router.get("/dashboard")
def get_dashboard(request: Request, user: dict = Depends(get_current_user)):
    conn = get_db()
    cursor = conn.cursor()

    if user["role"] == "brand":
        b_id = user.get("brand_id")
        cursor.execute("SELECT * FROM brands WHERE id = ?", (b_id,))
        brand_row = cursor.fetchone()
        brand_dict = dict(brand_row) if brand_row else None

        # Fetch briefs posted by this brand
        cursor.execute("SELECT id FROM briefs WHERE brand_id = ? ORDER BY created_at DESC", (b_id,))
        b_rows = cursor.fetchall()
        
        my_briefs = []
        open_count = 0
        for r in b_rows:
            b_detail = fetch_brief_detail_by_id(r["id"], cursor)
            if b_detail:
                my_briefs.append(b_detail.model_dump())
                if b_detail.status == "open":
                    open_count += 1

        conn.close()

        return {
            "role": "brand",
            "user": user,
            "brand": brand_dict,
            "briefs": my_briefs,
            "stats": {
                "total_briefs": len(my_briefs),
                "open_briefs": open_count
            }
        }

    else: # creator
        c_id = user.get("creator_id")
        cursor.execute("SELECT * FROM creators WHERE id = ?", (c_id,))
        cr_row = cursor.fetchone()
        if not cr_row:
            conn.close()
            raise HTTPException(status_code=404, detail="Creator profile not found")

        creator_summary = build_creator_dict(cr_row, cursor)
        cr_dict = creator_summary.model_dump()
        completeness = calculate_creator_completeness(cr_dict)

        # Fetch open briefs and score matches for this creator
        cursor.execute("SELECT id FROM briefs WHERE status = 'open' ORDER BY created_at DESC")
        brief_rows = cursor.fetchall()

        matching_briefs = []
        for r in brief_rows:
            b_detail = fetch_brief_detail_by_id(r["id"], cursor)
            if b_detail:
                brief_dict = {
                    "content_type_id": b_detail.content_type_id,
                    "required_tool_ids": [t.id for t in b_detail.required_tools],
                    "required_skill_ids": [s.id for s in b_detail.required_skills],
                    "budget_min_inr": b_detail.budget_min_inr,
                    "budget_max_inr": b_detail.budget_max_inr
                }
                match_info = compute_creator_match(cr_dict, brief_dict)
                if match_info["match_score"] >= 40:
                    matching_briefs.append({
                        "brief": b_detail.model_dump(),
                        "match_score": match_info["match_score"],
                        "match_reason": match_info["match_reason"]
                    })

        matching_briefs.sort(key=lambda m: m["match_score"], reverse=True)
        conn.close()

        return {
            "role": "creator",
            "user": user,
            "creator": cr_dict,
            "profile_completeness": completeness,
            "matching_briefs": matching_briefs
        }
