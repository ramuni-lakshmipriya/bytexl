from typing import List, Optional
import uuid
from fastapi import APIRouter, HTTPException, Query, Depends
from backend.database import get_db
from backend.services.auth import require_role
from backend.schemas import (
    CreatorSummary, CreatorDetail, CreatorListResponse,
    Tool, Skill, ContentType, PortfolioItem,
    CreatorProfileUpdate, PortfolioItemCreate, PortfolioItemUpdate,
    StarterStudioProjectCreate, StarterStudioProjectOut
)

router = APIRouter(prefix="/creators", tags=["creators"])

def build_creator_dict(row, cursor):
    """Helper to assemble a creator dictionary with tools, skills, content_types, portfolio_count."""
    c_id = row["id"]

    # Fetch Tools
    cursor.execute("""
        SELECT t.id, t.name, t.category, t.category_name, t.commercial_use, t.url, t.description, t.popular_archetype
        FROM tools t
        JOIN creator_tools ct ON t.id = ct.tool_id
        WHERE ct.creator_id = ?
        ORDER BY t.name ASC
    """, (c_id,))
    tools = [Tool(**dict(r)) for r in cursor.fetchall()]

    # Fetch Skills
    cursor.execute("""
        SELECT s.id, s.name
        FROM skills s
        JOIN creator_skills cs ON s.id = cs.skill_id
        WHERE cs.creator_id = ?
        ORDER BY s.name ASC
    """, (c_id,))
    skills = [Skill(**dict(r)) for r in cursor.fetchall()]

    # Fetch Content Types
    cursor.execute("""
        SELECT ct.id, ct.name
        FROM content_types ct
        JOIN creator_content_types cct ON ct.id = cct.content_type_id
        WHERE cct.creator_id = ?
        ORDER BY ct.name ASC
    """, (c_id,))
    content_types = [ContentType(**dict(r)) for r in cursor.fetchall()]

    # Portfolio Count
    cursor.execute("SELECT COUNT(*) as count FROM portfolio_items WHERE creator_id = ?", (c_id,))
    portfolio_count = cursor.fetchone()["count"]

    languages_str = row["languages"] or ""
    languages = [l.strip() for l in languages_str.split(",") if l.strip()]

    return CreatorSummary(
        id=row["id"],
        name=row["name"],
        headline=row["headline"],
        bio=row["bio"],
        location=row["location"],
        avatar_url=row["avatar_url"],
        specialization=row["specialization"],
        experience_level=row["experience_level"],
        rate_min_inr=row["rate_min_inr"],
        rate_max_inr=row["rate_max_inr"],
        availability=row["availability"],
        languages=languages,
        tools_verified=bool(row["tools_verified"]),
        workflow_documented=bool(row["workflow_documented"]),
        past_work_linked=bool(row["past_work_linked"]),
        tools=tools,
        skills=skills,
        content_types=content_types,
        portfolio_count=portfolio_count
    )

