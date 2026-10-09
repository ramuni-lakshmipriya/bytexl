# GenCraft — AI Content Creator Marketplace
## Data Model & Technical Specification Document

**Challenge**: Challenge 2: AI Content Creator Marketplace (by Kampus.VC & byteXL HacXLerate 2026)  
**Authors**: GenCraft Team  
**System Architecture**: FastAPI (Python 3.13) + SQLite + React (Vite / Tailwind CSS) + Google Gemini LLM API  

---

## 1. Executive Summary & Core Approach

GenCraft is an AI-native creator marketplace engineered specifically for generative workflows. Traditional freelance platforms fail AI creators because they treat video and visual production as traditional manual labor. GenCraft bridges this gap by structuring creator capabilities around:
1. **Generative Stack & Toolchain Transparency**: Tracking 250+ AI tools across 18 categories (Midjourney, Runway Gen-3, FLUX, ElevenLabs, ComfyUI, Kling, etc.).
2. **Workflow & Prompt Documentation**: Requiring explicit multi-step generative production pipelines (e.g. `Midjourney v6 Keyframes ➔ Runway Gen-3 Animation ➔ Topaz Video AI Upscaling ➔ DaVinci Resolve Color Grade`).
3. **Commercial Clearance & Licensing**: Direct tracking of full buyouts, social marketing rights, and model license parameters.
4. **6-Factor Explainable Match Engine**: Automated 0–100% match scoring linking campaign brief specifications with creator toolsets, skills, budget bounds, format compatibility, and verified signals.

---

## 2. Comprehensive Data Models

### A. Creator Profile Schema (`creators` & associated tables)

```sql
CREATE TABLE creators (
    id                    TEXT PRIMARY KEY,           -- e.g. cr_001
    name                  TEXT NOT NULL,
    headline              TEXT,                       -- Professional AI Headline
    bio                   TEXT,                       -- Creative vision & methodology
    location              TEXT,                       -- City, Country / Remote
    avatar_url            TEXT,
    specialization        TEXT NOT NULL,              -- AI Filmmaker, Animator, Generative Artist, etc.
    experience_level      TEXT NOT NULL CHECK (experience_level IN ('junior','mid','senior')),
    rate_min_inr          INTEGER,                    -- Min rate per project (INR)
    rate_max_inr          INTEGER,                    -- Max rate per project (INR)
    availability          TEXT NOT NULL CHECK (availability IN ('available','busy')),
    languages             TEXT,                       -- Comma-separated languages
    tools_verified        INTEGER NOT NULL DEFAULT 0, -- Trust Signal 1 (0/1)
    workflow_documented   INTEGER NOT NULL DEFAULT 0, -- Trust Signal 2 (0/1)
    past_work_linked      INTEGER NOT NULL DEFAULT 0, -- Trust Signal 3 (0/1)
    created_at            TEXT DEFAULT CURRENT_TIMESTAMP
);
```

- **M2M Tool Mapping (`creator_tools`)**: `(creator_id, tool_id)`
- **M2M Skill Mapping (`creator_skills`)**: `(creator_id, skill_id)`
- **M2M Format Mapping (`creator_content_types`)**: `(creator_id, content_type_id)`

---

### B. AI Portfolio Item Schema (`portfolio_items`)

```sql
CREATE TABLE portfolio_items (
    id               TEXT PRIMARY KEY,                -- e.g. pf_0001
    creator_id       TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    title            TEXT NOT NULL,
    media_type       TEXT NOT NULL CHECK (media_type IN ('video','animation','image')),
    content_type_id  INTEGER REFERENCES content_types(id),
    media_url        TEXT,                            -- High-res media / MP4 stream
    thumbnail_url    TEXT,                            -- Cover frame thumbnail
    duration_sec     INTEGER,                         -- Length in seconds (NULL for static images)
    aspect_ratio     TEXT,                            -- 16:9, 9:16, 1:1, 4:5
    workflow         TEXT,                            -- Multi-step tool pipeline string
    process_notes    TEXT,                            -- Prompt parameters, LoRA weights, seed notes
    client_name      TEXT,                            -- Client or spec project name
    commercial_use   TEXT NOT NULL CHECK (commercial_use IN ('cleared','pending','personal_only')),
    year             INTEGER
);
```

- **M2M Portfolio Tools (`portfolio_item_tools`)**: `(item_id, tool_id)`

---

### C. Campaign Brief Schema (`briefs`)

