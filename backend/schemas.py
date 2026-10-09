from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr

# --- Reference Models ---
class Tool(BaseModel):
    id: int
    name: str
    category: str
    category_name: Optional[str] = None
    commercial_use: str
    url: Optional[str] = None
    description: Optional[str] = None
    popular_archetype: Optional[str] = None

class Skill(BaseModel):
    id: int
    name: str

class ContentType(BaseModel):
    id: int
    name: str

class ToolCategory(BaseModel):
    id: str
    name: str
    emoji: str
    count: int
    archetype: Optional[str] = None

class CreatorArchetype(BaseModel):
    id: str
    name: str
    role: str
    icon: str
    description: str
    key_tools: List[str]
    suggested_skills: List[str]

class MarketplaceSource(BaseModel):
    name: str
    url: str
    description: str
    badge: str

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
    tool_categories: Optional[List[ToolCategory]] = []
    creator_archetypes: Optional[List[CreatorArchetype]] = []
    marketplace_sources: Optional[List[MarketplaceSource]] = []

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
    name: Optional[str] = None
    headline: Optional[str] = None
    bio: Optional[str] = None
    specialization: Optional[str] = None
    experience_level: Optional[str] = None
    availability: Optional[str] = None
    rate_min_inr: Optional[int] = None
    rate_max_inr: Optional[int] = None
    location: Optional[str] = None
    languages: List[str] = []
    tools: List[str] = []
    skills: List[str] = []
    content_types: List[str] = []
    portfolio_links: Optional[str] = None
    commercial_preferences: Optional[str] = None

class PortfolioItemCreate(BaseModel):
    title: str = Field(..., min_length=2)
    media_type: str = "video"
    content_type_id: Optional[int] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_sec: Optional[int] = None
    aspect_ratio: Optional[str] = "16:9"
    workflow: Optional[str] = None
    process_notes: Optional[str] = None
    client_name: Optional[str] = None
    commercial_use: str = "cleared"
    year: Optional[int] = 2026
    tool_ids: List[int] = []

class PortfolioItemUpdate(BaseModel):
    title: Optional[str] = None
    media_type: Optional[str] = None
    content_type_id: Optional[int] = None
    media_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    duration_sec: Optional[int] = None
    aspect_ratio: Optional[str] = None
    workflow: Optional[str] = None
    process_notes: Optional[str] = None
    client_name: Optional[str] = None
    commercial_use: Optional[str] = None
    year: Optional[int] = None
    tool_ids: Optional[List[int]] = None

class BriefApplicationCreate(BaseModel):
    pitch: str = Field(..., min_length=10)
    proposed_rate_inr: int = Field(..., gt=0)
    estimated_days: int = Field(..., gt=0)

class BriefApplicationUpdate(BaseModel):
    status: Optional[str] = Field(None, pattern="^(applied|shortlisted|accepted|in_progress|delivered|completed|revision_requested|rejected)$")
    revision_feedback: Optional[str] = None

class DeliverySubmit(BaseModel):
    delivery_url: str = Field(..., min_length=5)
    delivery_notes: Optional[str] = None

class BriefApplicationOut(BaseModel):
    id: str
    brief_id: str
    brief_title: Optional[str] = None
    creator_id: str
    creator_name: Optional[str] = None
    creator_avatar: Optional[str] = None
    creator_headline: Optional[str] = None
    pitch: Optional[str] = None
    proposed_rate_inr: Optional[int] = None
    estimated_days: Optional[int] = None
    status: str
    delivery_url: Optional[str] = None
    delivery_notes: Optional[str] = None
    revision_feedback: Optional[str] = None
    payment_status: str
    created_at: str
    updated_at: str

class StarterStudioProjectCreate(BaseModel):
    title: str
    project_type: str
    notes: Optional[str] = None

class StarterStudioProjectOut(BaseModel):
    id: str
    creator_id: str
    title: str
    project_type: str
    status: str
    notes: Optional[str] = None
    created_at: str

class AuthConfigStatus(BaseModel):
    google_configured: bool
    facebook_configured: bool
    instagram_configured: bool