@router.get("", response_model=CreatorListResponse)
def get_creators(
    search: Optional[str] = None,
    tools: Optional[List[str]] = Query(None),
    skills: Optional[List[str]] = Query(None),
    match_tools: str = Query("any", pattern="^(any|all)$"),
    match_skills: str = Query("any", pattern="^(any|all)$"),
    specialization: Optional[str] = None,
    content_type: Optional[str] = None,
    availability: Optional[str] = None,
    experience_level: Optional[str] = None,
    budget_max: Optional[int] = None,
    verified_only: bool = False,
    sort_by: str = Query("relevance", pattern="^(relevance|rate_asc|rate_desc|experience)$")
):
    conn = get_db()
    cursor = conn.cursor()

    # Parse comma separated values if query params sent as single string with commas
    parsed_tools = []
    if tools:
        for t in tools:
            parsed_tools.extend([item.strip() for item in t.split(",") if item.strip()])

    parsed_skills = []
    if skills:
        for s in skills:
            parsed_skills.extend([item.strip() for item in s.split(",") if item.strip()])

    query = "SELECT c.* FROM creators c WHERE 1=1"
    params = []

    # 1. Search filter
    if search:
        s_term = f"%{search.strip()}%"
        query += " AND (c.name LIKE ? OR c.headline LIKE ? OR c.bio LIKE ? OR c.location LIKE ?)"
        params.extend([s_term, s_term, s_term, s_term])

    # 2. Specialization
    if specialization:
        query += " AND c.specialization = ?"
        params.append(specialization)

    # 3. Availability
    if availability:
        query += " AND c.availability = ?"
        params.append(availability)

    # 4. Experience Level
    if experience_level:
        query += " AND c.experience_level = ?"
        params.append(experience_level)

    # 5. Budget Max
    if budget_max is not None:
        query += " AND c.rate_min_inr <= ?"
        params.append(budget_max)

    # 6. Verified Only
    if verified_only:
        query += " AND (c.tools_verified = 1 OR c.workflow_documented = 1 OR c.past_work_linked = 1)"

    # 7. Content Type Filter
    if content_type:
        query += """ AND c.id IN (
            SELECT creator_id FROM creator_content_types cct
            JOIN content_types ct ON cct.content_type_id = ct.id
            WHERE ct.name = ? OR CAST(ct.id AS TEXT) = ?
        )"""
        params.extend([content_type, content_type])

    # 8. Tools Filter (any vs all)
    if parsed_tools:
        placeholders = ",".join(["?"] * len(parsed_tools))
        if match_tools == "all":
            query += f""" AND c.id IN (
                SELECT ct.creator_id FROM creator_tools ct
                JOIN tools t ON ct.tool_id = t.id
                WHERE t.name IN ({placeholders}) OR CAST(t.id AS TEXT) IN ({placeholders})
                GROUP BY ct.creator_id
                HAVING COUNT(DISTINCT t.id) >= ?
            )"""
            params.extend(parsed_tools)
            params.extend(parsed_tools)
            params.append(len(parsed_tools))
        else: # any
            query += f""" AND c.id IN (
                SELECT ct.creator_id FROM creator_tools ct
                JOIN tools t ON ct.tool_id = t.id
                WHERE t.name IN ({placeholders}) OR CAST(t.id AS TEXT) IN ({placeholders})
            )"""
            params.extend(parsed_tools)
            params.extend(parsed_tools)

    # 9. Skills Filter (any vs all)
    if parsed_skills:
        placeholders = ",".join(["?"] * len(parsed_skills))
        if match_skills == "all":
            query += f""" AND c.id IN (
                SELECT cs.creator_id FROM creator_skills cs
                JOIN skills s ON cs.skill_id = s.id
                WHERE s.name IN ({placeholders}) OR CAST(s.id AS TEXT) IN ({placeholders})
                GROUP BY cs.creator_id
                HAVING COUNT(DISTINCT s.id) >= ?
            )"""
            params.extend(parsed_skills)
            params.extend(parsed_skills)
            params.append(len(parsed_skills))
        else: # any
            query += f""" AND c.id IN (
                SELECT cs.creator_id FROM creator_skills cs
                JOIN skills s ON cs.skill_id = s.id
                WHERE s.name IN ({placeholders}) OR CAST(s.id AS TEXT) IN ({placeholders})
            )"""
            params.extend(parsed_skills)
            params.extend(parsed_skills)

    # Sorting
    if sort_by == "rate_asc":
        query += " ORDER BY c.rate_min_inr ASC"
    elif sort_by == "rate_desc":
        query += " ORDER BY c.rate_max_inr DESC"
    elif sort_by == "experience":
        query += " ORDER BY CASE c.experience_level WHEN 'senior' THEN 3 WHEN 'mid' THEN 2 WHEN 'junior' THEN 1 ELSE 0 END DESC"
    else: # relevance
        query += " ORDER BY (c.tools_verified + c.workflow_documented + c.past_work_linked) DESC, c.name ASC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    creators_list = [build_creator_dict(r, cursor) for r in rows]

    conn.close()

    return CreatorListResponse(
        total=len(creators_list),
        creators=creators_list
    )

