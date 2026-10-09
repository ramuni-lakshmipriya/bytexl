from fastapi import APIRouter
from backend.database import get_db
from backend.schemas import (
    MetaResponse, Tool, Skill, ContentType,
    ToolCategory, CreatorArchetype, MarketplaceSource
)

router = APIRouter(prefix="", tags=["meta"])

CATEGORY_META = {
    "writing": {"name": "Writing, Scripts & Captions", "emoji": "✍️", "archetype": "AI Script Writer"},
    "image": {"name": "AI Image Generation", "emoji": "🎨", "archetype": "AI Graphic Designer"},
    "design": {"name": "Graphic Design, Posters & Thumbnails", "emoji": "🖼️", "archetype": "AI Graphic Designer"},
    "video": {"name": "AI Video Generation", "emoji": "🎬", "archetype": "AI Video Creator"},
    "editing": {"name": "Video Editing & Reels", "emoji": "📹", "archetype": "AI Editor & Repurposing Expert"},
    "voice": {"name": "Voice Generation & Text-to-Speech", "emoji": "🎙️", "archetype": "AI Voice Artist"},
    "music": {"name": "Music & Sound Effects", "emoji": "🎵", "archetype": "AI Music Producer"},
    "social": {"name": "Social Media Management", "emoji": "📱", "archetype": "Social Media Manager"},
    "research": {"name": "Research, Ideas & Trend Discovery", "emoji": "🔎", "archetype": "AI Marketing Strategist"},
    "seo": {"name": "SEO & Blog Optimization", "emoji": "📈", "archetype": "AI Marketing Strategist"},
    "podcast": {"name": "Podcasting & Audio Editing", "emoji": "🎧", "archetype": "AI Voice Artist"},
    "avatar": {"name": "AI Avatars, Dubbing & Translation", "emoji": "🌎", "archetype": "AI Influencer Creator"},
    "presentation": {"name": "Presentations & Infographics", "emoji": "📊", "archetype": "AI Graphic Designer"},
    "influencer": {"name": "AI Influencers & Virtual Creators", "emoji": "🤖", "archetype": "AI Influencer Creator"},
    "ugc": {"name": "UGC, Ads & Marketing Creatives", "emoji": "📣", "archetype": "UGC Ad Creator"},
    "repurposing": {"name": "Repurposing & Content Automation", "emoji": "♻️", "archetype": "AI Editor & Repurposing Expert"},
    "business": {"name": "Creator Business & Monetization", "emoji": "💼", "archetype": "Social Media Manager"},
    "coding": {"name": "AI Coding & Website Creation", "emoji": "💻", "archetype": "AI Graphic Designer"},
}

ARCHETYPES = [
    {
        "id": "ai_video_creator",
        "name": "AI Video Creator",
        "role": "AI Filmmaker & Video Specialist",
        "icon": "🎬",
        "description": "Produces cinematic generative shorts, ad spots, and trailers using state-of-the-art video diffusion models.",
        "key_tools": ["Runway", "Kling", "Veo", "Pika", "HeyGen"],
        "suggested_skills": ["prompt engineering", "camera direction", "storyboarding", "color grading"]
    },
    {
        "id": "ai_graphic_designer",
        "name": "AI Graphic Designer",
        "role": "Generative Graphics & Brand Visuals",
        "icon": "🎨",
        "description": "Crafts high-impact brand posters, product packaging, thumbnails, and vector assets.",
        "key_tools": ["Midjourney", "Ideogram", "Canva", "Adobe Firefly"],
        "suggested_skills": ["typography", "brand identity", "prompt engineering", "product photography"]
    },
    {
        "id": "ai_script_writer",
        "name": "AI Script Writer",
        "role": "Video Scripts & Content Strategist",
        "icon": "✍️",
        "description": "Writes scroll-stopping hooks, episodic video scripts, and high-converting marketing copy with LLMs.",
        "key_tools": ["ChatGPT", "Claude", "Jasper", "Copy.ai"],
        "suggested_skills": ["scriptwriting", "prompt engineering", "storyboarding", "social media strategy"]
    },
    {
        "id": "ai_voice_artist",
        "name": "AI Voice Artist",
        "role": "Voice Generation & Audio Storyteller",
        "icon": "🎙️",
        "description": "Masters expressive vocal cloning, multilingual voiceovers, and natural speech synthesis.",
        "key_tools": ["ElevenLabs", "Murf AI", "PlayHT"],
        "suggested_skills": ["voice cloning", "sound design", "localization", "audio editing"]
    },
    {
        "id": "ai_music_producer",
        "name": "AI Music Producer",
        "role": "Generative Audio & Sound Design",
        "icon": "🎵",
        "description": "Composes custom commercial soundtracks, ambient audio beds, and sound effects for visual media.",
        "key_tools": ["Suno", "Udio", "AIVA"],
        "suggested_skills": ["music composition", "sound design", "audio mastering"]
    },
    {
        "id": "ai_influencer_creator",
        "name": "AI Influencer Creator",
        "role": "Virtual Humans & Digital Persona Architect",
        "icon": "🤖",
        "description": "Develops consistent virtual brand ambassadors, AI avatars, and digital influencer channels.",
        "key_tools": ["HeyGen", "Hedra", "Synthesia"],
        "suggested_skills": ["avatar creation", "character design", "lip sync", "LoRA training"]
    },
    {
        "id": "ugc_ad_creator",
        "name": "UGC Ad Creator",
        "role": "Performance UGC & Direct Response Video",
        "icon": "📣",
        "description": "Rapidly tests high-converting direct-response ads and authentic creator-style product reviews.",
        "key_tools": ["Creatify", "Arcads", "JoggAI"],
        "suggested_skills": ["AI UGC ads", "video editing", "scriptwriting", "motion design"]
    },
    {
        "id": "social_media_manager",
        "name": "Social Media Manager",
        "role": "Multi-Channel Distribution & Community",
        "icon": "📱",
        "description": "Automates multi-platform publishing, trend research, engagement analytics, and social scheduling.",
        "key_tools": ["Buffer", "Predis.ai", "Metricool"],
        "suggested_skills": ["social media strategy", "SEO optimization", "content repurposing"]
    },
    {
        "id": "ai_editor_repurposer",
        "name": "AI Editor & Repurposing Expert",
        "role": "Long-to-Short Form & Virality Engineer",
        "icon": "📹",
        "description": "Transforms long podcasts and keynotes into viral Reels, Shorts, and clips with kinetic subtitles.",
        "key_tools": ["CapCut", "Descript", "OpusClip"],
        "suggested_skills": ["video editing", "color grading", "motion design", "upscaling"]
    },
    {
        "id": "ai_marketing_strategist",
        "name": "AI Marketing Strategist",
        "role": "Audience Intelligence & Search Growth",
        "icon": "📈",
        "description": "Directs data-backed keyword research, trend discovery, and organic SEO authority for creator brands.",
        "key_tools": ["Semrush", "Surfer SEO", "BuzzSumo"],
        "suggested_skills": ["SEO optimization", "trend discovery", "prompt engineering", "brand identity"]
    }
]

