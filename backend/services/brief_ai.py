import os
import json
import re
import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List
from backend.database import get_db

def get_ref_data():
    """Fetch current valid reference options from SQLite database."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM content_types")
    content_types = [{"id": r["id"], "name": r["name"]} for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM tools")
    tools = [{"id": r["id"], "name": r["name"]} for r in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM skills")
    skills = [{"id": r["id"], "name": r["name"]} for r in cursor.fetchall()]

    conn.close()

    return {
        "content_types": content_types,
        "tools": tools,
        "skills": skills,
        "aspect_ratios": ["16:9", "9:16", "1:1", "4:5"],
        "commercial_use_options": ["full_buyout", "social_only", "internal_only"],
    }

def rule_based_fallback(prompt: str, ref: Dict[str, Any]) -> Dict[str, Any]:
    """
    Keyword and rule-based extractor when LLM is unavailable or key is missing.
    Matches text against content_types, tools, skills, and aspect ratios.
    """
    prompt_lower = prompt.lower()

    # 1. Content type match
    selected_ct = ref["content_types"][0]  # default fallback
    for ct in ref["content_types"]:
        if ct["name"].lower() in prompt_lower:
            selected_ct = ct
            break

    # 2. Tools match
    matched_tool_ids = []
    for t in ref["tools"]:
        if re.search(r'\b' + re.escape(t["name"].lower()) + r'\b', prompt_lower):
            matched_tool_ids.append(t["id"])
    if not matched_tool_ids:
        # Default top tools if none matched
        matched_tool_ids = [ref["tools"][0]["id"]]

    # 3. Skills match
    matched_skill_ids = []
    for s in ref["skills"]:
        if re.search(r'\b' + re.escape(s["name"].lower()) + r'\b', prompt_lower):
            matched_skill_ids.append(s["id"])
    if not matched_skill_ids:
        matched_skill_ids = [ref["skills"][0]["id"]]

    # 4. Aspect Ratio match
    aspect_ratio = "16:9"
    if "9:16" in prompt or "vertical" in prompt_lower or "reel" in prompt_lower or "tiktok" in prompt_lower or "shorts" in prompt_lower:
        aspect_ratio = "9:16"
    elif "1:1" in prompt or "square" in prompt_lower or "instagram post" in prompt_lower:
        aspect_ratio = "1:1"
    elif "4:5" in prompt:
        aspect_ratio = "4:5"

    # 5. Commercial use match
    commercial_use = "full_buyout"
    if "social" in prompt_lower:
        commercial_use = "social_only"
    elif "internal" in prompt_lower:
        commercial_use = "internal_only"

    # 6. Budget extraction (search for numbers like 30,000 or 50k)
    budget_min = 20000
    budget_max = 60000
    numbers = [int(n) for n in re.findall(r'\b\d+\b', prompt.replace(',', '')) if int(n) >= 1000]
    if len(numbers) >= 2:
        budget_min, budget_max = min(numbers), max(numbers)
    elif len(numbers) == 1:
        budget_min = int(numbers[0] * 0.8)
        budget_max = int(numbers[0] * 1.2)

    # 7. Duration extraction
    duration_sec = 30
    dur_match = re.search(r'(\d+)\s*(sec|second|s|min|minute)', prompt_lower)
    if dur_match:
        val = int(dur_match.group(1))
        unit = dur_match.group(2)
        duration_sec = val * 60 if 'min' in unit else val

    # Title & Goal generation
    clean_prompt = prompt.strip()
    first_sentence = clean_prompt.split('.')[0]
    title = f"Campaign: {first_sentence[:50]}" if len(first_sentence) > 10 else f"AI {selected_ct['name'].title()} Production"
    
    deadline_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    return {
        "title": title,
        "campaign_goal": f"Produce high-quality {selected_ct['name']} content based on prompt requirement.",
        "description": prompt,
        "content_type_id": selected_ct["id"],
        "style": "Cinematic / Modern AI-assisted style",
        "aspect_ratio": aspect_ratio,
        "duration_sec": duration_sec,
        "deliverables_count": 1,
        "budget_min_inr": budget_min,
        "budget_max_inr": budget_max,
        "deadline": deadline_date,
        "commercial_use": commercial_use,
        "usage_region": "Global",
        "required_tool_ids": matched_tool_ids,
        "required_skill_ids": matched_skill_ids,
        "ai_generated": False,
        "fallback_used": True
    }

def generate_brief_draft(prompt: str) -> Dict[str, Any]:
    """
    Main entry point for generating brief drafts.
    Tries LLM first if GEMINI_API_KEY is configured, else falls back to rule-based parser.
    """
    ref = get_ref_data()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return rule_based_fallback(prompt, ref)

    try:
        # Structured system instruction and schema constraints
        system_instruction = (
            "You are an expert creative producer. Parse the user's rough creative request "
            "and extract structured JSON fields matching reference constraints exactly.\n"
            f"Available content_types (MUST pick exact ID): {json.dumps(ref['content_types'])}\n"
            f"Available tools (MUST pick matching IDs): {json.dumps(ref['tools'])}\n"
            f"Available skills (MUST pick matching IDs): {json.dumps(ref['skills'])}\n"
            f"Valid aspect_ratios: {ref['aspect_ratios']}\n"
            f"Valid commercial_use: {ref['commercial_use_options']}\n"
            "Return valid JSON only matching the schema."
        )

        user_content = f"User Request: {prompt}"

        # Gemini REST API request payload
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": f"{system_instruction}\n\n{user_content}"}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }

        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code == 200:
            data = res.json()
            text_response = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(text_response)

            # Validate extracted values against reference tables
            ct_id = parsed.get("content_type_id")
            valid_ct_ids = [c["id"] for c in ref["content_types"]]
            if ct_id not in valid_ct_ids:
                ct_id = valid_ct_ids[0]

            aspect = parsed.get("aspect_ratio")
            if aspect not in ref["aspect_ratios"]:
                aspect = "16:9"

            comm_use = parsed.get("commercial_use")
            if comm_use not in ref["commercial_use_options"]:
                comm_use = "full_buyout"

            valid_tool_ids = [t["id"] for t in ref["tools"]]
            req_tools = [tid for tid in parsed.get("required_tool_ids", []) if tid in valid_tool_ids]
            if not req_tools:
                req_tools = [valid_tool_ids[0]]

            valid_skill_ids = [s["id"] for s in ref["skills"]]
            req_skills = [sid for sid in parsed.get("required_skill_ids", []) if sid in valid_skill_ids]
            if not req_skills:
                req_skills = [valid_skill_ids[0]]

            deadline_str = parsed.get("deadline")
            if not deadline_str or not re.match(r'^\d{4}-\d{2}-\d{2}$', str(deadline_str)):
                deadline_str = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

            return {
                "title": str(parsed.get("title", f"AI Production Brief")),
                "campaign_goal": str(parsed.get("campaign_goal", prompt)),
                "description": str(parsed.get("description", prompt)),
                "content_type_id": ct_id,
                "style": str(parsed.get("style", "Cinematic")),
                "aspect_ratio": aspect,
                "duration_sec": int(parsed.get("duration_sec", 30)),
                "deliverables_count": int(parsed.get("deliverables_count", 1)),
                "budget_min_inr": int(parsed.get("budget_min_inr", 15000)),
                "budget_max_inr": int(parsed.get("budget_max_inr", 50000)),
                "deadline": deadline_str,
                "commercial_use": comm_use,
                "usage_region": str(parsed.get("usage_region", "Global")),
                "required_tool_ids": req_tools,
                "required_skill_ids": req_skills,
                "ai_generated": True,
                "fallback_used": False
            }
        else:
            print(f"Gemini API returned error {res.status_code}: {res.text}. Falling back.")
            return rule_based_fallback(prompt, ref)

    except Exception as e:
        print(f"Exception during LLM brief generation: {e}. Falling back to rule-based.")
        return rule_based_fallback(prompt, ref)
