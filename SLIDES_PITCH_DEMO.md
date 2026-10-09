# GenCraft — AI Content Creator Marketplace 🏆
## Hackathon Demo Deck & Evaluator Presentation

**Challenge**: Challenge 2: AI Content Creator Marketplace (by Kampus.VC & byteXL HacXLerate 2026)  
**Live Platform Application**: [http://localhost:3000](http://localhost:3000)  
**API OpenAPI Auto-Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)  

---

## 📺 Slide Deck Summary (5 Core Slides)

### Slide 1: The Problem
> **Generative AI created a new tier of creators — but existing marketplaces fail them.**
> - Brands struggle to verify true AI capabilities beyond static images.
> - Workflows are hidden inside black-box prompts.
> - Commercial buyout terms for generative AI outputs are ambiguous.

### Slide 2: The GenCraft Solution
> **An AI-Native Marketplace built around toolchains, workflows, and explainable matching.**
> - **Generative Tool Stacks**: Tracks 250+ AI tools across 18 specialized categories.
> - **Workflow Transparency**: Every portfolio item documents multi-step tool pipelines (`Midjourney v6 ➔ Runway Gen-3 ➔ Topaz Video AI ➔ DaVinci Resolve`).
> - **Explainable Matching**: Automated 6-factor scoring engine matching creator toolsets to brand briefs.

### Slide 3: Core Platform Features
> 1. **Creator Onboarding & Starter Studio**: Personalized project recommendations & production checklists.
> 2. **AI Portfolio Management**: Rich video/art viewer with prompt notes, aspect ratios, and commercial buyout clearance.
> 3. **AI-Assisted Brief Builder**: Powered by Google Gemini LLM to convert rough ideas into structured campaign briefs.
> 4. **Verification Signals**: Visible trust badges for verified tool usage and documented workflows.
> 5. **Engagement Workflow**: Full lifecycle tracking from application pitch to delivery URLs, revisions, and simulated escrow release.

### Slide 4: Architecture & Tech Stack
> - **Frontend**: React + Vite + Tailwind CSS + Glassmorphism UI Design System.
> - **Backend**: Python FastAPI with SQLite database auto-seeded with 26 creators, 100+ portfolio items, 10 campaign briefs, and 7 brand profiles.
> - **AI & Matching**: Google Gemini REST API + 6-Factor weighted math engine.
> - **Auth & Security**: Dual-role JWT authentication in `httpOnly` cookies with OAuth state management.

### Slide 5: Live Demo & Verification
> - **Test Suite**: 19/19 Pytest integration tests passing clean (`python -m pytest backend/tests`).
> - **Production Build**: 0-error Vite build (`cd frontend && npm run build`).

---

## 🎬 3-Minute Evaluator Demo Script

### Step 1: 1-Click Demo Login Switcher (0:00 - 0:45)
1. Open [http://localhost:3000](http://localhost:3000).
2. Click **`⚡ 1-Click Demo Login`** in the top navigation bar or navigate to `/login`.
3. Select **Demo Creator** (`demo.creator@gencraft.demo`).
4. Notice the persistent top **Evaluator Demo Access Bar** allowing instant role toggling without logging out!

### Step 2: Creator Starter Studio & Portfolio CRUD (0:45 - 1:30)
1. In the Creator Dashboard, inspect the **Profile Completeness Checklist** (85% Complete).
2. View **Starter Studio Recommendations**:
   - Inspect the **Cinematic AI Microfilm** or **Product Advertisement** starter card.
   - Click **"Start Project"** to save progress.
   - Click **"Add Completed Work to Portfolio"** to open the **Portfolio Manager Modal**.
3. Fill out title, workflow (`Midjourney v6 -> Runway Gen-3 -> DaVinci Resolve`), select tools, and click **Publish Portfolio Item**.

### Step 3: Brand Brief Builder & Gemini AI Draft (1:30 - 2:15)
1. Click **`⚡ Switch Persona: Demo Brand`** in the top Evaluator Bar.
2. Navigate to **Campaign Briefs** ➔ **`+ Post New Campaign Brief`** (`/briefs/new`).
3. Under **AI-Assisted Brief Builder**, type: *"We need a luxury electric vehicle teaser for social reels with neon lighting and energetic music"*.
4. Click **`✨ Draft Brief with Gemini AI`**.
5. Watch as the AI populates title, campaign goal, content format, aspect ratio (16:9), deliverables count, budget bounds (₹25,000 - ₹75,000), and required tools.
6. Click **`🚀 Review & Publish Brief`**.

### Step 4: Search, Filtering & Explainable Match Scoring (2:15 - 3:00)
1. Navigate to **Creators Directory** (`/creators`).
2. Filter creators by tools (`Midjourney v6`, `Runway Gen-3`) or specialization (`AI Filmmaker`).
3. Click **`🧪 No-Match Test Case`** in the sidebar to verify the zero-result state, loading skeletons, and 1-click filter reset!
4. Click on any brief or creator card to view the **6-Factor Match Breakdown Modal** and test the **Engagement Workflow** (`Apply` ➔ `Shortlist` ➔ `Accept` ➔ `Deliver` ➔ `Payment Released`).