MARKETPLACE_SOURCES = [
    {"name": "Kampus.VC", "url": "https://kampus.vc", "description": "Next-gen venture campus and AI creator ecosystem connecting university innovators with brands.", "badge": "Core Marketplace Partner"},
    {"name": "Buffer", "url": "https://buffer.com", "description": "Leading social media platform providing AI social content creation benchmarks.", "badge": "Research Benchmark"},
    {"name": "VEED.io", "url": "https://www.veed.io", "description": "Cloud video creation suite and reference authority on creator AI tool pipelines.", "badge": "Ecosystem Partner"},
    {"name": "Collabstr", "url": "https://collabstr.com", "description": "Public marketplace benchmarking creator pricing, deliverables, and sponsorship rates.", "badge": "Rate Benchmark"},
    {"name": "Upfluence", "url": "https://www.upfluence.com", "description": "Enterprise creator discovery and influencer relationship management platform.", "badge": "Discovery Partner"},
    {"name": "CreatorIQ", "url": "https://www.creatoriq.com", "description": "Global enterprise creator intelligence and end-to-end campaign measurement.", "badge": "Enterprise Benchmark"},
    {"name": "AspireIQ", "url": "https://creators.aspireiq.com", "description": "Community commerce and relationship platform linking top tier digital creators with brands.", "badge": "Network Reference"},
    {"name": "Wishlink", "url": "https://www.wishlink.com", "description": "Creator commerce platform empowering direct audience monetization and affiliate sales.", "badge": "Monetization Reference"},
    {"name": "Heepsy", "url": "https://www.heepsy.com", "description": "Comprehensive influencer search engine with authenticity scoring and audience metrics.", "badge": "Verification Benchmark"},
    {"name": "Qoruz", "url": "https://qoruz.com", "description": "Influencer marketing intelligence platform measuring regional creator reach and ROI.", "badge": "Regional Intelligence"}
]

@router.get("/meta", response_model=MetaResponse)
def get_meta():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category, category_name, commercial_use, url, description, popular_archetype 
        FROM tools ORDER BY name ASC
    """)
    tools = [Tool(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM skills ORDER BY name ASC")
    skills = [Skill(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT id, name FROM content_types ORDER BY name ASC")
    content_types = [ContentType(**dict(row)) for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT specialization FROM creators ORDER BY specialization ASC")
    specializations = [row["specialization"] for row in cursor.fetchall()]

    # Group counts by category
    cursor.execute("SELECT category, COUNT(*) as cnt FROM tools GROUP BY category")
    counts = {row["category"]: row["cnt"] for row in cursor.fetchall()}

    conn.close()

    tool_categories = []
    for cat_id, meta in CATEGORY_META.items():
        tool_categories.append(ToolCategory(
            id=cat_id,
            name=meta["name"],
            emoji=meta["emoji"],
            count=counts.get(cat_id, 0),
            archetype=meta.get("archetype")
        ))

    creator_archetypes = [CreatorArchetype(**item) for item in ARCHETYPES]
    marketplace_sources = [MarketplaceSource(**item) for item in MARKETPLACE_SOURCES]

    return MetaResponse(
        tools=tools,
        skills=skills,
        content_types=content_types,
        specializations=specializations,
        aspect_ratios=["16:9", "9:16", "1:1", "4:5"],
        commercial_use_options=["full_buyout", "social_only", "internal_only"],
        tool_categories=tool_categories,
        creator_archetypes=creator_archetypes,
        marketplace_sources=marketplace_sources
    )
