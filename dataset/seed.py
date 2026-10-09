#!/usr/bin/env python3
"""
Seed script for the AI Content Creator Marketplace.

Usage:
    python seed.py                 # creates/resets marketplace.db next to this file
    python seed.py --db my.db      # custom DB path

All data is synthetic. Brands are fictional. Media URLs are royalty-free
placeholders (picsum.photos); replace them with your own hosted clips/images.
Running the script again wipes and rebuilds the database (one-command reset).
"""
import argparse
import os
import random
import sqlite3

random.seed(42)  # deterministic: everyone on the team gets identical data

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# Reference data
# --------------------------------------------------------------------------
# (name, category, commercial_use, url). Licence terms change often, so the
# UI should say "check current plan terms" rather than promise anything.
TOOLS = [
    ("Midjourney", "image", "plan_dependent", "https://www.midjourney.com"),
    ("Runway", "video", "yes", "https://runwayml.com"),
    ("Sora", "video", "plan_dependent", "https://openai.com/sora"),
    ("Veo", "video", "plan_dependent", "https://deepmind.google/models/veo/"),
    ("Pika", "video", "plan_dependent", "https://pika.art"),
    ("Kling", "video", "plan_dependent", "https://klingai.com"),
    ("Luma Dream Machine", "video", "plan_dependent", "https://lumalabs.ai"),
    ("Stable Diffusion", "image", "yes", "https://stability.ai"),
    ("ComfyUI", "image", "yes", "https://www.comfy.org"),
    ("Adobe Firefly", "image", "yes", "https://firefly.adobe.com"),
    ("Leonardo AI", "image", "plan_dependent", "https://leonardo.ai"),
    ("ElevenLabs", "audio", "plan_dependent", "https://elevenlabs.io"),
    ("Suno", "audio", "plan_dependent", "https://suno.com"),
    ("HeyGen", "avatar", "plan_dependent", "https://www.heygen.com"),
    ("DaVinci Resolve", "editing", "yes", "https://www.blackmagicdesign.com"),
    ("After Effects", "editing", "yes", "https://www.adobe.com/products/aftereffects.html"),
    ("Topaz Video AI", "editing", "yes", "https://www.topazlabs.com"),
    ("Blender", "3d", "yes", "https://www.blender.org"),
]

SKILLS = [
    "storyboarding", "prompt engineering", "motion design", "color grading",
    "sound design", "voice cloning", "3D modeling", "lip sync",
    "character design", "video editing", "scriptwriting", "upscaling",
    "LoRA training", "VFX compositing", "typography", "brand identity",
    "product photography", "camera direction", "music composition", "localization",
]

CONTENT_TYPES = [
    "short film", "ad spot", "music video", "social reel", "product visual",
    "explainer", "animation loop", "poster/graphic", "logo animation", "game cinematic",
]

# content type -> (media_type, aspect ratios to choose from, duration range or None)
CT_PROFILE = {
    "short film":      ("video",     ["16:9", "16:9", "9:16"], (45, 180)),
    "ad spot":         ("video",     ["16:9", "9:16", "1:1"],  (15, 45)),
    "music video":     ("video",     ["16:9", "16:9", "9:16"], (60, 200)),
    "social reel":     ("video",     ["9:16", "9:16", "1:1"],  (8, 30)),
    "product visual":  ("image",     ["1:1", "4:5", "16:9"],   None),
    "explainer":       ("video",     ["16:9", "16:9", "1:1"],  (40, 120)),
    "animation loop":  ("animation", ["1:1", "16:9", "9:16"],  (4, 15)),
    "poster/graphic":  ("image",     ["4:5", "1:1", "16:9"],   None),
    "logo animation":  ("animation", ["1:1", "16:9"],          (3, 8)),
    "game cinematic":  ("animation", ["16:9", "16:9"],         (30, 90)),
}

