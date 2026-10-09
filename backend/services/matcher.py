"""
Creator-to-Brief Match Scoring Service

Weights & Formula Breakdown (Total 100 Points):
1. Required Tool Overlap: 30 Points
   - Score = (creator_tools_matching_brief_req / total_brief_required_tools) * 30
   - If brief requires no tools, creator gets full 30 points.
2. Required Skill Overlap: 30 Points
   - Score = (creator_skills_matching_brief_req / total_brief_required_skills) * 30
   - If brief requires no skills, creator gets full 30 points.
3. Content Type Compatibility: 15 Points
   - If brief's content_type_id is in creator's content_types: 15 points, else 0.
4. Budget Compatibility: 15 Points
   - Checks overlap between creator rate range (rate_min..rate_max) and brief budget range (budget_min..budget_max).
   - Full overlap (creator fits inside or overlaps >= 50% budget range): 15 points.
   - Partial overlap: 7.5 points.
   - No overlap: 0 points.
5. Availability: 5 Points
   - 'available': 5 points.
   - 'busy': 0 points.
6. Verification Signals: 5 Points
   - (tools_verified + workflow_documented + past_work_linked) / 3 * 5 points.
"""

from typing import Dict, Any, List
from backend.database import get_db

def extract_id(item: Any) -> Any:
    if isinstance(item, dict):
        return item.get("id")
    if isinstance(item, (int, str)):
        return item
    return getattr(item, "id", item)

def compute_creator_match(creator: Dict[str, Any], brief: Dict[str, Any]) -> Dict[str, Any]:
    # 1. Required Tools Match (30 pts)
    req_tool_ids = set(extract_id(t) for t in brief.get("required_tool_ids", []) if extract_id(t) is not None)
    creator_tool_ids = set(extract_id(t) for t in creator.get("tools", []) if extract_id(t) is not None)
    
    if not req_tool_ids:
        tool_score = 30.0
        tool_match_count = 0
    else:
        matched_tools = req_tool_ids.intersection(creator_tool_ids)
        tool_match_count = len(matched_tools)
        tool_score = (tool_match_count / len(req_tool_ids)) * 30.0

    # 2. Required Skills Match (30 pts)
    req_skill_ids = set(extract_id(s) for s in brief.get("required_skill_ids", []) if extract_id(s) is not None)
    creator_skill_ids = set(extract_id(s) for s in creator.get("skills", []) if extract_id(s) is not None)
    
    if not req_skill_ids:
        skill_score = 30.0
        skill_match_count = 0
    else:
        matched_skills = req_skill_ids.intersection(creator_skill_ids)
        skill_match_count = len(matched_skills)
        skill_score = (skill_match_count / len(req_skill_ids)) * 30.0

    # 3. Content Type Match (15 pts)
    creator_ct_ids = set(ct["id"] for ct in creator.get("content_types", []))
    brief_ct_id = brief.get("content_type_id")
    if brief_ct_id and brief_ct_id in creator_ct_ids:
        ct_score = 15.0
        ct_match = True
    else:
        ct_score = 0.0
        ct_match = False

    # 4. Budget Match (15 pts)
    c_min = creator.get("rate_min_inr") or 0
    c_max = creator.get("rate_max_inr") or 999999
    b_min = brief.get("budget_min_inr") or 0
    b_max = brief.get("budget_max_inr") or 999999

    # Check range overlap
    overlap_min = max(c_min, b_min)
    overlap_max = min(c_max, b_max)
    if overlap_min <= overlap_max:
        # Overlap exists
        if c_min >= b_min and c_max <= b_max:
            budget_score = 15.0  # Perfect fit inside budget
            budget_status = "fits budget"
        else:
            budget_score = 10.0  # Overlaps budget range
            budget_status = "budget overlaps"
    else:
        budget_score = 0.0
        budget_status = "above budget" if c_min > b_max else "rate below budget"

    # 5. Availability Match (5 pts)
    if creator.get("availability") == "available":
        avail_score = 5.0
        avail_status = "available"
    else:
        avail_score = 0.0
        avail_status = "busy"

    # 6. Verification Signals (5 pts)
    v_tools = 1 if creator.get("tools_verified") else 0
    v_work = 1 if creator.get("workflow_documented") else 0
    v_past = 1 if creator.get("past_work_linked") else 0
    verification_score = ((v_tools + v_work + v_past) / 3.0) * 5.0

    total_score = round(tool_score + skill_score + ct_score + budget_score + avail_score + verification_score)
    total_score = max(0, min(100, total_score))

    # Generate Human-Readable Reason
    reasons = []
    if req_tool_ids:
        reasons.append(f"Matches {tool_match_count}/{len(req_tool_ids)} required tools")
    if req_skill_ids:
        reasons.append(f"covers {skill_match_count}/{len(req_skill_ids)} skills")
    reasons.append(budget_status)
    if v_work:
        reasons.append("verified workflow")
    elif v_tools:
        reasons.append("tools verified")

    reason_str = ", ".join(reasons)
    # Capitalize first letter
    reason_str = reason_str[0].upper() + reason_str[1:] if reason_str else "General match profile"

    return {
        "match_score": total_score,
        "score_breakdown": {
            "tool_score": round(tool_score, 1),
            "skill_score": round(skill_score, 1),
            "content_type_score": round(ct_score, 1),
            "budget_score": round(budget_score, 1),
            "availability_score": round(avail_score, 1),
            "verification_score": round(verification_score, 1)
        },
        "match_reason": reason_str
    }