@router.get("/{creator_id}", response_model=CreatorDetail)
def get_creator_detail(creator_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM creators WHERE id = ?", (creator_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Creator with ID '{creator_id}' not found")

    summary = build_creator_dict(row, cursor)

    # Fetch portfolio items
    cursor.execute("""
        SELECT p.*, ct.name as content_type_name
        FROM portfolio_items p
        LEFT JOIN content_types ct ON p.content_type_id = ct.id
        WHERE p.creator_id = ?
        ORDER BY p.year DESC, p.title ASC
    """, (creator_id,))
    p_rows = cursor.fetchall()

    portfolio_items = []
    for pr in p_rows:
        item_id = pr["id"]
        cursor.execute("""
            SELECT t.id, t.name, t.category, t.category_name, t.commercial_use, t.url, t.description, t.popular_archetype
            FROM tools t
            JOIN portfolio_item_tools pit ON t.id = pit.tool_id
            WHERE pit.item_id = ?
            ORDER BY t.name ASC
        """, (item_id,))
        p_tools = [Tool(**dict(tr)) for tr in cursor.fetchall()]

        portfolio_items.append(PortfolioItem(
            id=pr["id"],
            creator_id=pr["creator_id"],
            title=pr["title"],
            media_type=pr["media_type"],
            content_type_id=pr["content_type_id"],
            content_type_name=pr["content_type_name"],
            media_url=pr["media_url"],
            thumbnail_url=pr["thumbnail_url"],
            duration_sec=pr["duration_sec"],
            aspect_ratio=pr["aspect_ratio"],
            workflow=pr["workflow"],
            process_notes=pr["process_notes"],
            client_name=pr["client_name"],
            commercial_use=pr["commercial_use"],
            year=pr["year"],
            tools=p_tools
        ))

    conn.close()

    return CreatorDetail(
        **summary.model_dump(),
        portfolio=portfolio_items
    )