# --------------------------------------------------------------------------
# Creators
# (name, specialization, headline, location, level, rate_min, rate_max,
#  availability, languages, (tools_verified, workflow_documented, past_work_linked),
#  skills, tools, content_types)
# Rates are in INR per project.
# --------------------------------------------------------------------------
CREATORS = [
    ("Ananya Rao", "AI Filmmaker", "Short films and ad spots with cinematic AI pipelines", "Hyderabad, IN", "senior", 40000, 120000, "available", ["English", "Telugu", "Hindi"], (1, 1, 0),
     ["storyboarding", "motion design", "prompt engineering", "color grading"], ["Runway", "Midjourney", "DaVinci Resolve"], ["short film", "ad spot"]),
    ("Rohan Mehta", "AI Ad Creative", "Scroll-stopping social reels for D2C brands", "Mumbai, IN", "mid", 15000, 45000, "available", ["English", "Hindi"], (1, 1, 1),
     ["prompt engineering", "video editing", "scriptwriting", "localization"], ["Pika", "Kling", "ElevenLabs", "Adobe Firefly"], ["social reel", "ad spot"]),
    ("Sara Lindqvist", "AI Animator", "Stylised character animation with Stable Diffusion and ComfyUI", "Stockholm, SE", "senior", 60000, 180000, "busy", ["English", "Swedish"], (1, 1, 1),
     ["character design", "motion design", "LoRA training", "VFX compositing"], ["ComfyUI", "Stable Diffusion", "After Effects", "Topaz Video AI"], ["animation loop", "explainer", "short film"]),
    ("Kiran Reddy", "Generative Graphics Artist", "Posters and brand visuals for local businesses", "Vijayawada, IN", "junior", 5000, 20000, "available", ["English", "Telugu"], (0, 0, 1),
     ["typography", "brand identity", "prompt engineering"], ["Midjourney", "Leonardo AI", "Adobe Firefly"], ["poster/graphic", "product visual"]),
    ("Meera Nair", "AI Music Video Director", "Dreamlike music videos for indie artists", "Kochi, IN", "mid", 30000, 90000, "available", ["English", "Malayalam", "Hindi"], (1, 0, 1),
     ["camera direction", "color grading", "storyboarding", "music composition"], ["Runway", "Suno", "DaVinci Resolve", "Midjourney"], ["music video", "social reel"]),
    ("Daniel Okafor", "AI Filmmaker", "Narrative shorts built on Sora and Veo", "Lagos, NG", "mid", 35000, 100000, "available", ["English"], (1, 1, 0),
     ["storyboarding", "camera direction", "scriptwriting", "prompt engineering"], ["Sora", "Veo", "DaVinci Resolve"], ["short film", "ad spot"]),
    ("Priya Sharma", "Product Visualization", "Photoreal product shots, AI plus 3D", "Bengaluru, IN", "senior", 45000, 130000, "available", ["English", "Hindi", "Kannada"], (1, 1, 1),
     ["3D modeling", "product photography", "VFX compositing", "upscaling"], ["Blender", "Stable Diffusion", "ComfyUI", "Topaz Video AI"], ["product visual", "ad spot"]),
    ("Liam Chen", "AI Animator", "Fast, stylised animation for explainers and social", "Singapore, SG", "mid", 35000, 95000, "busy", ["English", "Mandarin"], (1, 0, 1),
     ["character design", "motion design", "lip sync"], ["Kling", "Luma Dream Machine", "After Effects", "HeyGen"], ["animation loop", "explainer", "social reel"]),
    ("Fatima Khan", "AI Explainer Producer", "Explainer videos with synthetic presenters", "Delhi, IN", "mid", 20000, 60000, "available", ["English", "Hindi", "Urdu"], (1, 1, 0),
     ["scriptwriting", "voice cloning", "localization", "lip sync"], ["HeyGen", "ElevenLabs", "Runway"], ["explainer", "social reel"]),
    ("Arjun Patel", "Motion Graphics", "Logo stings and kinetic type with a generative twist", "Ahmedabad, IN", "mid", 20000, 55000, "available", ["English", "Gujarati", "Hindi"], (0, 1, 1),
     ["motion design", "typography", "brand identity", "video editing"], ["After Effects", "Midjourney", "Adobe Firefly"], ["logo animation", "ad spot"]),
    ("Chloe Martin", "AI Filmmaker", "Festival-style short films and game cinematics", "Lyon, FR", "senior", 80000, 220000, "busy", ["English", "French"], (1, 1, 1),
     ["storyboarding", "camera direction", "VFX compositing", "color grading"], ["Runway", "Luma Dream Machine", "DaVinci Resolve", "Topaz Video AI"], ["short film", "game cinematic", "music video"]),
    ("Vikram Singh", "Character Designer", "Concept characters and game-ready art", "Jaipur, IN", "junior", 8000, 30000, "available", ["English", "Hindi"], (0, 0, 1),
     ["character design", "LoRA training", "prompt engineering"], ["Stable Diffusion", "Leonardo AI"], ["poster/graphic", "game cinematic"]),
    ("Isabella Rossi", "Generative Graphics Artist", "Editorial-grade brand imagery", "Milan, IT", "mid", 25000, 80000, "available", ["English", "Italian"], (1, 1, 0),
     ["typography", "brand identity", "product photography"], ["Midjourney", "Adobe Firefly"], ["poster/graphic", "product visual"]),
    ("Tanvi Joshi", "AI Ad Creative", "Regional-language ads that feel local", "Pune, IN", "mid", 18000, 50000, "available", ["English", "Hindi", "Marathi"], (1, 0, 0),
     ["scriptwriting", "localization", "voice cloning", "video editing"], ["Pika", "ElevenLabs", "HeyGen"], ["ad spot", "social reel"]),
    ("Omar Haddad", "AI Music Video Director", "Cinematic music videos with full audio pipeline", "Dubai, AE", "senior", 70000, 200000, "available", ["English", "Arabic"], (1, 1, 1),
     ["music composition", "camera direction", "sound design", "VFX compositing"], ["Veo", "Suno", "ElevenLabs", "DaVinci Resolve"], ["music video", "short film"]),
    ("Nisha Kulkarni", "AI Animator", "Hand-drawn feel, AI-accelerated", "Chennai, IN", "mid", 22000, 65000, "available", ["English", "Tamil"], (0, 1, 1),
     ["character design", "motion design", "storyboarding"], ["Pika", "Stable Diffusion", "After Effects"], ["animation loop", "short film"]),
    ("Sebastian Weber", "Product Visualization", "Automotive and appliance visuals", "Berlin, DE", "senior", 60000, 160000, "busy", ["English", "German"], (1, 1, 0),
     ["3D modeling", "VFX compositing", "upscaling"], ["Blender", "ComfyUI", "Topaz Video AI"], ["product visual", "ad spot"]),
    ("Harsha Vardhan", "AI Filmmaker", "Telugu short films and reels", "Guntur, IN", "junior", 6000, 25000, "available", ["English", "Telugu"], (0, 0, 1),
     ["storyboarding", "video editing", "prompt engineering"], ["Runway", "Kling"], ["short film", "social reel"]),
    ("Zoe Williams", "AI Ad Creative", "Premium ad campaigns, concept to final grade", "London, UK", "senior", 90000, 250000, "available", ["English"], (1, 1, 1),
     ["scriptwriting", "camera direction", "color grading", "prompt engineering"], ["Sora", "Runway", "DaVinci Resolve", "ElevenLabs"], ["ad spot", "short film"]),
    ("Aditya Menon", "Motion Graphics", "Motion design student turned freelancer", "Trivandrum, IN", "junior", 7000, 22000, "available", ["English", "Malayalam"], (0, 0, 0),
     ["motion design", "typography"], ["After Effects", "Leonardo AI"], ["logo animation", "social reel"]),
    ("Yuki Tanaka", "Character Designer", "Anime-inspired characters, from concept to 3D", "Tokyo, JP", "senior", 55000, 150000, "busy", ["English", "Japanese"], (1, 1, 1),
     ["character design", "LoRA training", "3D modeling", "lip sync"], ["ComfyUI", "Stable Diffusion", "Blender", "Kling"], ["game cinematic", "animation loop"]),
    ("Pooja Iyer", "AI Explainer Producer", "Multilingual explainers with clean voiceover", "Bengaluru, IN", "mid", 18000, 48000, "available", ["English", "Tamil", "Kannada"], (1, 0, 1),
     ["scriptwriting", "voice cloning", "localization", "sound design"], ["ElevenLabs", "HeyGen", "Suno"], ["explainer", "social reel"]),
    # Awkward record: only one tool
    ("Marcus Johnson", "Generative Graphics Artist", "Midjourney specialist", "Austin, US", "mid", 30000, 85000, "available", ["English"], (1, 0, 1),
     ["typography", "upscaling", "brand identity"], ["Midjourney"], ["poster/graphic"]),
    # Awkward record: no portfolio yet
    ("Neha Gupta", "AI Filmmaker", "New to AI film, building a first portfolio", "Noida, IN", "junior", 5000, 18000, "available", ["English", "Hindi"], (0, 0, 0),
     ["storyboarding", "scriptwriting"], ["Runway"], ["short film"]),
    # Awkward record: very long bio and many tools
    ("Elena Petrova", "AI Animator", "Experimental animation researcher and director", "Prague, CZ", "senior", 75000, 210000, "busy", ["English", "Czech", "Russian"], (1, 1, 1),
     ["character design", "motion design", "LoRA training", "VFX compositing", "color grading", "storyboarding", "upscaling"],
     ["Stable Diffusion", "ComfyUI", "After Effects", "DaVinci Resolve", "Blender", "Topaz Video AI", "Runway", "Midjourney"],
     ["animation loop", "short film", "game cinematic", "music video"]),
    ("Imran Sheikh", "AI Music Video Director", "Multilingual music videos, Telugu to Urdu", "Hyderabad, IN", "mid", 25000, 70000, "available", ["English", "Hindi", "Telugu", "Urdu"], (1, 1, 0),
     ["music composition", "sound design", "video editing", "color grading"], ["Suno", "Runway", "DaVinci Resolve", "Pika"], ["music video", "social reel"]),
]