```sql
CREATE TABLE briefs (
    id                    TEXT PRIMARY KEY,           -- e.g. bf_001
    brand_id              TEXT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    title                 TEXT NOT NULL,
    campaign_goal         TEXT,                       -- Business goal & target audience
    description           TEXT,                       -- Creative direction
    content_type_id       INTEGER NOT NULL REFERENCES content_types(id),
    style                 TEXT,                       -- Visual aesthetic style
    aspect_ratio          TEXT,                       -- 16:9, 9:16, 1:1, 4:5
    duration_sec          INTEGER,
    deliverables_count    INTEGER DEFAULT 1,
    budget_min_inr        INTEGER,
    budget_max_inr        INTEGER,
    deadline              TEXT,                       -- ISO date
    commercial_use        TEXT NOT NULL CHECK (commercial_use IN ('full_buyout','social_only','internal_only')),
    usage_region          TEXT,                       -- Global / Regional
    status                TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','in_review','closed')),
    created_at            TEXT DEFAULT CURRENT_TIMESTAMP
);
```

- **Brief Tool Requirements (`brief_required_tools`)**: `(brief_id, tool_id)`
- **Brief Skill Requirements (`brief_required_skills`)**: `(brief_id, skill_id)`

---

### D. Engagement & Delivery Schema (`brief_applications`)

```sql
CREATE TABLE brief_applications (
    id                 TEXT PRIMARY KEY,
    brief_id           TEXT NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    creator_id         TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    pitch              TEXT,                          -- Pitch proposal & technical approach
    proposed_rate_inr  INTEGER,
    estimated_days     INTEGER,
    status             TEXT NOT NULL DEFAULT 'applied' CHECK (status IN ('applied','shortlisted','accepted','in_progress','delivered','completed','revision_requested','rejected')),
    delivery_url       TEXT,                          -- Submitted delivery media link
    delivery_notes     TEXT,                          -- Keyframe & prompt log notes
    revision_feedback  TEXT,                          -- Brand revision feedback
    payment_status     TEXT DEFAULT 'escrow_held' CHECK (payment_status IN ('escrow_pending','escrow_held','payment_released')),
    created_at         TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at         TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(brief_id, creator_id)
);
```

---

## 3. Reference Data & Vocabularies

### 18 AI Tool Categories (250+ Master Tools)
1. **Writing & Scripts**: ChatGPT, Claude, Gemini, Jasper
2. **AI Image Generation**: Midjourney v6, DALL-E 3, Adobe Firefly, FLUX.1, Leonardo AI, ComfyUI
3. **AI Video & Motion**: Runway Gen-3, Luma Dream Machine, Sora, Kling AI, Pika 1.5, Hailuo AI
4. **AI Audio & Voice**: ElevenLabs, Udio, Suno, Topaz Audio
5. **3D & Asset Synthesis**: Luma Genie, Meshy, Spline AI, Tripo3D
6. **Upscaling & Enhancement**: Topaz Video AI, Magnific AI, Krea AI
*(Full list seeded in `dataset/seed.py` across all 18 categories)*

### Commercial-Use & Licensing Terms
- `full_buyout`: Complete transfer of commercial rights for global broadcast and digital ads.
- `social_only`: Restricted to social media channels (Instagram, TikTok, YouTube Shorts).
- `internal_only`: Non-broadcast internal corporate or spec use.

---

## 4. Algorithmic Match Engine & Scoring Formula

Matches between creators and briefs are scored from **0 to 100 Points** using a 6-Factor weighted engine:

$$\text{Total Score} = S_{\text{tools}} (30) + S_{\text{skills}} (30) + S_{\text{format}} (15) + S_{\text{budget}} (15) + S_{\text{avail}} (5) + S_{\text{verif}} (5)$$

1. **Required Tool Overlap (30 Points)**:
   $$\left(\frac{\text{Matched Tools}}{\text{Brief Required Tools}}\right) \times 30$$
2. **Required Skill Overlap (30 Points)**:
   $$\left(\frac{\text{Matched Skills}}{\text{Brief Required Skills}}\right) \times 30$$
3. **Content Format Fit (15 Points)**: 15 pts if content format matches creator specialization.
4. **Budget Alignment (15 Points)**: 15 pts for complete fit within budget bounds; 10 pts for range overlap.
5. **Availability Status (5 Points)**: 5 pts if 'available'.
6. **Verification Signals (5 Points)**: Up to 5 pts based on verified tool usage and documented workflows.

---

## 5. Verification Signals & Trust Architecture

Visible trust badges display on creator cards and portfolio modals:
- **Tools Verified**: Validated through documented past project outputs.
- **Workflow Documented**: Detailed multi-step generation notes and tool pipelines provided.
- **Past Work Linked**: Verified external portfolio reels or commercial client links.
- **Commercial Rights Confirmed**: Explicit license clearance declaration.

---

## 6. AI-Assisted Brief Builder (Gemini LLM Integration)

Brands can enter a rough prompt (e.g., *"We need a futuristic electric SUV teaser for social reels with neon lighting and high energy music"*).
1. `POST /briefs/draft` calls Google Gemini LLM via REST API.
2. Formats prompt into structured JSON (Title, Campaign Goal, Content Type ID, Style, Aspect Ratio, Budget Bounds, Deadline, Required Tool IDs, Required Skill IDs).
3. Provides rule-based deterministic fallback if API key is unconfigured.
4. Requires brand review & approval before posting.
