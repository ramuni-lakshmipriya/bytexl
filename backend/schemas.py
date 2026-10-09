from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr

# --- Reference Models ---
class Tool(BaseModel):
    id: int
    name: str
    category: str
    commercial_use: str
    url: Optional[str] = None

class Skill(BaseModel):
    id: int
    name: str

class ContentType(BaseModel):
    id: int
    name: str

class Brand(BaseModel):
    id: str
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    is_agency: bool = False

class MetaResponse(BaseModel):
    tools: List[Tool]
    skills: List[Skill]
    content_types: List[ContentType]
    specializations: List[str]
    aspect_ratios: List[str]
    commercial_use_options: List[str]

# --- Portfolio Models ---
class PortfolioItem(BaseModel):
    id: str
    creator_id: str
    title: str
    media_type: str
    content_type_id: Optional[int] = None
    content_type_name: Optional[str] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_sec: Optional[int] = None
    aspect_ratio: Optional[str] = None
    workflow: Optional[str] = None
    process_notes: Optional[str] = None
    client_name: Optional[str] = None
    commercial_use: str
    year: Optional[int] = None
    tools: List[Tool] = []

# --- Creator Models ---
class CreatorSummary(BaseModel):
    id: str
    name: str
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    specialization: str
    experience_level: str
    rate_min_inr: Optional[int] = None
    rate_max_inr: Optional[int] = None
    availability: str
    languages: List[str] = []
    tools_verified: bool
    workflow_documented: bool
    past_work_linked: bool
    tools: List[Tool] = []
    skills: List[Skill] = []
    content_types: List[ContentType] = []
    portfolio_count: int = 0

class CreatorDetail(CreatorSummary):
    portfolio: List[PortfolioItem] = []

class CreatorListResponse(BaseModel):
    total: int
    creators: List[CreatorSummary]

# --- Brief Models ---
class BriefCreate(BaseModel):
    title: str = Field(..., min_length=3)
    campaign_goal: Optional[str] = None
    description: Optional[str] = None
    content_type_id: int
    style: Optional[str] = None
    aspect_ratio: Optional[str] = "16:9"
    duration_sec: Optional[int] = 30
    deliverables_count: Optional[int] = 1
    budget_min_inr: Optional[int] = 10000
    budget_max_inr: Optional[int] = 50000
    deadline: Optional[str] = None
    commercial_use: str = "full_buyout"
    usage_region: Optional[str] = "Global"
    required_tool_ids: List[int] = []
    required_skill_ids: List[int] = []

class BriefSummary(BaseModel):
    id: str
    brand_id: str
    brand_name: str
    brand_logo: Optional[str] = None
    is_agency: bool = False
    title: str
    campaign_goal: Optional[str] = None
    description: Optional[str] = None
    content_type_id: int
    content_type_name: str
    style: Optional[str] = None
    aspect_ratio: Optional[str] = None
    duration_sec: Optional[int] = None
    deliverables_count: int = 1
    budget_min_inr: Optional[int] = None
    budget_max_inr: Optional[int] = None
    deadline: Optional[str] = None
    commercial_use: str
    usage_region: Optional[str] = None
    status: str
    created_at: str
    required_tools: List[Tool] = []
    required_skills: List[Skill] = []

class BriefDetail(BriefSummary):
    pass

class BriefDraftRequest(BaseModel):
    prompt: str = Field(..., min_length=5)

class BriefDraftResponse(BaseModel):
    title: str
    campaign_goal: str
    description: str
    content_type_id: int
    style: str
    aspect_ratio: str
    duration_sec: int
    deliverables_count: int
    budget_min_inr: int
    budget_max_inr: int
    deadline: str
    commercial_use: str
    usage_region: str
    required_tool_ids: List[int]
    required_skill_ids: List[int]
    ai_generated: bool
    fallback_used: bool

# --- Match Score Models ---
class CreatorMatch(BaseModel):
    creator: CreatorSummary
    match_score: int  # 0 to 100
    score_breakdown: dict
    match_reason: str

# --- Auth Models ---
class UserOut(BaseModel):
    id: str
    email: str
    role: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    creator_id: Optional[str] = None
    brand_id: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class DemoLoginRequest(BaseModel):
    role: str = Field(..., pattern="^(creator|brand)$")

class CreatorSignupRequest(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: str
    password: str = Field(..., min_length=8)
    specialization: str
    tools: List[str] = []
    location: Optional[str] = None
    accept_terms: bool

class BrandSignupRequest(BaseModel):
    contact_name: str = Field(..., min_length=2)
    work_email: str
    password: str = Field(..., min_length=8)
    company_name: str = Field(..., min_length=2)
    industry: Optional[str] = None
    is_agency: bool = False
    website: Optional[str] = None
    accept_terms: bool

class CreatorProfileUpdate(BaseModel):
    headline: Optional[str] = None
    bio: Optional[str] = None
    rate_min_inr: Optional[int] = None
    rate_max_inr: Optional[int] = None
    availability: Optional[str] = None
    languages: List[str] = []
    skill_names: List[str] = []
    content_type_names: List[str] = []

class AuthConfigStatus(BaseModel):
    google_configured: bool
    facebook_configured: bool
    instagram_configured: bool
