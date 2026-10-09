-- AI Content Creator Marketplace: SQLite schema
PRAGMA foreign_keys = ON;

-- ---------- Reference data ----------
CREATE TABLE tools (
    id               INTEGER PRIMARY KEY,
    name             TEXT NOT NULL UNIQUE,
    category         TEXT NOT NULL CHECK (category IN ('video','image','audio','editing','3d','avatar')),
    commercial_use   TEXT NOT NULL CHECK (commercial_use IN ('yes','plan_dependent')),
    url              TEXT
);

CREATE TABLE skills (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE content_types (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

-- ---------- Creators ----------
CREATE TABLE creators (
    id                    TEXT PRIMARY KEY,           -- e.g. cr_001
    name                  TEXT NOT NULL,
    headline              TEXT,
    bio                   TEXT,
    location              TEXT,
    avatar_url            TEXT,
    specialization        TEXT NOT NULL,
    experience_level      TEXT NOT NULL CHECK (experience_level IN ('junior','mid','senior')),
    rate_min_inr          INTEGER,                    -- per project
    rate_max_inr          INTEGER,
    availability          TEXT NOT NULL CHECK (availability IN ('available','busy')),
    languages             TEXT,                       -- comma separated
    -- verification signals (bonus)
    tools_verified        INTEGER NOT NULL DEFAULT 0 CHECK (tools_verified IN (0,1)),
    workflow_documented   INTEGER NOT NULL DEFAULT 0 CHECK (workflow_documented IN (0,1)),
    past_work_linked      INTEGER NOT NULL DEFAULT 0 CHECK (past_work_linked IN (0,1)),
    created_at            TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE creator_tools (
    creator_id TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    tool_id    INTEGER NOT NULL REFERENCES tools(id),
    PRIMARY KEY (creator_id, tool_id)
);

CREATE TABLE creator_skills (
    creator_id TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    skill_id   INTEGER NOT NULL REFERENCES skills(id),
    PRIMARY KEY (creator_id, skill_id)
);

CREATE TABLE creator_content_types (
    creator_id      TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    content_type_id INTEGER NOT NULL REFERENCES content_types(id),
    PRIMARY KEY (creator_id, content_type_id)
);

-- ---------- Portfolio ----------
CREATE TABLE portfolio_items (
    id               TEXT PRIMARY KEY,                -- e.g. pf_0001
    creator_id       TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
    title            TEXT NOT NULL,
    media_type       TEXT NOT NULL CHECK (media_type IN ('video','animation','image')),
    content_type_id  INTEGER REFERENCES content_types(id),
    media_url        TEXT,                            -- placeholder / royalty-free
    thumbnail_url    TEXT,
    duration_sec     INTEGER,                         -- NULL for images
    aspect_ratio     TEXT,                            -- 16:9, 9:16, 1:1, 4:5
    workflow         TEXT,                            -- "Midjourney -> Runway -> DaVinci"
    process_notes    TEXT,
    client_name      TEXT,                            -- fictional
    commercial_use   TEXT NOT NULL CHECK (commercial_use IN ('cleared','pending','personal_only')),
    year             INTEGER
);

CREATE TABLE portfolio_item_tools (
    item_id TEXT NOT NULL REFERENCES portfolio_items(id) ON DELETE CASCADE,
    tool_id INTEGER NOT NULL REFERENCES tools(id),
    PRIMARY KEY (item_id, tool_id)
);

-- ---------- Brands and briefs ----------
CREATE TABLE brands (
    id           TEXT PRIMARY KEY,                    -- e.g. br_01
    name         TEXT NOT NULL,
    industry     TEXT,
    description  TEXT,
    logo_url     TEXT,
    is_agency    INTEGER NOT NULL DEFAULT 0 CHECK (is_agency IN (0,1))
);

CREATE TABLE briefs (
    id                    TEXT PRIMARY KEY,           -- e.g. bf_01
    brand_id              TEXT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
    title                 TEXT NOT NULL,
    campaign_goal         TEXT,
    description           TEXT,
    content_type_id       INTEGER NOT NULL REFERENCES content_types(id),
    style                 TEXT,
    aspect_ratio          TEXT,
    duration_sec          INTEGER,
    deliverables_count    INTEGER DEFAULT 1,
    budget_min_inr        INTEGER,
    budget_max_inr        INTEGER,
    deadline              TEXT,                       -- ISO date
    commercial_use        TEXT NOT NULL CHECK (commercial_use IN ('full_buyout','social_only','internal_only')),
    usage_region          TEXT,
    status                TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open','in_review','closed')),
    created_at            TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE brief_required_tools (
    brief_id TEXT NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    tool_id  INTEGER NOT NULL REFERENCES tools(id),
    PRIMARY KEY (brief_id, tool_id)
);

CREATE TABLE brief_required_skills (
    brief_id TEXT NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
    skill_id INTEGER NOT NULL REFERENCES skills(id),
    PRIMARY KEY (brief_id, skill_id)
);

-- ---------- Authentication & Users ----------
CREATE TABLE users (
    id            TEXT PRIMARY KEY,                  -- e.g. usr_001
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT,                              -- bcrypt hash or NULL for OAuth
    role          TEXT NOT NULL CHECK (role IN ('creator','brand')),
    creator_id    TEXT REFERENCES creators(id) ON DELETE SET NULL,
    brand_id      TEXT REFERENCES brands(id) ON DELETE SET NULL,
    display_name  TEXT,
    avatar_url    TEXT,
    created_at    TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE oauth_accounts (
    id               TEXT PRIMARY KEY,               -- e.g. oa_001
    user_id          TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider         TEXT NOT NULL,                  -- 'google', 'facebook', 'instagram'
    provider_user_id TEXT NOT NULL,
    email            TEXT,
    created_at       TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_user_id)
);

-- ---------- Indexes for search / filter / auth ----------
CREATE INDEX idx_creator_tools_tool     ON creator_tools(tool_id);
CREATE INDEX idx_creator_skills_skill   ON creator_skills(skill_id);
CREATE INDEX idx_creator_ct_ct          ON creator_content_types(content_type_id);
CREATE INDEX idx_creators_spec          ON creators(specialization);
CREATE INDEX idx_portfolio_creator      ON portfolio_items(creator_id);
CREATE INDEX idx_briefs_status          ON briefs(status);
CREATE INDEX idx_users_email            ON users(email);
CREATE INDEX idx_users_creator          ON users(creator_id);
CREATE INDEX idx_users_brand            ON users(brand_id);
CREATE INDEX idx_oauth_user             ON oauth_accounts(user_id);

