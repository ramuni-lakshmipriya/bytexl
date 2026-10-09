from typing import List, Optional
import uuid
from fastapi import APIRouter, HTTPException, Query, Depends
from backend.database import get_db
from backend.schemas import (
    BriefSummary, BriefDetail, BriefCreate,
    BriefDraftRequest, BriefDraftResponse,
    CreatorMatch, Tool, Skill
)
from backend.services.brief_ai import generate_brief_draft
from backend.services.matcher import compute_creator_match
from backend.services.auth import require_role
from backend.routers.creators import build_creator_dict

router = APIRouter(prefix="/briefs", tags=["briefs"])

def fetch_brief_detail_by_id(brief_id: str, cursor) -> BriefDetail:
    cursor.execute("""
        SELECT b.*, br.name as brand_name, br.logo_url as brand_logo, br.is_agency, ct.name as content_type_name
        FROM briefs b
        JOIN brands br ON b.brand_id = br.id
        JOIN content_types ct ON b.content_type_id = ct.id
        WHERE b.id = ?
    """, (brief_id,))
    row = cursor.fetchone()
    if not row:
        return None

    # Fetch required tools
    cursor.execute("""
        SELECT t.id, t.name, t.category, t.commercial_use, t.url
        FROM tools t
        JOIN brief_required_tools brt ON t.id = brt.tool_id
        WHERE brt.brief_id = ?
        ORDER BY t.name ASC
    """, (brief_id,))
    req_tools = [Tool(**dict(r)) for r in cursor.fetchall()]

    # Fetch required skills
    cursor.execute("""
        SELECT s.id, s.name
        FROM skills s
        JOIN brief_required_skills brs ON s.id = brs.skill_id
        WHERE brs.brief_id = ?
        ORDER BY s.name ASC
    """, (brief_id,))
    req_skills = [Skill(**dict(r)) for r in cursor.fetchall()]

    return BriefDetail(
        id=row["id"],
        brand_id=row["brand_id"],
        brand_name=row["brand_name"],
        brand_logo=row["brand_logo"],
        is_agency=bool(row["is_agency"]),
        title=row["title"],
        campaign_goal=row["campaign_goal"],
        description=row["description"],
        content_type_id=row["content_type_id"],
        content_type_name=row["content_type_name"],
        style=row["style"],
        aspect_ratio=row["aspect_ratio"],
        duration_sec=row["duration_sec"],
        deliverables_count=row["deliverables_count"] or 1,
        budget_min_inr=row["budget_min_inr"],
        budget_max_inr=row["budget_max_inr"],
        deadline=row["deadline"],
        commercial_use=row["commercial_use"],
        usage_region=row["usage_region"],
        status=row["status"],
        created_at=str(row["created_at"]),
        required_tools=req_tools,
        required_skills=req_skills
    )

@router.get("", response_model=List[BriefSummary])
def get_briefs(status: Optional[str] = Query(None, pattern="^(open|in_review|closed)$")):
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT id FROM briefs WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    briefs = []
    for r in rows:
        b_detail = fetch_brief_detail_by_id(r["id"], cursor)
        if b_detail:
            briefs.append(b_detail)

    conn.close()
    return briefs

@router.get("/{brief_id}", response_model=BriefDetail)
def get_brief_by_id(brief_id: str):
    conn = get_db()
    cursor = conn.cursor()

    b_detail = fetch_brief_detail_by_id(brief_id, cursor)
    conn.close()

    if not b_detail:
        raise HTTPException(status_code=404, detail=f"Brief with ID '{brief_id}' not found")

    return b_detail

@router.post("", response_model=BriefDetail, status_code=201)
def create_brief(brief: BriefCreate, current_user: dict = Depends(require_role("brand"))):
    # Validation
    if brief.aspect_ratio not in ["16:9", "9:16", "1:1", "4:5"]:
        raise HTTPException(status_code=400, detail="Invalid aspect ratio. Must be one of: 16:9, 9:16, 1:1, 4:5")

    if brief.commercial_use not in ["full_buyout", "social_only", "internal_only"]:
        raise HTTPException(status_code=400, detail="Invalid commercial use option")

    if brief.budget_min_inr and brief.budget_max_inr and brief.budget_min_inr > brief.budget_max_inr:
        raise HTTPException(status_code=400, detail="Minimum budget cannot exceed maximum budget")

    brand_id = current_user.get("brand_id")
    if not brand_id:
        raise HTTPException(status_code=400, detail="Logged in user is not associated with a valid brand record.")

    conn = get_db()
    cursor = conn.cursor()

    # Check content_type_id exists
    cursor.execute("SELECT id FROM content_types WHERE id = ?", (brief.content_type_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail=f"Content type ID {brief.content_type_id} does not exist")

    # Generate Brief ID e.g. bf_custom_...
    new_id = f"bf_{uuid.uuid4().hex[:8]}"

    cursor.execute("""
        INSERT INTO briefs (
            id, brand_id, title, campaign_goal, description, content_type_id,
            style, aspect_ratio, duration_sec, deliverables_count,
            budget_min_inr, budget_max_inr, deadline, commercial_use,
            usage_region, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'open')
    """, (
        new_id, brand_id, brief.title, brief.campaign_goal, brief.description,
        brief.content_type_id, brief.style, brief.aspect_ratio, brief.duration_sec,
        brief.deliverables_count, brief.budget_min_inr, brief.budget_max_inr,
        brief.deadline, brief.commercial_use, brief.usage_region
    ))

    # Insert required tools
    for tid in brief.required_tool_ids:
        cursor.execute("INSERT OR IGNORE INTO brief_required_tools (brief_id, tool_id) VALUES (?, ?)", (new_id, tid))

    # Insert required skills
    for sid in brief.required_skill_ids:
        cursor.execute("INSERT OR IGNORE INTO brief_required_skills (brief_id, skill_id) VALUES (?, ?)", (new_id, sid))

    conn.commit()

    created_brief = fetch_brief_detail_by_id(new_id, cursor)
    conn.close()

    return created_brief

@router.post("/draft", response_model=BriefDraftResponse)
def draft_brief_ai(req: BriefDraftRequest):
    draft_data = generate_brief_draft(req.prompt)
    return BriefDraftResponse(**draft_data)

@router.get("/{brief_id}/matches", response_model=List[CreatorMatch])
def get_brief_matches(brief_id: str):
    conn = get_db()
    cursor = conn.cursor()

    b_detail = fetch_brief_detail_by_id(brief_id, cursor)
    if not b_detail:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Brief with ID '{brief_id}' not found")

    # Brief as dict for matcher
    brief_dict = {
        "content_type_id": b_detail.content_type_id,
        "required_tool_ids": [t.id for t in b_detail.required_tools],
        "required_skill_ids": [s.id for s in b_detail.required_skills],
        "budget_min_inr": b_detail.budget_min_inr,
        "budget_max_inr": b_detail.budget_max_inr
    }

    # Fetch all creators
    cursor.execute("SELECT * FROM creators")
    creator_rows = cursor.fetchall()

    matches = []
    for cr in creator_rows:
        summary = build_creator_dict(cr, cursor)
        cr_dict = summary.model_dump()
        match_info = compute_creator_match(cr_dict, brief_dict)

        matches.append(CreatorMatch(
            creator=summary,
            match_score=match_info["match_score"],
            score_breakdown=match_info["score_breakdown"],
            match_reason=match_info["match_reason"]
        ))

    conn.close()

    # Sort matches by score descending
    matches.sort(key=lambda m: m.match_score, reverse=True)
    return matches
