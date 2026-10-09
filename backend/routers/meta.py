from fastapi import APIRouter
from backend.database import get_db
from backend.schemas import MetaResponse, Tool, Skill, ContentType

router = APIRouter(prefix="", tags=["meta"])

@router.get("/meta", response_model=MetaResponse)
def get_meta():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, category, commercial_use, url FROM tools ORDER BY name ASC")
    tools = [Tool(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM skills ORDER BY name ASC")
    skills = [Skill(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM content_types ORDER BY name ASC")
    content_types = [ContentType(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT specialization FROM creators ORDER BY specialization ASC")
    specializations = [row["specialization"] for row in cursor.fetchall()]

    conn.close()

    return MetaResponse(
        tools=tools,
        skills=skills,
        content_types=content_types,
        specializations=specializations,
        aspect_ratios=["16:9", "9:16", "1:1", "4:5"],
        commercial_use_options=["full_buyout", "social_only", "internal_only"]
    )