LONG_BIO = (
    "Elena has spent over a decade at the edge of animation and machine learning. She began as a traditional "
    "2D animator, moved into compositing for feature films, and turned to generative models early, training "
    "custom LoRAs on her own hand-drawn frames so that style stays consistent across hundreds of shots. Her "
    "pipeline combines Stable Diffusion and ComfyUI for look development, Blender for layout and camera, "
    "Runway for motion passes, and After Effects and DaVinci Resolve for final compositing and grade, with "
    "Topaz for upscaling. She documents every project step by step, publishes her node graphs, and mentors "
    "junior artists on keeping human direction at the centre of AI-assisted work. She is selective about "
    "commissions and prefers long-form collaborations with clear creative briefs."
)

THEMES = [
    "Monsoon Chai", "Neon Sneaker Drop", "Aurora Coffee", "Desert Rail Journey", "Lotus Skincare",
    "Pixel Garden", "Midnight Metro", "Solar Bikes", "Saffron and Salt", "Orbit Fitness",
    "Velvet Sound", "Paper Lanterns", "Coastal Escape", "Urban Bloom", "Retro Arcade",
]
FICTIONAL_CLIENTS = [
    "Chaiwala Co", "StrideLab", "Aurora Roasters", "Rail Odyssey", "Lotus & Loom",
    "Pixel Patch Studio", "Metroline", "Solara Bikes", "Saffron Table", "Orbit Fitness",
    None, None,  # some portfolio items have no client (personal work)
]
PROCESS_NOTES = [
    "Generated 40+ keyframes, curated 12, then animated and graded.",
    "Consistent character via reference images and a trained LoRA.",
    "Prompts iterated over three rounds with client feedback.",
    "Hybrid: AI base plates, manual compositing for final polish.",
    "Audio generated separately and synced in the edit.",
    "Upscaled to 4K and denoised before delivery.",
]

