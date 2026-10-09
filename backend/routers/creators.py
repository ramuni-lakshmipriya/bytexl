from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_db
from backend.schemas import (
    CreatorSummary, CreatorDetail, CreatorListResponse,
    Tool, Skill, ContentType, PortfolioItem
)

router = APIRouter(prefix="/creators", tags=["creators"])

def build_creator_dict(row, cursor):
    """Helper to assemble a creator dictionary with tools, skills, content_types, portfolio_count."""
    c_id = row["id"]

    # Fetch Tools
    cursor.execute("""
        SELECT t.id, t.name, t.category, t.commercial_use, t.url
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
            SELECT t.id, t.name, t.category, t.commercial_use, t.url
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