# --- Creator Profile & Onboarding Updates ---
@router.put("/me", response_model=CreatorDetail)
def update_my_creator_profile(
    updates: CreatorProfileUpdate,
    current_user: dict = Depends(require_role("creator"))
):
    c_id = current_user.get("creator_id")
    if not c_id:
        raise HTTPException(status_code=400, detail="User is not linked to a valid creator record")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM creators WHERE id = ?", (c_id,))
    cr_row = cursor.fetchone()
    if not cr_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Creator record not found")

    # Update basic fields if provided
    update_fields = []
    params = []

    if updates.name is not None:
        update_fields.append("name = ?")
        params.append(updates.name.strip())
        cursor.execute("UPDATE users SET display_name = ? WHERE creator_id = ?", (updates.name.strip(), c_id))

    if updates.headline is not None:
        update_fields.append("headline = ?")
        params.append(updates.headline.strip())

    if updates.bio is not None:
        update_fields.append("bio = ?")
        params.append(updates.bio.strip())

    if updates.specialization is not None:
        update_fields.append("specialization = ?")
        params.append(updates.specialization.strip())

    if updates.experience_level is not None:
        update_fields.append("experience_level = ?")
        params.append(updates.experience_level.strip())

    if updates.availability is not None:
        update_fields.append("availability = ?")
        params.append(updates.availability.strip())

    if updates.rate_min_inr is not None:
        update_fields.append("rate_min_inr = ?")
        params.append(updates.rate_min_inr)

    if updates.rate_max_inr is not None:
        update_fields.append("rate_max_inr = ?")
        params.append(updates.rate_max_inr)

    if updates.location is not None:
        update_fields.append("location = ?")
        params.append(updates.location.strip())

    if updates.languages:
        update_fields.append("languages = ?")
        params.append(", ".join(updates.languages))

    if update_fields:
        query = f"UPDATE creators SET {', '.join(update_fields)} WHERE id = ?"
        params.append(c_id)
        cursor.execute(query, params)

    # Sync Tools
    if updates.tools:
        cursor.execute("DELETE FROM creator_tools WHERE creator_id = ?", (c_id,))
        for t_name in updates.tools:
            cursor.execute("SELECT id FROM tools WHERE name = ? OR CAST(id AS TEXT) = ?", (t_name, t_name))
            tr = cursor.fetchone()
            if tr:
                cursor.execute("INSERT OR IGNORE INTO creator_tools (creator_id, tool_id) VALUES (?, ?)", (c_id, tr["id"]))

    # Sync Skills
    if updates.skills:
        cursor.execute("DELETE FROM creator_skills WHERE creator_id = ?", (c_id,))
        for s_name in updates.skills:
            cursor.execute("SELECT id FROM skills WHERE name = ? OR CAST(id AS TEXT) = ?", (s_name, s_name))
            sr = cursor.fetchone()
            if sr:
                cursor.execute("INSERT OR IGNORE INTO creator_skills (creator_id, skill_id) VALUES (?, ?)", (c_id, sr["id"]))

    # Sync Content Types
    if updates.content_types:
        cursor.execute("DELETE FROM creator_content_types WHERE creator_id = ?", (c_id,))
        for ct_name in updates.content_types:
            cursor.execute("SELECT id FROM content_types WHERE name = ? OR CAST(id AS TEXT) = ?", (ct_name, ct_name))
            ctr = cursor.fetchone()
            if ctr:
                cursor.execute("INSERT OR IGNORE INTO creator_content_types (creator_id, content_type_id) VALUES (?, ?)", (c_id, ctr["id"]))

    conn.commit()
    conn.close()

    return get_creator_detail(c_id)