# --------------------------------------------------------------------------
# Brands and briefs (all fictional)
# --------------------------------------------------------------------------
BRANDS = [
    ("br_01", "Lotus & Loom", "Skincare", "Ayurveda-inspired skincare for everyday routines.", 0),
    ("br_02", "Orbit Fitness", "Fitness app", "Subscription fitness app with live classes.", 0),
    ("br_03", "Saffron Table", "Food and beverage", "Regional restaurant chain across South India.", 0),
    ("br_04", "Solara Bikes", "Electric mobility", "Affordable electric bikes for city commuters.", 0),
    ("br_05", "Velvet Sound", "Music streaming", "Independent-artist-first streaming platform.", 0),
    ("br_06", "Paperlane Games", "Gaming", "Indie studio building narrative fantasy RPGs.", 0),
    ("br_07", "Northwind Creative", "Advertising agency", "Boutique agency running campaigns for D2C brands.", 1),
]

# (id, brand, title, goal, content_type, style, ratio, duration, deliverables,
#  budget_min, budget_max, deadline, commercial_use, region, status, tools, skills, description)
BRIEFS = [
    ("bf_01", "br_01", "Monsoon Glow skincare reel", "Awareness for new monsoon range", "social reel", "soft, dewy, minimalist", "9:16", 20, 3, 15000, 40000,
     "2026-11-10", "social_only", "India", "open", ["Kling", "Pika"], ["prompt engineering", "color grading"],
     "Three short reels showing the monsoon range with calm, water-themed visuals."),
    ("bf_02", "br_02", "App launch 30s ad", "Drive installs at launch", "ad spot", "high-energy, neon", "16:9", 30, 1, 40000, 90000,
     "2026-11-20", "full_buyout", "Global", "open", ["Runway", "Sora"], ["camera direction", "color grading"],
     "A single high-energy spot introducing live classes. Strong opening hook required."),
    ("bf_03", "br_03", "Festive menu explainer", "Explain the festive thali menu", "explainer", "warm, illustrated", "16:9", 60, 1, 20000, 50000,
     "2026-11-05", "social_only", "India", "open", ["HeyGen", "ElevenLabs"], ["scriptwriting", "localization"],
     "One-minute explainer in English and Telugu with a synthetic presenter."),
    ("bf_04", "br_04", "3D product reveal", "Reveal the new commuter model", "product visual", "clean, photoreal", "16:9", 15, 4, 50000, 120000,
     "2026-12-01", "full_buyout", "Global", "open", ["Blender", "ComfyUI"], ["3D modeling", "VFX compositing"],
     "Four hero visuals plus a short reveal animation of the new model."),
    ("bf_05", "br_05", "Single launch music video", "Launch a new artist single", "music video", "surreal, dreamy", "16:9", 120, 1, 60000, 150000,
     "2026-11-30", "full_buyout", "Global", "open", ["Runway", "Suno"], ["music composition", "camera direction"],
     "Two-minute music video; creator may also propose an AI-assisted soundtrack."),
    ("bf_06", "br_06", "Fantasy RPG cinematic trailer", "Announce the game", "game cinematic", "dark fantasy, painterly", "16:9", 45, 1, 70000, 180000,
     "2026-12-15", "full_buyout", "Global", "open", ["ComfyUI", "Stable Diffusion", "Blender"], ["character design", "VFX compositing"],
     "Announcement trailer with consistent characters across shots."),
    ("bf_07", "br_07", "Retro poster series", "Print and social poster set", "poster/graphic", "retro, bold typography", "4:5", None, 6, 12000, 30000,
     "2026-11-08", "full_buyout", "India", "open", ["Midjourney"], ["typography", "brand identity"],
     "Six posters in a consistent retro style for an out-of-home campaign."),
    ("bf_08", "br_07", "Telugu festival greetings", "Festival greetings for client brands", "social reel", "festive, colourful", "9:16", 15, 5, 10000, 25000,
     "2026-10-30", "social_only", "India", "open", ["Pika", "ElevenLabs"], ["localization", "voice cloning"],
     "Five Telugu-language greeting reels with natural voiceover."),
    ("bf_09", "br_02", "Logo sting animation", "Refresh intro for class videos", "logo animation", "minimalist", "1:1", 5, 2, 8000, 20000,
     "2026-11-12", "full_buyout", "Global", "in_review", ["After Effects"], ["motion design", "typography"],
     "Two logo stings for class intros and social."),
    ("bf_10", "br_01", "Brand film (completed)", "Flagship brand film", "short film", "cinematic", "16:9", 90, 1, 80000, 160000,
     "2026-09-30", "full_buyout", "India", "closed", ["Runway", "Luma Dream Machine"], ["storyboarding", "color grading"],
     "Completed campaign kept as a closed example."),
]


# --------------------------------------------------------------------------
def build_db(db_path: str) -> None:
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = OFF")
    for (t,) in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    ).fetchall():
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.execute("PRAGMA foreign_keys = ON")
    with open(os.path.join(HERE, "schema.sql"), encoding="utf-8") as f:
        conn.executescript(f.read())
    cur = conn.cursor()

    # --- reference tables
    for name, cat, comm, url in TOOLS:
        cur.execute("INSERT INTO tools(name, category, commercial_use, url) VALUES (?,?,?,?)", (name, cat, comm, url))
    for s in SKILLS:
        cur.execute("INSERT INTO skills(name) VALUES (?)", (s,))
    for c in CONTENT_TYPES:
        cur.execute("INSERT INTO content_types(name) VALUES (?)", (c,))

    tool_id = {n: i for i, n in cur.execute("SELECT id, name FROM tools")}
    skill_id = {n: i for i, n in cur.execute("SELECT id, name FROM skills")}
    ct_id = {n: i for i, n in cur.execute("SELECT id, name FROM content_types")}

    # --- creators
    pf_counter = 0
    for idx, (name, spec, headline, loc, level, rmin, rmax, avail, langs, ver, skills, tools, cts) in enumerate(CREATORS, start=1):
        cid = f"cr_{idx:03d}"
        city = loc.split(",")[0]
        bio = LONG_BIO if name == "Elena Petrova" else (
            f"{name} is a {spec.lower()} based in {city}. {headline}. "
            f"Works with {', '.join(tools)} and speaks {', '.join(langs)}."
        )
        avatar = f"https://api.dicebear.com/7.x/shapes/svg?seed={name.replace(' ', '')}"
        cur.execute(
            """INSERT INTO creators(id,name,headline,bio,location,avatar_url,specialization,experience_level,
               rate_min_inr,rate_max_inr,availability,languages,tools_verified,workflow_documented,past_work_linked)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (cid, name, headline, bio, loc, avatar, spec, level, rmin, rmax, avail, ", ".join(langs), *ver),
        )
        for t in tools:
            cur.execute("INSERT INTO creator_tools VALUES (?,?)", (cid, tool_id[t]))
        for s in skills:
            cur.execute("INSERT INTO creator_skills VALUES (?,?)", (cid, skill_id[s]))
        for c in cts:
            cur.execute("INSERT INTO creator_content_types VALUES (?,?)", (cid, ct_id[c]))

        # --- portfolio items
        if name == "Neha Gupta":
            n_items = 0
        elif name == "Marcus Johnson":
            n_items = 3
        elif name == "Elena Petrova":
            n_items = 5
        else:
            n_items = random.randint(3, 5)

        for k in range(n_items):
            pf_counter += 1
            pid = f"pf_{pf_counter:04d}"
            ct = cts[k % len(cts)]
            media_type, ratios, dur = CT_PROFILE[ct]
            ratio = random.choice(ratios)
            duration = random.randint(*dur) if dur else None
            used = random.sample(tools, k=min(len(tools), random.randint(1, 3)))
            workflow = " -> ".join(used)
            theme = random.choice(THEMES)
            client = random.choice(FICTIONAL_CLIENTS)
            commercial = random.choice(["cleared", "cleared", "cleared", "pending", "personal_only"])
            seed_key = f"{cid}{k}"
            cur.execute(
                """INSERT INTO portfolio_items(id,creator_id,title,media_type,content_type_id,media_url,thumbnail_url,
                   duration_sec,aspect_ratio,workflow,process_notes,client_name,commercial_use,year)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (pid, cid, f"{theme}: {ct}", media_type, ct_id[ct],
                 f"https://picsum.photos/seed/{seed_key}/1280/720",
                 f"https://picsum.photos/seed/{seed_key}/480/270",
                 duration, ratio, workflow, random.choice(PROCESS_NOTES), client, commercial,
                 random.choice([2024, 2025, 2026])),
            )
            for t in used:
                cur.execute("INSERT INTO portfolio_item_tools VALUES (?,?)", (pid, tool_id[t]))

    # --- brands
    for bid, name, industry, desc, agency in BRANDS:
        logo = f"https://api.dicebear.com/7.x/initials/svg?seed={name.replace(' ', '')}"
        cur.execute("INSERT INTO brands VALUES (?,?,?,?,?,?)", (bid, name, industry, desc, logo, agency))

    # --- briefs
    for (bfid, brand, title, goal, ct, style, ratio, dur, deliv, bmin, bmax, deadline,
         comm, region, status, tools, skills, desc) in BRIEFS:
        cur.execute(
            """INSERT INTO briefs(id,brand_id,title,campaign_goal,description,content_type_id,style,aspect_ratio,
               duration_sec,deliverables_count,budget_min_inr,budget_max_inr,deadline,commercial_use,usage_region,status)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (bfid, brand, title, goal, desc, ct_id[ct], style, ratio, dur, deliv, bmin, bmax, deadline, comm, region, status),
        )
        for t in tools:
            cur.execute("INSERT INTO brief_required_tools VALUES (?,?)", (bfid, tool_id[t]))
        for s in skills:
            cur.execute("INSERT INTO brief_required_skills VALUES (?,?)", (bfid, skill_id[s]))

    # --- users (demo users & creator/brand user accounts)
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    cr_pass_hash = pwd_context.hash("DemoCreator123!")
    br_pass_hash = pwd_context.hash("DemoBrand123!")
    default_pass_hash = pwd_context.hash("Password123!")

    # 1. Demo Creator
    cur.execute("""
        INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
        VALUES (?, ?, ?, 'creator', 'cr_001', NULL, ?, ?)
    """, ("usr_demo_cr", "demo.creator@gencraft.demo", cr_pass_hash, "Ananya Rao (Demo Creator)", "https://picsum.photos/seed/cr_001/200"))

    # 2. Demo Brand
    cur.execute("""
        INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
        VALUES (?, ?, ?, 'brand', NULL, 'br_01', ?, ?)
    """, ("usr_demo_br", "demo.brand@gencraft.demo", br_pass_hash, "Lotus & Loom (Demo Brand)", "https://api.dicebear.com/7.x/initials/svg?seed=LotusLoom"))

    # 3. Seed users for remaining creators
    for i, cr_data in enumerate(CREATORS[1:], start=2):
        cid = f"cr_{i:03d}"
        c_name = cr_data[0]
        c_email = f"{c_name.lower().replace(' ', '.')}@creators.gencraft.demo"
        cur.execute("""
            INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
            VALUES (?, ?, ?, 'creator', ?, NULL, ?, ?)
        """, (f"usr_cr_{i:03d}", c_email, default_pass_hash, cid, c_name, f"https://picsum.photos/seed/{cid}/200"))

    # 4. Seed users for remaining brands
    for bid, b_name, industry, desc, is_agency in BRANDS[1:]:
        b_email = f"contact@{b_name.lower().replace(' ', '').replace('&', 'and')}.demo"
        cur.execute("""
            INSERT INTO users (id, email, password_hash, role, creator_id, brand_id, display_name, avatar_url)
            VALUES (?, ?, ?, 'brand', NULL, ?, ?, ?)
        """, (f"usr_{bid}", b_email, default_pass_hash, bid, b_name, f"https://api.dicebear.com/7.x/initials/svg?seed={b_name.replace(' ', '')}"))

    conn.commit()
    conn.close()


def report(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    q = lambda sql, *a: conn.execute(sql, a).fetchall()

    print(f"Seeded {db_path}")
    for table in ("tools", "skills", "content_types", "creators", "portfolio_items", "brands", "briefs", "users", "oauth_accounts"):
        print(f"  {table:<16} {q(f'SELECT COUNT(*) FROM {table}')[0][0]}")

    bad = q("PRAGMA foreign_key_check")
    print("  foreign key problems:", len(bad))

    # Demo filter checks
    def count(tools=(), skill=None):
        sql = "SELECT COUNT(DISTINCT c.id) FROM creators c WHERE 1=1"
        params = []
        for t in tools:
            sql += " AND EXISTS (SELECT 1 FROM creator_tools ct JOIN tools t ON t.id=ct.tool_id WHERE ct.creator_id=c.id AND t.name=?)"
            params.append(t)
        if skill:
            sql += " AND EXISTS (SELECT 1 FROM creator_skills cs JOIN skills s ON s.id=cs.skill_id WHERE cs.creator_id=c.id AND s.name=?)"
            params.append(skill)
        return conn.execute(sql, params).fetchone()[0]

    print("Demo filters:")
    print("  Midjourney                        ->", count(["Midjourney"]), "creators (common tool)")
    print("  ComfyUI                           ->", count(["ComfyUI"]), "creators (rarer tool)")
    print("  Sora + 3D modeling                ->", count(["Sora"], "3D modeling"), "creators (empty-state demo)")
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the marketplace database")
    parser.add_argument("--db", default=os.path.join(HERE, "marketplace.db"))
    args = parser.parse_args()
    build_db(args.db)
    report(args.db)