# --- Creator Portfolio Management (CRUD) ---
@router.post("/me/portfolio", response_model=PortfolioItem, status_code=201)
def add_portfolio_item(
    item: PortfolioItemCreate,
    current_user: dict = Depends(require_role("creator"))
):
    c_id = current_user.get("creator_id")
    if not c_id:
        raise HTTPException(status_code=400, detail="User is not linked to a valid creator record")

    conn = get_db()
    cursor = conn.cursor()

    pf_id = f"pf_{uuid.uuid4().hex[:8]}"

    # Default fallback thumbnail if missing
    thumb = item.thumbnail_url or item.media_url or f"https://picsum.photos/seed/{pf_id}/600/400"

    cursor.execute("""
        INSERT INTO portfolio_items (
            id, creator_id, title, media_type, content_type_id, media_url,
            thumbnail_url, duration_sec, aspect_ratio, workflow, process_notes,
            client_name, commercial_use, year
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pf_id, c_id, item.title, item.media_type, item.content_type_id,
        item.media_url or thumb, thumb, item.duration_sec, item.aspect_ratio,
        item.workflow, item.process_notes, item.client_name, item.commercial_use, item.year
    ))

    # Insert associated tools
    for tid in item.tool_ids:
        cursor.execute("INSERT OR IGNORE INTO portfolio_item_tools (item_id, tool_id) VALUES (?, ?)", (pf_id, tid))

    # Mark workflow_documented if workflow present
    if item.workflow and len(item.workflow) > 10:
        cursor.execute("UPDATE creators SET workflow_documented = 1, past_work_linked = 1 WHERE id = ?", (c_id,))

    conn.commit()
    conn.close()

    # Return full updated detail
    detail = get_creator_detail(c_id)
    added = next((p for p in detail.portfolio if p.id == pf_id), None)
    if not added:
        raise HTTPException(status_code=500, detail="Failed to retrieve newly created portfolio item")
    return added

@router.put("/me/portfolio/{item_id}", response_model=PortfolioItem)
def update_portfolio_item(
    item_id: str,
    updates: PortfolioItemUpdate,
    current_user: dict = Depends(require_role("creator"))
):
    c_id = current_user.get("creator_id")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM portfolio_items WHERE id = ? AND creator_id = ?", (item_id, c_id))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio item not found or unauthorized")

    fields = []
    params = []

    for key, val in updates.model_dump(exclude_unset=True).items():
        if key == "tool_ids":
            continue
        if val is not None:
            fields.append(f"{key} = ?")
            params.append(val)

    if fields:
        params.append(item_id)
        cursor.execute(f"UPDATE portfolio_items SET {', '.join(fields)} WHERE id = ?", params)

    if updates.tool_ids is not None:
        cursor.execute("DELETE FROM portfolio_item_tools WHERE item_id = ?", (item_id,))
        for tid in updates.tool_ids:
            cursor.execute("INSERT OR IGNORE INTO portfolio_item_tools (item_id, tool_id) VALUES (?, ?)", (item_id, tid))

    conn.commit()
    conn.close()

    detail = get_creator_detail(c_id)
    updated = next((p for p in detail.portfolio if p.id == item_id), None)
    if not updated:
        raise HTTPException(status_code=404, detail="Portfolio item missing after update")
    return updated

@router.delete("/me/portfolio/{item_id}")
def delete_portfolio_item(
    item_id: str,
    current_user: dict = Depends(require_role("creator"))
):
    c_id = current_user.get("creator_id")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM portfolio_items WHERE id = ? AND creator_id = ?", (item_id, c_id))
    existing = cursor.fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Portfolio item not found or unauthorized")

    cursor.execute("DELETE FROM portfolio_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": f"Portfolio item '{item_id}' deleted successfully"}

# --- Starter Studio Saved Projects ---
@router.get("/me/studio-projects", response_model=List[StarterStudioProjectOut])
def get_my_studio_projects(current_user: dict = Depends(require_role("creator"))):
    c_id = current_user.get("creator_id")
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM starter_studio_projects WHERE creator_id = ? ORDER BY created_at DESC", (c_id,))
    rows = cursor.fetchall()
    conn.close()

    return [StarterStudioProjectOut(**dict(r)) for r in rows]

@router.post("/me/studio-projects", response_model=StarterStudioProjectOut, status_code=201)
def save_studio_project(
    req: StarterStudioProjectCreate,
    current_user: dict = Depends(require_role("creator"))
):
    c_id = current_user.get("creator_id")
    conn = get_db()
    cursor = conn.cursor()

    # Check if project already exists for this creator & title
    cursor.execute("SELECT * FROM starter_studio_projects WHERE creator_id = ? AND title = ?", (c_id, req.title))
    existing = cursor.fetchone()

    if existing:
        new_status = "completed" if existing["status"] == "in_progress" else "in_progress"
        cursor.execute("UPDATE starter_studio_projects SET status = ?, notes = ? WHERE id = ?", (new_status, req.notes or existing["notes"], existing["id"]))
        conn.commit()
        cursor.execute("SELECT * FROM starter_studio_projects WHERE id = ?", (existing["id"],))
        updated = cursor.fetchone()
        conn.close()
        return StarterStudioProjectOut(**dict(updated))

    ssp_id = f"ssp_{uuid.uuid4().hex[:8]}"
    cursor.execute("""
        INSERT INTO starter_studio_projects (id, creator_id, title, project_type, status, notes)
        VALUES (?, ?, ?, ?, 'in_progress', ?)
    """, (ssp_id, c_id, req.title, req.project_type, req.notes or ""))

    conn.commit()
    cursor.execute("SELECT * FROM starter_studio_projects WHERE id = ?", (ssp_id,))
    row = cursor.fetchone()
    conn.close()
    return StarterStudioProjectOut(**dict(row))

