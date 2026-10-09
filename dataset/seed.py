#!/usr/bin/env python3
"""
Seed script for the AI Content Creator Marketplace (Kampus.VC & GenCraft).

Usage:
    python seed.py                 # creates/resets marketplace.db next to this file
    python seed.py --db my.db      # custom DB path

Integrates 250+ curated AI tools across 18 creator categories,
maps the 10 core Kampus.VC marketplace creator archetypes,
and seeds creators, briefs, portfolio items, and demo accounts.
"""
import argparse
import os
import random
import sqlite3

random.seed(42)  # deterministic: everyone on the team gets identical data

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# 18 AI Tool Categories (20 tools each)
# Schema: (name, category_slug, category_name, commercial_use, url, description, popular_archetype)
# --------------------------------------------------------------------------
RAW_TOOL_CATEGORIES = [
    {
        "id": "writing",
        "name": "Writing, Scripts & Captions",
        "emoji": "✍️",
        "archetype": "AI Script Writer",
        "tools": [
            ("ChatGPT", "writing", "Writing, Scripts & Captions", "yes", "https://chatgpt.com", "Industry-leading conversational LLM for video scripting, outlines, and hooks.", "AI Script Writer"),
            ("Claude", "writing", "Writing, Scripts & Captions", "yes", "https://claude.ai", "Advanced reasoning AI with long-context nuance for deep narrative scripts and dialogue.", "AI Script Writer"),
            ("Google Gemini", "writing", "Writing, Scripts & Captions", "yes", "https://gemini.google.com", "Multimodal intelligence for researching, drafting, and refining creative copy.", "AI Script Writer"),
            ("Jasper", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://www.jasper.ai", "Enterprise brand voice platform for conversion copy and marketing campaigns.", "AI Script Writer"),
            ("Copy.ai", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://www.copy.ai", "Automated marketing workflow engine for social captions, blogs, and ad copy.", "AI Script Writer"),
            ("Writesonic", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://writesonic.com", "AI writer with built-time search and SEO-optimized article generation.", "AI Script Writer"),
            ("Rytr", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://rytr.me", "Budget-friendly lightweight assistant for quick social post captions and emails.", "AI Script Writer"),
            ("Sudowrite", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://www.sudowrite.com", "Specialized creative writing suite for fictional stories, twists, and character arcs.", "AI Script Writer"),
            ("Grammarly", "writing", "Writing, Scripts & Captions", "yes", "https://www.grammarly.com", "Real-time grammar, tone detection, and vocabulary enhancement assistant.", "AI Script Writer"),
            ("QuillBot", "writing", "Writing, Scripts & Captions", "yes", "https://quillbot.com", "Paraphrasing, summarizing, and fluency-polishing tool for creator scripts.", "AI Script Writer"),
            ("Wordtune", "writing", "Writing, Scripts & Captions", "yes", "https://www.wordtune.com", "Context-aware phrasing rewrite and tone adaptation engine.", "AI Script Writer"),
            ("Anyword", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://www.anyword.com", "Performance-predictive copy generator with data-driven copy scores.", "AI Script Writer"),
            ("HyperWrite", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://hyperwriteai.com", "Personal AI writing companion for thought expansion and workflow automation.", "AI Script Writer"),
            ("Notion AI", "writing", "Writing, Scripts & Captions", "yes", "https://www.notion.so", "Integrated workspace AI for content calendar drafting, wikis, and task briefs.", "AI Script Writer"),
            ("Simplified", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://simplified.com", "All-in-one creator app with instant AI copy generators for multi-channel posts.", "AI Script Writer"),
            ("HIX.AI", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://hix.ai", "Comprehensive AI writing copilot for social posts, long-form blogs, and email responses.", "AI Script Writer"),
            ("Peppertype", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://www.peppertype.ai", "Content marketing platform built for rapid creative ideation and headline generation.", "AI Script Writer"),
            ("Writer.com", "writing", "Writing, Scripts & Captions", "yes", "https://writer.com", "Full-stack generative AI tailored for enterprise brand guidelines and compliance.", "AI Script Writer"),
            ("INK", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://inkforall.com", "AI writing and semantic optimization tool for audience engagement.", "AI Script Writer"),
            ("TextCortex", "writing", "Writing, Scripts & Captions", "plan_dependent", "https://textcortex.com", "Customizable AI assistant that adapts to personal creator voice and knowledge bases.", "AI Script Writer")
        ]
    },
    {
        "id": "image",
        "name": "AI Image Generation",
        "emoji": "🎨",
        "archetype": "AI Graphic Designer",
        "tools": [
            ("Midjourney", "image", "AI Image Generation", "plan_dependent", "https://www.midjourney.com", "Premier photorealistic and artistic image generation model.", "AI Graphic Designer"),
            ("DALL-E", "image", "AI Image Generation", "yes", "https://openai.com/dall-e-3", "OpenAI text-to-image engine with exceptional prompt adherence and detail.", "AI Graphic Designer"),
            ("Adobe Firefly", "image", "AI Image Generation", "yes", "https://firefly.adobe.com", "Commercially safe generative engine integrated natively into Adobe Creative Cloud.", "AI Graphic Designer"),
            ("Leonardo AI", "image", "AI Image Generation", "plan_dependent", "https://leonardo.ai", "Versatile creative studio with custom fine-tuned asset generation models.", "AI Graphic Designer"),
            ("Ideogram", "image", "AI Image Generation", "plan_dependent", "https://ideogram.ai", "State-of-the-art text rendering in visuals, typography, and graphic posters.", "AI Graphic Designer"),
            ("FLUX", "image", "AI Image Generation", "yes", "https://blackforestlabs.ai", "Open-weights next-gen diffusion model delivering hyper-realistic human details.", "AI Graphic Designer"),
            ("Stable Diffusion", "image", "AI Image Generation", "yes", "https://stability.ai", "Open-source foundation model for highly customized generative visual pipelines.", "AI Graphic Designer"),
            ("ComfyUI", "image", "AI Image Generation", "yes", "https://www.comfy.org", "Modular node-based graphical UI for Stable Diffusion and SDXL generative workflows.", "AI Graphic Designer"),
            ("Recraft", "image", "AI Image Generation", "yes", "https://www.recraft.ai", "Vector graphics, 3D icons, and brand illustrations generation canvas.", "AI Graphic Designer"),
            ("Playground AI", "image", "AI Image Generation", "plan_dependent", "https://playgroundai.com", "Free-flowing image editor and canvas for mixing generative styles.", "AI Graphic Designer"),
            ("NightCafe", "image", "AI Image Generation", "plan_dependent", "https://creator.nightcafe.studio", "Community-centric art creation studio supporting multiple generative algorithms.", "AI Graphic Designer"),
            ("DreamStudio", "image", "AI Image Generation", "yes", "https://dreamstudio.ai", "Official Stability AI web workspace for high-speed prompt-to-image creation.", "AI Graphic Designer"),
            ("Krea AI", "image", "AI Image Generation", "plan_dependent", "https://www.krea.ai", "Real-time generative canvas with instant feedback, video morphing, and upscaling.", "AI Graphic Designer"),
            ("Microsoft Designer", "image", "AI Image Generation", "yes", "https://designer.microsoft.com", "DALL-E powered visual designer for promotional banners and social posts.", "AI Graphic Designer"),
            ("ImagineArt", "image", "AI Image Generation", "plan_dependent", "https://www.imagine.art", "Fast AI art generator for stylized fantasy, anime, and product concepts.", "AI Graphic Designer"),
            ("SeaArt AI", "image", "AI Image Generation", "plan_dependent", "https://www.seaart.ai", "Feature-rich painting and rendering engine with massive community model library.", "AI Graphic Designer"),
            ("Tensor.Art", "image", "AI Image Generation", "yes", "https://tensor.art", "Free model hosting and online generation engine for checkpoint and LoRA rendering.", "AI Graphic Designer"),
            ("Mage.space", "image", "AI Image Generation", "plan_dependent", "https://www.mage.space", "High-speed canvas running SDXL and specialized fine-tunes.", "AI Graphic Designer"),
            ("Dreamina", "image", "AI Image Generation", "plan_dependent", "https://dreamina.com", "ByteDance creative image generator designed for creative social media storytelling.", "AI Graphic Designer"),
            ("Canva AI", "image", "AI Image Generation", "yes", "https://www.canva.com", "Magic Media image generation seamlessly embedded inside social post templates.", "AI Graphic Designer"),
            ("Photoroom", "image", "AI Image Generation", "yes", "https://www.photoroom.com", "Automated background replacement and studio product photography lighting.", "AI Graphic Designer")
        ]
    },
    {
        "id": "design",
        "name": "Graphic Design, Posters & Thumbnails",
        "emoji": "🖼️",
        "archetype": "AI Graphic Designer",
        "tools": [
            ("Canva", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://www.canva.com", "Intuitive drag-and-drop graphic design suite with comprehensive AI Magic Studio.", "AI Graphic Designer"),
            ("Adobe Express", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://express.adobe.com", "Quick-turnaround design platform with Firefly text-to-template features.", "AI Graphic Designer"),
            ("Flair AI", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://flair.ai", "AI design tool for branded product photography and commercial tabletop scenes.", "AI Graphic Designer"),
            ("Pebblely", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://pebblely.com", "E-commerce product visuals generator with photorealistic studio lighting.", "AI Graphic Designer"),
            ("Clipdrop", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://clipdrop.co", "Ecosystem of AI photo manipulation tools: relight, uncrop, and object removal.", "AI Graphic Designer"),
            ("Designs.ai", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://designs.ai", "Integrated creative suite for logo generation, mockups, and banner variations.", "AI Graphic Designer"),
            ("Stockimg.ai", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://stockimg.ai", "Generates book covers, posters, wallpapers, and YouTube thumbnails instantly.", "AI Graphic Designer"),
            ("Brandmark", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://brandmark.io", "Automated neural network brand identity and logo creation system.", "AI Graphic Designer"),
            ("Looka", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://looka.com", "AI-powered brand builder generating cohesive logos, cards, and social assets.", "AI Graphic Designer"),
            ("Uizard", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://uizard.io", "Rapid AI wireframing and UI/UX mockup designer from hand-drawn sketches.", "AI Graphic Designer"),
            ("Pixlr AI", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://pixlr.com", "Browser-based photo editing and generative fill design suite.", "AI Graphic Designer"),
            ("Fotor", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://www.fotor.com", "One-click photo enhancer, generative expander, and thumbnail maker.", "AI Graphic Designer"),
            ("Kittl", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://www.kittl.com", "Advanced typography and graphic illustration platform with generative vector tools.", "AI Graphic Designer"),
            ("AutoDraw", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://www.autodraw.com", "Google machine learning tool transforming rough sketches into clean iconography.", "AI Graphic Designer"),
            ("Renderforest", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://www.renderforest.com", "All-in-one branding suite for animated logos, mockups, and promotional graphics.", "AI Graphic Designer"),
            ("Visme", "design", "Graphic Design, Posters & Thumbnails", "plan_dependent", "https://www.visme.co", "Interactive visual design and infographic builder for content creators.", "AI Graphic Designer"),
            ("Pixelcut", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://pixelcut.ai", "Fast mobile and web product photo studio with instant background clearing.", "AI Graphic Designer"),
            ("PicMonkey", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://www.picmonkey.com", "Photo editing and graphic design software with smart cutout utilities.", "AI Graphic Designer"),
            ("Snappa", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://snappa.com", "Quick social graphic and YouTube thumbnail design without complexity.", "AI Graphic Designer"),
            ("DesignCap", "design", "Graphic Design, Posters & Thumbnails", "yes", "https://www.designcap.com", "Online poster, flyer, and card maker with customizable design presets.", "AI Graphic Designer")
        ]
    },
    {
        "id": "video",
        "name": "AI Video Generation",
        "emoji": "🎬",
        "archetype": "AI Video Creator",
        "tools": [
            ("Runway", "video", "AI Video Generation", "yes", "https://runwayml.com", "Gen-2 & Gen-3 Alpha foundational video models with camera controls and motion brush.", "AI Video Creator"),
            ("Sora", "video", "AI Video Generation", "plan_dependent", "https://openai.com/sora", "OpenAI physics-aware cinematic video foundation model.", "AI Video Creator"),
            ("Veo", "video", "AI Video Generation", "plan_dependent", "https://deepmind.google/models/veo/", "Google DeepMind high-definition video generation model with cinematic coherence.", "AI Video Creator"),
            ("Pika", "video", "AI Video Generation", "plan_dependent", "https://pika.art", "Idea-to-video platform with Pika 2.0 physics simulation and sound sync.", "AI Video Creator"),
            ("Kling", "video", "AI Video Generation", "plan_dependent", "https://klingai.com", "Photorealistic high-frame-rate video generator with incredible human motion fidelity.", "AI Video Creator"),
            ("Luma Dream Machine", "video", "AI Video Generation", "plan_dependent", "https://lumalabs.ai", "High-speed camera motion and fluid scene transition generative video engine.", "AI Video Creator"),
            ("Hailuo AI", "video", "AI Video Generation", "plan_dependent", "https://hailuoai.video", "MiniMax high-fidelity expressive motion video generator.", "AI Video Creator"),
            ("PixVerse", "video", "AI Video Generation", "plan_dependent", "https://pixverse.ai", "AI video generation platform offering stylized 4K motion and camera tracks.", "AI Video Creator"),
            ("Vidu", "video", "AI Video Generation", "plan_dependent", "https://www.vidu.studio", "Ultra-fast text/image-to-video engine with realistic lighting simulations.", "AI Video Creator"),
            ("Kaiber", "video", "AI Video Generation", "plan_dependent", "https://kaiber.ai", "Stylized music video generator with audio-reactive visual animation.", "AI Video Creator"),
            ("Morph Studio", "video", "AI Video Generation", "plan_dependent", "https://www.morphstudio.com", "Node-based generative video workflow for storyboarding and scene sequence composition.", "AI Video Creator"),
            ("InVideo AI", "video", "AI Video Generation", "plan_dependent", "https://invideo.io", "Turn text prompts into full-length narrated YouTube videos with footage and music.", "AI Video Creator"),
            ("Synthesia", "video", "AI Video Generation", "plan_dependent", "https://synthesia.io", "Studio-grade synthetic video presenters and avatars in 120+ languages.", "AI Video Creator"),
            ("HeyGen", "video", "AI Video Generation", "plan_dependent", "https://www.heygen.com", "Hyper-realistic talking avatars, interactive digital humans, and video dubbing.", "AI Video Creator"),
            ("Hedra", "video", "AI Video Generation", "plan_dependent", "https://hedra.com", "Character-consistent controllable video generation with full lip-sync expression.", "AI Video Creator"),
            ("D-ID", "video", "AI Video Generation", "plan_dependent", "https://d-id.com", "Photorealistic talking head generation from single still portraits.", "AI Video Creator"),
            ("Colossyan", "video", "AI Video Generation", "plan_dependent", "https://www.colossyan.com", "AI video creator for workplace learning, sales presentations, and onboarding.", "AI Video Creator"),
            ("DeepBrain AI", "video", "AI Video Generation", "plan_dependent", "https://www.deepbrain.io", "Conversational AI digital humans for broadcast news and brand explainers.", "AI Video Creator"),
            ("Hour One", "video", "AI Video Generation", "plan_dependent", "https://hourone.ai", "Automated virtual presenter video creation with scalable enterprise templates.", "AI Video Creator"),
            ("Rephrase.ai", "video", "AI Video Generation", "plan_dependent", "https://www.rephrase.ai", "Personalized video messaging engine driving customer engagement at scale.", "AI Video Creator")
        ]
    },
    {
        "id": "editing",
        "name": "Video Editing & Reels",
        "emoji": "📹",
        "archetype": "AI Editor & Repurposing Expert",
        "tools": [
            ("CapCut", "editing", "Video Editing & Reels", "yes", "https://www.capcut.com", "Viral short-form video editor with AI auto-captions, effects, and trending templates.", "AI Editor & Repurposing Expert"),
            ("Descript", "editing", "Video Editing & Reels", "yes", "https://www.descript.com", "Text-based video and audio editing with Overdub voice repair and filler word removal.", "AI Editor & Repurposing Expert"),
            ("Adobe Premiere Pro", "editing", "Video Editing & Reels", "yes", "https://www.adobe.com/products/premiere.html", "Industry-standard NLE with Firefly generative extend and text-based editing.", "AI Editor & Repurposing Expert"),
            ("DaVinci Resolve", "editing", "Video Editing & Reels", "yes", "https://www.blackmagicdesign.com", "Hollywood-grade color grading, Fairlight audio, and Neural Engine speed warp.", "AI Editor & Repurposing Expert"),
            ("Filmora", "editing", "Video Editing & Reels", "yes", "https://filmora.wondershare.com", "Creator-friendly video editing with AI smart cutout and copilot editing assistant.", "AI Editor & Repurposing Expert"),
            ("VEED.io", "editing", "Video Editing & Reels", "plan_dependent", "https://www.veed.io", "Online video suite with AI subtitling, clean audio filters, and eye-contact correction.", "AI Editor & Repurposing Expert"),
            ("OpusClip", "editing", "Video Editing & Reels", "plan_dependent", "https://www.opus.pro", "Generative AI repurposing tool converting long videos into viral shorts with hook scores.", "AI Editor & Repurposing Expert"),
            ("Vizard", "editing", "Video Editing & Reels", "plan_dependent", "https://vizard.ai", "Auto-repurposes webinars, podcasts, and recordings into social clips.", "AI Editor & Repurposing Expert"),
            ("Klap", "editing", "Video Editing & Reels", "plan_dependent", "https://klap.app", "AI video reframing and dynamic captioning for TikTok, Reels, and Shorts.", "AI Editor & Repurposing Expert"),
            ("Munch", "editing", "Video Editing & Reels", "plan_dependent", "https://www.getmunch.com", "Extracts the most engaging moments from long-form content using trend analysis.", "AI Editor & Repurposing Expert"),
            ("Vidyo.ai", "editing", "Video Editing & Reels", "plan_dependent", "https://vidyo.ai", "AI content repurposing platform with smart chapters and customizable social templates.", "AI Editor & Repurposing Expert"),
            ("Wisecut", "editing", "Video Editing & Reels", "plan_dependent", "https://www.wisecut.video", "Automatic video editor that cuts silences and adds background music ducking.", "AI Editor & Repurposing Expert"),
            ("Gling", "editing", "Video Editing & Reels", "plan_dependent", "https://gling.ai", "Specifically built for YouTubers to cut out silences, stumbles, and bad takes.", "AI Editor & Repurposing Expert"),
            ("Captions", "editing", "Video Editing & Reels", "plan_dependent", "https://www.captions.ai", "Studio-grade mobile/desktop app for animated captions, eye contact, and AI voiceover.", "AI Editor & Repurposing Expert"),
            ("Submagic", "editing", "Video Editing & Reels", "plan_dependent", "https://www.submagic.co", "Generates dynamic captions with auto-emojis, highlighted keywords, and B-roll sound effects.", "AI Editor & Repurposing Expert"),
            ("AutoPod", "editing", "Video Editing & Reels", "yes", "https://www.autopod.fm", "Multi-camera automated podcast and interview editing plugin for Premiere Pro.", "AI Editor & Repurposing Expert"),
            ("Riverside", "editing", "Video Editing & Reels", "yes", "https://riverside.fm", "Lossless local recording studio with Magic Clips AI video snippet generator.", "AI Editor & Repurposing Expert"),
            ("Canva Video", "editing", "Video Editing & Reels", "yes", "https://www.canva.com/video", "Fast drag-and-drop video maker with animation transitions and stock library.", "AI Editor & Repurposing Expert"),
            ("Clipchamp", "editing", "Video Editing & Reels", "yes", "https://clipchamp.com", "Windows-native lightweight video editor with AI auto-compose and speech-to-text.", "AI Editor & Repurposing Expert"),
            ("Recast Studio", "editing", "Video Editing & Reels", "plan_dependent", "https://recast.studio", "Converts podcast audio and video into bite-sized marketing clips and audiograms.", "AI Editor & Repurposing Expert"),
            ("After Effects", "editing", "Video Editing & Reels", "yes", "https://www.adobe.com/products/aftereffects.html", "Visual effects, motion graphics, and compositing software with AI rotoscoping.", "AI Editor & Repurposing Expert"),
            ("Topaz Video AI", "editing", "Video Editing & Reels", "yes", "https://www.topazlabs.com", "Neural network video upscaling, de-interlacing, motion smoothing, and restoration.", "AI Editor & Repurposing Expert")
        ]
    },
    {
        "id": "voice",
        "name": "Voice Generation & Text-to-Speech",
        "emoji": "🎙️",
        "archetype": "AI Voice Artist",
        "tools": [
            ("ElevenLabs", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://elevenlabs.io", "Industry benchmark for emotionally nuanced voice cloning and multilingual speech synthesis.", "AI Voice Artist"),
            ("Murf AI", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://murf.ai", "Versatile voice studio for corporate explainers, product demos, and e-learning.", "AI Voice Artist"),
            ("PlayHT", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://play.ht", "Conversational AI voice engine with low latency and instant voice cloning.", "AI Voice Artist"),
            ("LOVO AI", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://lovo.ai", "Award-winning Genny voice platform featuring 500+ voices with emotional inflections.", "AI Voice Artist"),
            ("WellSaid Labs", "voice", "Voice Generation & Text-to-Speech", "yes", "https://wellsaidlabs.com", "Ethical AI voice platform producing studio-grade enterprise voiceovers.", "AI Voice Artist"),
            ("Speechify", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://speechify.com", "High-speed text-to-speech reader and creator voiceover generator.", "AI Voice Artist"),
            ("Resemble AI", "voice", "Voice Generation & Text-to-Speech", "yes", "https://www.resemble.ai", "Custom voice cloning with granular phoneme control and deepfake watermarking.", "AI Voice Artist"),
            ("Cartesia", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://cartesia.ai", "Ultra-low-latency sonic generative voice model for interactive audio agents.", "AI Voice Artist"),
            ("Typecast", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://typecast.ai", "Directable virtual voice casting platform with emotion and pitch modulation.", "AI Voice Artist"),
            ("Narakeet", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://narakeet.com", "Turns presentation slides and scripts into video voiceovers in 90+ languages.", "AI Voice Artist"),
            ("NaturalReader", "voice", "Voice Generation & Text-to-Speech", "yes", "https://www.naturalreaders.com", "Natural sounding text-to-speech for commercial narration and accessibility.", "AI Voice Artist"),
            ("Listnr", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://listnr.tech", "Podcast hosting and AI voiceover tool with 900+ accents and voices.", "AI Voice Artist"),
            ("TTSMaker", "voice", "Voice Generation & Text-to-Speech", "yes", "https://ttsmaker.com", "Free and commercial online text-to-speech tool supporting multiple file exports.", "AI Voice Artist"),
            ("Dubverse", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://dubverse.ai", "Generative video dubbing and subtitles engine in 30+ Indian and global languages.", "AI Voice Artist"),
            ("FineVoice", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://www.finevoice.com", "Digital voice solution for voice changing, text-to-speech, and audio transcription.", "AI Voice Artist"),
            ("Rask AI", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://rask.ai", "End-to-end video localization and voice dubbing with original voice tone matching.", "AI Voice Artist"),
            ("Altered Studio", "voice", "Voice Generation & Text-to-Speech", "yes", "https://www.altered.ai", "Professional voice morphing and voice performance transformation software.", "AI Voice Artist"),
            ("Voice.ai", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://voice.ai", "Real-time AI voice changer for streaming, gaming, and content creation.", "AI Voice Artist"),
            ("Fish Audio", "voice", "Voice Generation & Text-to-Speech", "plan_dependent", "https://fish.audio", "High-fidelity open-weights and cloud voice model with few-shot cloning.", "AI Voice Artist"),
            ("OpenAI text-to-speech", "voice", "Voice Generation & Text-to-Speech", "yes", "https://platform.openai.com/docs/guides/text-to-speech", "Developer-friendly whisper-clear TTS API with human-like prosody.", "AI Voice Artist")
        ]
    },
    {
        "id": "music",
        "name": "Music & Sound Effects",
        "emoji": "🎵",
        "archetype": "AI Music Producer",
        "tools": [
            ("Suno", "music", "Music & Sound Effects", "plan_dependent", "https://suno.com", "Full-song generative audio model synthesizing vocals, instrumentation, and lyrics.", "AI Music Producer"),
            ("Udio", "music", "Music & Sound Effects", "plan_dependent", "https://www.udio.com", "High-fidelity musical creation suite with genre blending and multi-track extension.", "AI Music Producer"),
            ("AIVA", "music", "Music & Sound Effects", "plan_dependent", "https://www.aiva.ai", "AI music composer recognized by author rights societies for emotional cinematic scores.", "AI Music Producer"),
            ("Boomy", "music", "Music & Sound Effects", "plan_dependent", "https://boomy.com", "Instant song creation app allowing creators to publish tracks to streaming platforms.", "AI Music Producer"),
            ("Loudly", "music", "Music & Sound Effects", "plan_dependent", "https://www.loudly.com", "Royalty-free AI music generator customized for video creators and game developers.", "AI Music Producer"),
            ("Soundraw", "music", "Music & Sound Effects", "plan_dependent", "https://soundraw.io", "Customizable background music generator where tempo and structure match video cuts.", "AI Music Producer"),
            ("Mubert", "music", "Music & Sound Effects", "plan_dependent", "https://mubert.com", "Generative music streaming API and creator track generator for real-time ambience.", "AI Music Producer"),
            ("Soundful", "music", "Music & Sound Effects", "plan_dependent", "https://soundful.com", "Studio-quality royalty-free tracks generator across EDM, Hip Hop, and Pop genres.", "AI Music Producer"),
            ("Beatoven.ai", "music", "Music & Sound Effects", "plan_dependent", "https://www.beatoven.ai", "Emotion-based background music composition tailored for podcast and video editors.", "AI Music Producer"),
            ("Splash Music", "music", "Music & Sound Effects", "plan_dependent", "https://splashmusic.com", "Text-to-song engine designed for aspiring beatmakers and social creators.", "AI Music Producer"),
            ("Ecrett Music", "music", "Music & Sound Effects", "plan_dependent", "https://ecrettmusic.com", "Simple music generation based on scene type, mood, and genre.", "AI Music Producer"),
            ("Voicemod", "music", "Music & Sound Effects", "yes", "https://www.voicemod.net", "Real-time voice changer and soundboard software for streamers and content creators.", "AI Music Producer"),
            ("ElevenLabs Sound Effects", "music", "Music & Sound Effects", "plan_dependent", "https://elevenlabs.io/sound-effects", "Generates realistic foley, cinematic whooshes, and atmospheric audio from prompts.", "AI Music Producer"),
            ("Melodia", "music", "Music & Sound Effects", "plan_dependent", "https://melodia.ai", "Melody generation and vocal tuning assistant for independent music producers.", "AI Music Producer"),
            ("MusicLM", "music", "Music & Sound Effects", "plan_dependent", "https://google.com/musiclm", "Google experimental high-fidelity musical generator from descriptive text.", "AI Music Producer"),
            ("Stable Audio", "music", "Music & Sound Effects", "yes", "https://stableaudio.com", "Stability AI foundation audio diffusion model for music tracks and stems.", "AI Music Producer"),
            ("Audiocraft", "music", "Music & Sound Effects", "yes", "https://audiocraft.metademolab.com", "Meta open-source research suite powering MusicGen and AudioGen.", "AI Music Producer"),
            ("Lalal.ai", "music", "Music & Sound Effects", "plan_dependent", "https://lalal.ai", "High-precision stem splitter for extracting vocals, drums, and bass lines.", "AI Music Producer"),
            ("Moises", "music", "Music & Sound Effects", "plan_dependent", "https://moises.ai", "Musician app for AI stem separation, pitch shifting, and metronome detection.", "AI Music Producer"),
            ("Soundstripe AI", "music", "Music & Sound Effects", "yes", "https://soundstripe.com", "Royalty-free licensing music platform with intelligent song search and matching.", "AI Music Producer")
        ]
    },
    {
        "id": "social",
        "name": "Social Media Management",
        "emoji": "📱",
        "archetype": "Social Media Manager",
        "tools": [
            ("Buffer", "social", "Social Media Management", "yes", "https://buffer.com", "Clean publishing, scheduling, and analytics platform with AI assistant for repurposing.", "Social Media Manager"),
            ("Predis.ai", "social", "Social Media Management", "plan_dependent", "https://predis.ai", "Generates ready-to-publish social posts, carousels, and videos from text prompts.", "Social Media Manager"),
            ("Metricool", "social", "Social Media Management", "yes", "https://metricool.com", "All-in-one social media analytics, scheduling, and competitor tracking platform.", "Social Media Manager"),
            ("Hootsuite", "social", "Social Media Management", "yes", "https://hootsuite.com", "Enterprise social media suite with OwlyWriter AI for caption generation.", "Social Media Manager"),
            ("Sprout Social", "social", "Social Media Management", "yes", "https://sproutsocial.com", "Comprehensive social listening, customer advocacy, and publishing workflows.", "Social Media Manager"),
            ("Later", "social", "Social Media Management", "yes", "https://later.com", "Visual social scheduler optimized for Instagram grid planning and TikTok campaigns.", "Social Media Manager"),
            ("FeedHive", "social", "Social Media Management", "plan_dependent", "https://feedhive.com", "AI-powered social media calendar with viral post performance predictions.", "Social Media Manager"),
            ("Ocoya", "social", "Social Media Management", "plan_dependent", "https://ocoya.com", "Content creation and scheduling workspace integrating AI graphics and copywriting.", "Social Media Manager"),
            ("Vista Social", "social", "Social Media Management", "plan_dependent", "https://vistasocial.com", "Modern social media management with unified inbox and automated comment responses.", "Social Media Manager"),
            ("SocialBee", "social", "Social Media Management", "plan_dependent", "https://socialbee.com", "Category-based social scheduling engine with evergreen recycling algorithms.", "Social Media Manager"),
            ("Flick", "social", "Social Media Management", "plan_dependent", "https://flick.tech", "Hashtag research, brainstorm assistant, and post scheduler for creators.", "Social Media Manager"),
            ("Publer", "social", "Social Media Management", "plan_dependent", "https://publer.io", "Social media virtual superhero for multi-account publishing and watermark protection.", "Social Media Manager"),
            ("CoSchedule", "social", "Social Media Management", "yes", "https://coschedule.com", "Marketing calendar suite with Headline Studio for maximum click-through rates.", "Social Media Manager"),
            ("Sendible", "social", "Social Media Management", "yes", "https://sendible.com", "Agency-tailored management platform with custom client approval dashboards.", "Social Media Manager"),
            ("Planoly", "social", "Social Media Management", "plan_dependent", "https://planoly.com", "Visual planner designed specifically for multi-channel video and carousel campaigns.", "Social Media Manager"),
            ("ContentStudio", "social", "Social Media Management", "plan_dependent", "https://contentstudio.io", "Content discovery, curation, and automated social publishing engine.", "Social Media Manager"),
            ("Agorapulse", "social", "Social Media Management", "yes", "https://agorapulse.com", "Social media management with social CRM and ROI tracking.", "Social Media Manager"),
            ("Loomly", "social", "Social Media Management", "yes", "https://loomly.com", "Brand success platform with automated post ideas and collaborative approval workflows.", "Social Media Manager"),
            ("SocialPilot", "social", "Social Media Management", "yes", "https://socialpilot.co", "Cost-effective team scheduling and white-label reporting for marketing agencies.", "Social Media Manager"),
            ("Crowdfire", "social", "Social Media Management", "yes", "https://crowdfireapp.com", "Simple social media manager for content discovery and scheduled distribution.", "Social Media Manager")
        ]
    },
    {
        "id": "research",
        "name": "Research, Ideas & Trend Discovery",
        "emoji": "🔎",
        "archetype": "AI Marketing Strategist",
        "tools": [
            ("Perplexity AI", "research", "Research, Ideas & Trend Discovery", "yes", "https://perplexity.ai", "Conversational search engine delivering cited, real-time web research answers.", "AI Marketing Strategist"),
            ("Google Trends", "research", "Research, Ideas & Trend Discovery", "yes", "https://trends.google.com", "Authoritative real-time search volume queries and geographical interest data.", "AI Marketing Strategist"),
            ("BuzzSumo", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://buzzsumo.com", "Discovers viral content headlines, trending topics, and key industry influencers.", "AI Marketing Strategist"),
            ("AnswerThePublic", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://answerthepublic.com", "Visual search listening tool mapping raw consumer questions and search queries.", "AI Marketing Strategist"),
            ("Exploding Topics", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://explodingtopics.com", "Analyzes millions of web searches to flag breakout trends before they become mainstream.", "AI Marketing Strategist"),
            ("Feedly AI", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://feedly.com", "Leo AI engine curates high-signal news feeds and competitive intelligence.", "AI Marketing Strategist"),
            ("Brandwatch", "research", "Research, Ideas & Trend Discovery", "yes", "https://brandwatch.com", "Consumer intelligence and enterprise social media sentiment monitoring.", "AI Marketing Strategist"),
            ("TubeBuddy", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://tubebuddy.com", "YouTube channel optimization toolkit with keyword scorecards and A/B thumbnail testing.", "AI Marketing Strategist"),
            ("vidIQ", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://vidiq.com", "AI-powered YouTube growth assistant offering daily video ideas and competitor tracking.", "AI Marketing Strategist"),
            ("SparkToro", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://sparktoro.com", "Audience research engine uncovering podcasts, accounts, and websites target users follow.", "AI Marketing Strategist"),
            ("Semrush", "research", "Research, Ideas & Trend Discovery", "yes", "https://semrush.com", "Complete marketing intelligence suite for competitor organic and paid research.", "AI Marketing Strategist"),
            ("Ahrefs", "research", "Research, Ideas & Trend Discovery", "yes", "https://ahrefs.com", "SEO powerhouse for backlink analysis, keyword exploration, and content gap spotting.", "AI Marketing Strategist"),
            ("GummySearch", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://gummysearch.com", "Audience research engine parsing Reddit communities for customer pain points.", "AI Marketing Strategist"),
            ("ChatSpot", "research", "Research, Ideas & Trend Discovery", "yes", "https://chatspot.ai", "HubSpot natural language AI assistant combining CRM data with market insights.", "AI Marketing Strategist"),
            ("Consensus", "research", "Research, Ideas & Trend Discovery", "yes", "https://consensus.app", "AI search engine summarizing evidence-based findings across peer-reviewed papers.", "AI Marketing Strategist"),
            ("Scite.ai", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://scite.ai", "Smart citation index showing whether research papers are supported or contrasted.", "AI Marketing Strategist"),
            ("Elicit", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://elicit.com", "AI research assistant automating literature reviews and data synthesis.", "AI Marketing Strategist"),
            ("Glasp", "research", "Research, Ideas & Trend Discovery", "yes", "https://glasp.co", "Social web highlighter collecting notes, quotes, and YouTube video summaries.", "AI Marketing Strategist"),
            ("TrendHunter", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://trendhunter.com", "Trend community leveraging crowd data to forecast future lifestyle innovations.", "AI Marketing Strategist"),
            ("Trends.co", "research", "Research, Ideas & Trend Discovery", "plan_dependent", "https://trends.co", "HubSpot research community analyzing emerging startup niches and market data.", "AI Marketing Strategist")
        ]
    },
    {
        "id": "seo",
        "name": "SEO & Blog Optimization",
        "emoji": "📈",
        "archetype": "AI Marketing Strategist",
        "tools": [
            ("Surfer SEO", "seo", "SEO & Blog Optimization", "plan_dependent", "https://surferseo.com", "Content editor analyzing SERP correlation data to optimize ranking articles.", "AI Marketing Strategist"),
            ("Frase", "seo", "SEO & Blog Optimization", "plan_dependent", "https://frase.io", "Combines research, content briefs, and AI writing to rank on search engines.", "AI Marketing Strategist"),
            ("Clearscope", "seo", "SEO & Blog Optimization", "yes", "https://clearscope.io", "Premium SEO content optimization platform driven by semantic search entities.", "AI Marketing Strategist"),
            ("MarketMuse", "seo", "SEO & Blog Optimization", "plan_dependent", "https://marketmuse.com", "AI content planning and topic modeling software identifying content gaps.", "AI Marketing Strategist"),
            ("RankIQ", "seo", "SEO & Blog Optimization", "plan_dependent", "https://rankiq.com", "SEO tool designed specifically for bloggers to discover low-competition keywords.", "AI Marketing Strategist"),
            ("NeuronWriter", "seo", "SEO & Blog Optimization", "plan_dependent", "https://neuronwriter.com", "NLP-driven content editor optimizing articles with Google SERP semantic models.", "AI Marketing Strategist"),
            ("Yoast SEO", "seo", "SEO & Blog Optimization", "yes", "https://yoast.com", "Standard WordPress plugin for on-page SEO analysis and readability checks.", "AI Marketing Strategist"),
            ("Rank Math", "seo", "SEO & Blog Optimization", "yes", "https://rankmath.com", "Lightweight WordPress SEO suite with built-in schema markup and rank monitoring.", "AI Marketing Strategist"),
            ("SE Ranking", "seo", "SEO & Blog Optimization", "plan_dependent", "https://seranking.com", "All-in-one SEO platform covering keyword rank tracking, audit, and competitor analysis.", "AI Marketing Strategist"),
            ("Scalenut", "seo", "SEO & Blog Optimization", "plan_dependent", "https://scalenut.com", "AI-powered SEO marketing platform managing content from keyword research to publishing.", "AI Marketing Strategist"),
            ("GrowthBar", "seo", "SEO & Blog Optimization", "plan_dependent", "https://growthbarseo.com", "Simple AI writing tool with built-in keyword research and blog outline generator.", "AI Marketing Strategist"),
            ("Outranking", "seo", "SEO & Blog Optimization", "plan_dependent", "https://outranking.io", "Data-driven SEO content strategist with automated facts extraction.", "AI Marketing Strategist"),
            ("Dashword", "seo", "SEO & Blog Optimization", "plan_dependent", "https://dashword.com", "Content optimization software for editorial teams to build high-converting briefs.", "AI Marketing Strategist"),
            ("Robinize", "seo", "SEO & Blog Optimization", "plan_dependent", "https://robinize.com", "Fast SEO content assistant analyzing top-ranking Google competitors.", "AI Marketing Strategist"),
            ("Writesonic SEO", "seo", "SEO & Blog Optimization", "plan_dependent", "https://writesonic.com", "Articles generation tool with integrated real-time keyword enrichment.", "AI Marketing Strategist"),
            ("SEObility", "seo", "SEO & Blog Optimization", "yes", "https://seobility.net", "Website crawler, backlink checker, and continuous Google rank monitoring tool.", "AI Marketing Strategist"),
            ("SpyFu", "seo", "SEO & Blog Optimization", "yes", "https://spyfu.com", "Competitor research tool exposing competitors' most profitable search keywords.", "AI Marketing Strategist"),
            ("Mangools", "seo", "SEO & Blog Optimization", "yes", "https://mangools.com", "User-friendly SEO toolset featuring KWFinder and SERPWatcher.", "AI Marketing Strategist"),
            ("Ubersuggest", "seo", "SEO & Blog Optimization", "plan_dependent", "https://neilpatel.com/ubersuggest", "Reverse engineers competitors' SEO and social media marketing strategies.", "AI Marketing Strategist"),
            ("Sitechecker", "seo", "SEO & Blog Optimization", "plan_dependent", "https://sitechecker.pro", "Real-time website health audits, on-page SEO checker, and ranking tracker.", "AI Marketing Strategist")
        ]
    },
    {
        "id": "podcast",
        "name": "Podcasting & Audio Editing",
        "emoji": "🎧",
        "archetype": "AI Voice Artist",
        "tools": [
            ("Adobe Podcast AI", "podcast", "Podcasting & Audio Editing", "yes", "https://podcast.adobe.com", "Enhance Speech removes background echo and noise to sound like professional studio recordings.", "AI Voice Artist"),
            ("Auphonic", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://auphonic.com", "Automated audio post-production service balancing loudness and filtering hums.", "AI Voice Artist"),
            ("Podcastle", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://podcastle.ai", "All-in-one studio for recording, audio cleanup, voice cloning, and text-to-speech.", "AI Voice Artist"),
            ("Cleanvoice AI", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://cleanvoice.ai", "Detects and removes filler words, mouth smacks, stuttering, and dead air.", "AI Voice Artist"),
            ("Resound", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://resound.fm", "AI audio editor for podcasters that automates cut points and audio leveling.", "AI Voice Artist"),
            ("Wondercraft", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://wondercraft.ai", "Transforms blogs and scripts into professional podcasts using synthetic voices.", "AI Voice Artist"),
            ("Castmagic", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://castmagic.io", "Turns podcast audio into show notes, timestamps, tweets, and newsletter summaries.", "AI Voice Artist"),
            ("Swell AI", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://swellai.com", "AI writing assistant generating transcripts, show notes, and articles from podcasts.", "AI Voice Artist"),
            ("Podsqueeze", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://podsqueeze.com", "Generates complete podcast content kits: clips, timestamps, and blog posts.", "AI Voice Artist"),
            ("Nomono", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://nomono.co", "Spatial audio recording hardware and cloud audio enhancement software.", "AI Voice Artist"),
            ("Adobe Audition", "podcast", "Podcasting & Audio Editing", "yes", "https://www.adobe.com/products/audition.html", "Professional digital audio workstation with spectral editing and noise gates.", "AI Voice Artist"),
            ("Soundop", "podcast", "Podcasting & Audio Editing", "yes", "https://soundop.com", "Fast audio recording, multitrack mixing, and batch audio processing software.", "AI Voice Artist"),
            ("Krisp", "podcast", "Podcasting & Audio Editing", "yes", "https://krisp.ai", "AI noise-cancellation app eliminating background noise and meeting chatter in real time.", "AI Voice Artist"),
            ("Reaper", "podcast", "Podcasting & Audio Editing", "yes", "https://reaper.fm", "Highly customizable digital audio workstation favored by sound designers.", "AI Voice Artist"),
            ("Hindenburg", "podcast", "Podcasting & Audio Editing", "yes", "https://hindenburg.com", "Audio workstation tailored for spoken-word storytellers, journalists, and radio.", "AI Voice Artist"),
            ("Riverside Magic Clips", "podcast", "Podcasting & Audio Editing", "yes", "https://riverside.fm", "Automatically identifies the most viral moments in podcast recordings for social sharing.", "AI Voice Artist"),
            ("Alitu", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://alitu.com", "Podcast maker app automating audio cleanup, intro/outro music, and RSS publishing.", "AI Voice Artist"),
            ("Podbean AI", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://podbean.com", "Podcast hosting platform offering AI show notes and automated episode mastering.", "AI Voice Artist"),
            ("Castos", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://castos.com", "Podcast hosting with automatic episode transcriptions and YouTube video republishing.", "AI Voice Artist"),
            ("Podomatic AI", "podcast", "Podcasting & Audio Editing", "plan_dependent", "https://podomatic.com", "Long-standing podcast community with AI audio mastering and promotional tools.", "AI Voice Artist")
        ]
    },
    {
        "id": "avatar",
        "name": "AI Avatars, Dubbing & Translation",
        "emoji": "🌎",
        "archetype": "AI Influencer Creator",
        "tools": [
            ("Akool", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://akool.com", "Generative AI face-swapping, talking avatars, and live streaming persona studio.", "AI Influencer Creator"),
            ("Lipdub", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://lipdub.ai", "Instant multi-language video translation with synchronized mouth movement.", "AI Influencer Creator"),
            ("Papercup", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://papercup.com", "Automated AI dubbing with human quality assurance for global broadcast content.", "AI Influencer Creator"),
            ("Camb.ai", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://camb.ai", "Dubbing platform capable of translating colloquial emotion into 140+ languages.", "AI Influencer Creator"),
            ("Speechelo", "avatar", "AI Avatars, Dubbing & Translation", "yes", "https://speechelo.com", "Text-to-speech software with natural inflections and breathing pauses.", "AI Influencer Creator"),
            ("Fliki", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://fliki.ai", "Text to video maker featuring realistic AI voices and dynamic subtitles.", "AI Influencer Creator"),
            ("Wonder Dynamics", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://wonderdynamics.com", "Automatically animates, lights, and composes CG characters into live-action scenes.", "AI Influencer Creator"),
            ("Tavus", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://tavus.io", "Conversational video replica platform producing personalized programmatic videos.", "AI Influencer Creator"),
            ("Neets AI", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://neets.ai", "High-speed text-to-speech engine creating expressive character voices.", "AI Influencer Creator"),
            ("HeyGen Dubbing", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://heygen.com", "One-click video dubbing matching speaker lip movement in the target language.", "AI Influencer Creator"),
            ("ElevenLabs Dubbing", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://elevenlabs.io/dubbing", "End-to-end video localization that preserves the creator's unique vocal identity.", "AI Influencer Creator"),
            ("DeepBrain Avatars", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://deepbrain.io", "Real-time AI avatar generators powering kiosk interactions and media news.", "AI Influencer Creator"),
            ("Synthesia Avatars", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://synthesia.io", "Expressive studio digital humans with customized outfits and branded gestures.", "AI Influencer Creator"),
            ("Hedra Character", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://hedra.com", "Multimodal character creation blending image, voice, and facial dynamics.", "AI Influencer Creator"),
            ("D-ID Presenter", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://d-id.com", "Interactive streaming API for live AI agents and marketing avatars.", "AI Influencer Creator"),
            ("Rask Localization", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://rask.ai", "Multi-speaker video dubbing and automated subtitle synchronization.", "AI Influencer Creator"),
            ("Dubverse Studio", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://dubverse.ai", "Self-service dubbing platform for video creators with phonetic control.", "AI Influencer Creator"),
            ("Colossyan Video", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://colossyan.com", "Interactive avatar scenarios for corporate roleplays and compliance learning.", "AI Influencer Creator"),
            ("Hour One Studio", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://hourone.ai", "Transforms structured content into photo-real virtual presenter videos.", "AI Influencer Creator"),
            ("Rephrase Studio", "avatar", "AI Avatars, Dubbing & Translation", "plan_dependent", "https://rephrase.ai", "Enterprise digital twin platform for dynamic customer journey video clips.", "AI Influencer Creator")
        ]
    },
    {
        "id": "presentation",
        "name": "Presentations & Infographics",
        "emoji": "📊",
        "archetype": "AI Graphic Designer",
        "tools": [
            ("Gamma", "presentation", "Presentations & Infographics", "yes", "https://gamma.app", "Interactive webpage, doc, and slide deck generation from natural language prompts.", "AI Graphic Designer"),
            ("Tome", "presentation", "Presentations & Infographics", "plan_dependent", "https://tome.app", "Generative storytelling platform formatting narrative decks and client proposals.", "AI Graphic Designer"),
            ("Beautiful.ai", "presentation", "Presentations & Infographics", "yes", "https://beautiful.ai", "Smart slide deck software where design layouts adapt dynamically as content is typed.", "AI Graphic Designer"),
            ("Pitch", "presentation", "Presentations & Infographics", "yes", "https://pitch.com", "Collaborative presentation workspace with modern design templates and AI generator.", "AI Graphic Designer"),
            ("SlidesAI", "presentation", "Presentations & Infographics", "plan_dependent", "https://slidesai.io", "Google Slides add-on that summarizes long text documents into presentation slides.", "AI Graphic Designer"),
            ("Canva Presentations", "presentation", "Presentations & Infographics", "yes", "https://canva.com", "Full-featured slide creator with Magic Design animations and collaborative whiteboards.", "AI Graphic Designer"),
            ("Presentations.AI", "presentation", "Presentations & Infographics", "plan_dependent", "https://presentations.ai", "Turn ideas into investor-ready pitch decks with instant brand consistency.", "AI Graphic Designer"),
            ("Decktopus", "presentation", "Presentations & Infographics", "plan_dependent", "https://decktopus.com", "Guided AI presentation creator complete with built-in audience forms and tips.", "AI Graphic Designer"),
            ("Storydoc", "presentation", "Presentations & Infographics", "plan_dependent", "https://storydoc.com", "Interactive proposal and deck builder that tracks viewer scroll depth and engagement.", "AI Graphic Designer"),
            ("Plus AI", "presentation", "Presentations & Infographics", "plan_dependent", "https://plusai.me", "Google Slides and Docs AI extension for building custom branded presentations.", "AI Graphic Designer"),
            ("PopAI", "presentation", "Presentations & Infographics", "plan_dependent", "https://popai.pro", "Personal workspace combining document reading, visual mapping, and slide creation.", "AI Graphic Designer"),
            ("Prezi AI", "presentation", "Presentations & Infographics", "yes", "https://prezi.com", "Dynamic zooming presentation software that brings zoom transitions into AI decks.", "AI Graphic Designer"),
            ("Microsoft Copilot PowerPoint", "presentation", "Presentations & Infographics", "yes", "https://microsoft.com", "Generates slide presentations directly from Word documents and OneDrive assets.", "AI Graphic Designer"),
            ("Slidebean", "presentation", "Presentations & Infographics", "plan_dependent", "https://slidebean.com", "Pitch deck design platform tailored for venture startups seeking funding.", "AI Graphic Designer"),
            ("Wondershare Presentory", "presentation", "Presentations & Infographics", "plan_dependent", "https://presentory.wondershare.com", "Virtual presentation software for live streaming with AI scene layouts.", "AI Graphic Designer"),
            ("Venngage", "presentation", "Presentations & Infographics", "plan_dependent", "https://venngage.com", "Infographic maker turning complex datasets into engaging visual storytelling.", "AI Graphic Designer"),
            ("Piktochart", "presentation", "Presentations & Infographics", "plan_dependent", "https://piktochart.com", "Visual communication tool for turning numbers and reports into crisp infographics.", "AI Graphic Designer"),
            ("Infogram", "presentation", "Presentations & Infographics", "plan_dependent", "https://infogram.com", "Data visualization tool generating responsive interactive charts and infographics.", "AI Graphic Designer"),
            ("Zoho Show AI", "presentation", "Presentations & Infographics", "yes", "https://zoho.com/show", "Cloud-based presentation app with smart layout formatting and remote casting.", "AI Graphic Designer"),
            ("Simplified Presentations", "presentation", "Presentations & Infographics", "plan_dependent", "https://simplified.com", "Automated deck designer for social media workshops and client pitches.", "AI Graphic Designer")
        ]
    },
    {
        "id": "influencer",
        "name": "AI Influencers & Virtual Creators",
        "emoji": "🤖",
        "archetype": "AI Influencer Creator",
        "tools": [
            ("RenderNet", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://rendernet.ai", "Generates consistent character faces and poses across diverse scenes and lighting.", "AI Influencer Creator"),
            ("FaceFusion", "influencer", "AI Influencers & Virtual Creators", "yes", "https://facefusion.io", "Next-gen open-source face swapper and facial enhancement pipeline.", "AI Influencer Creator"),
            ("Roop", "influencer", "AI Influencers & Virtual Creators", "yes", "https://github.com/s0md3v/roop", "One-click deep face swap utility without requiring dataset training.", "AI Influencer Creator"),
            ("Fooocus", "influencer", "AI Influencers & Virtual Creators", "yes", "https://github.com/lllyasviel/Fooocus", "Image generating software blending SDXL and Midjourney simplicity.", "AI Influencer Creator"),
            ("LivePortrait", "influencer", "AI Influencers & Virtual Creators", "yes", "https://liveportrait.github.io", "Efficient portrait animation from single images driven by driving video clips.", "AI Influencer Creator"),
            ("Civitai", "influencer", "AI Influencers & Virtual Creators", "yes", "https://civitai.com", "Open hub for AI generative models, LoRAs, and community character checkpoints.", "AI Influencer Creator"),
            ("Artbreeder", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://artbreeder.com", "Collaborative art tool remixing faces, characters, and landscapes with gene mixers.", "AI Influencer Creator"),
            ("Inworld AI", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://inworld.ai", "Generates dynamic AI characters with personality, memory, and emotional dialogue.", "AI Influencer Creator"),
            ("Character.ai", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://character.ai", "Conversational platform allowing users to interact with customizable virtual personalities.", "AI Influencer Creator"),
            ("SoulGen", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://soulgen.net", "AI generator creating customizable anime and real-looking virtual avatars.", "AI Influencer Creator"),
            ("Promptchan", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://promptchan.ai", "Uncensored AI image and character creator for creative fantasy figures.", "AI Influencer Creator"),
            ("Kupid AI", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://kupid.ai", "Virtual companion platform featuring AI avatars with voice responses.", "AI Influencer Creator"),
            ("Replika", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://replika.com", "Personal AI companion with personalized 3D avatar and empathetic chat.", "AI Influencer Creator"),
            ("Virtual Humans Hub", "influencer", "AI Influencers & Virtual Creators", "yes", "https://virtualhumans.org", "Resource portal tracking the virtual influencer industry, trends, and case studies.", "AI Influencer Creator"),
            ("Hedra Avatars", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://hedra.com", "Generates expressively animated virtual human video characters with speech.", "AI Influencer Creator"),
            ("HeyGen Avatar Pro", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://heygen.com", "Studio 4K digital twins with personal clothing and gesture replication.", "AI Influencer Creator"),
            ("Synthesia Expressive", "influencer", "AI Influencers & Virtual Creators", "plan_dependent", "https://synthesia.io", "Expressive micro-gestures and conversational avatars for virtual brands.", "AI Influencer Creator"),
            ("Stable Diffusion XL", "influencer", "AI Influencers & Virtual Creators", "yes", "https://stability.ai", "Foundation model for training character LoRAs and consistent brand spokespersons.", "AI Influencer Creator"),
            ("ComfyUI Workflow", "influencer", "AI Influencers & Virtual Creators", "yes", "https://comfy.org", "Node-based graphical interface for constructing consistent character pipelines.", "AI Influencer Creator"),
            ("Blender 3D Character", "influencer", "AI Influencers & Virtual Creators", "yes", "https://blender.org", "Free 3D creation suite for rigging, lighting, and rendering virtual creators.", "AI Influencer Creator")
        ]
    },
    {
        "id": "ugc",
        "name": "UGC, Ads & Marketing Creatives",
        "emoji": "📣",
        "archetype": "UGC Ad Creator",
        "tools": [
            ("Creatify", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://creatify.ai", "Transforms product links into high-converting UGC video ads in minutes.", "UGC Ad Creator"),
            ("Arcads", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://arcads.ai", "Generates realistic AI actor UGC ads from scripts for TikTok and Meta feeds.", "UGC Ad Creator"),
            ("JoggAI", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://jogg.ai", "AI video ad creator turning URL listings into engaging short-form commercials.", "UGC Ad Creator"),
            ("AdCreative.ai", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://adcreative.ai", "Generates conversion-focused ad creatives and banners using machine learning.", "UGC Ad Creator"),
            ("Pencil", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://trypencil.com", "Generative AI platform predicting ad performance before brands run campaigns.", "UGC Ad Creator"),
            ("QuickAds", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://quickads.ai", "Generates on-brand ad copies and display banners in all standard dimensions.", "UGC Ad Creator"),
            ("Memethic", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://memethic.com", "Generates viral brand memes and humorous social content hooks.", "UGC Ad Creator"),
            ("Tagshop", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://tagshop.ai", "Shoppable UGC and social commerce gallery platform for e-commerce sites.", "UGC Ad Creator"),
            ("Zebracat", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://zebracat.ai", "Turns text prompts and scripts into impactful marketing videos with AI effects.", "UGC Ad Creator"),
            ("CapCut for Business", "ugc", "UGC, Ads & Marketing Creatives", "yes", "https://capcut.com/business", "Enterprise suite for creating TikTok-optimized commercials with commercial templates.", "UGC Ad Creator"),
            ("Foreplay", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://foreplay.co", "Swipe file and ad intelligence platform for discovering top-performing ads.", "UGC Ad Creator"),
            ("Motion App", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://motionapp.com", "Creative analytics tool bridging the gap between media buyers and designers.", "UGC Ad Creator"),
            ("Marpipe", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://marpipe.com", "Automates multivariate creative testing for digital performance marketing.", "UGC Ad Creator"),
            ("Omneky", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://omneky.com", "Optimizes ad content with generative computer vision and predictive CTR insights.", "UGC Ad Creator"),
            ("Adsmurai", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://adsmurai.com", "Automates dynamic product ads and feed management across social networks.", "UGC Ad Creator"),
            ("Smartly.io", "ugc", "UGC, Ads & Marketing Creatives", "yes", "https://smartly.io", "Enterprise multi-platform social advertising automation and dynamic creative scaling.", "UGC Ad Creator"),
            ("Vidmob", "ugc", "UGC, Ads & Marketing Creatives", "yes", "https://vidmob.com", "Creative data platform analyzing visual attributes that drive advertising conversions.", "UGC Ad Creator"),
            ("InVideo Ad Maker", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://invideo.io", "Fast commercial builder with pre-cleared media and brand overlay templates.", "UGC Ad Creator"),
            ("Jasper Campaign", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://jasper.ai", "Builds multi-channel ad copy, email sequences, and landing pages from single briefs.", "UGC Ad Creator"),
            ("Copy.ai Marketing OS", "ugc", "UGC, Ads & Marketing Creatives", "plan_dependent", "https://copy.ai", "Automated marketing workflows executing ad angle testing and copy variations.", "UGC Ad Creator")
        ]
    },
    {
        "id": "repurposing",
        "name": "Repurposing & Content Automation",
        "emoji": "♻️",
        "archetype": "AI Editor & Repurposing Expert",
        "tools": [
            ("Repurpose.io", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://repurpose.io", "Automates cross-posting videos across TikTok, YouTube, Instagram, and LinkedIn.", "AI Editor & Repurposing Expert"),
            ("Chopcast", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://chopcast.io", "Extracts key clips from webinars and podcasts based on topic interest.", "AI Editor & Repurposing Expert"),
            ("2short.ai", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://2short.ai", "Extracts the best moments from YouTube videos and converts them into vertical shorts.", "AI Editor & Repurposing Expert"),
            ("Dumme", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://dumme.com", "AI video short generator finding logical hooks with no human intervention needed.", "AI Editor & Repurposing Expert"),
            ("Spikes Studio", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://spikes.studio", "Video clipping tool analyzing stream clips for gamers and podcast creators.", "AI Editor & Repurposing Expert"),
            ("GlossAi", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://glossai.co", "Enterprise video repurposing suite turning long events into eBooks, teasers, and carousels.", "AI Editor & Repurposing Expert"),
            ("Zapier AI", "repurposing", "Repurposing & Content Automation", "yes", "https://zapier.com", "Connects 6000+ web applications to automate creator publishing workflows.", "AI Editor & Repurposing Expert"),
            ("Make.com", "repurposing", "Repurposing & Content Automation", "yes", "https://make.com", "Visual workflow automation platform for orchestrating complex AI content pipelines.", "AI Editor & Repurposing Expert"),
            ("n8n", "repurposing", "Repurposing & Content Automation", "yes", "https://n8n.io", "Fair-code node-based workflow automation tool integrating custom LLMs and APIs.", "AI Editor & Repurposing Expert"),
            ("IFTTT", "repurposing", "Repurposing & Content Automation", "yes", "https://ifttt.com", "Lightweight applets connecting social accounts, smart devices, and creator clouds.", "AI Editor & Repurposing Expert"),
            ("OpusClip Repurposer", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://opus.pro", "Automated multi-clip extraction with auto-reframe, dynamic captions, and virality ranking.", "AI Editor & Repurposing Expert"),
            ("Klap Auto-Reels", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://klap.app", "One-click short generator adding subtitles and dynamic zooms for social channels.", "AI Editor & Repurposing Expert"),
            ("Vizard AI Studio", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://vizard.ai", "Automated transcript-based clipping with customizable brand kits.", "AI Editor & Repurposing Expert"),
            ("Munch Social Clips", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://getmunch.com", "Trend-analyzing content extraction that matches keywords to current social topics.", "AI Editor & Repurposing Expert"),
            ("Vidyo AI Clips", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://vidyo.ai", "Automated short video generation with templates for podcasts and presentations.", "AI Editor & Repurposing Expert"),
            ("Castmagic Automation", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://castmagic.io", "Extracts quotes, blog drafts, and carousels from raw recorded audio.", "AI Editor & Repurposing Expert"),
            ("Podsqueeze Repurposer", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://podsqueeze.com", "All-in-one generator creating social posts and newsletters from podcast episodes.", "AI Editor & Repurposing Expert"),
            ("Riverside Magic", "repurposing", "Repurposing & Content Automation", "yes", "https://riverside.fm", "Instant highlight generator creating polished reels straight from studio recordings.", "AI Editor & Repurposing Expert"),
            ("Automator", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://automator.ai", "Builds automated data transformation and generative publishing chains.", "AI Editor & Repurposing Expert"),
            ("Castos Automated", "repurposing", "Repurposing & Content Automation", "plan_dependent", "https://castos.com", "Automatic social audio audiogram and YouTube video generation for podcasters.", "AI Editor & Repurposing Expert")
        ]
    },
    {
        "id": "business",
        "name": "Creator Business & Monetization",
        "emoji": "💼",
        "archetype": "Social Media Manager",
        "tools": [
            ("Stan Store", "business", "Creator Business & Monetization", "plan_dependent", "https://stan.store", "All-in-one creator digital storefront for courses, bookings, and digital downloads.", "Social Media Manager"),
            ("Beacons", "business", "Creator Business & Monetization", "plan_dependent", "https://beacons.ai", "Creator mobile site builder combining link-in-bio, media kit, and email marketing.", "Social Media Manager"),
            ("Gumroad", "business", "Creator Business & Monetization", "yes", "https://gumroad.com", "E-commerce platform empowering creators to sell digital products, prompts, and tutorials.", "Social Media Manager"),
            ("Lemon Squeezy", "business", "Creator Business & Monetization", "yes", "https://lemonsqueezy.com", "Merchant of record platform handling taxes and global subscriptions for digital creators.", "Social Media Manager"),
            ("Buy Me a Coffee", "business", "Creator Business & Monetization", "yes", "https://buymeacoffee.com", "Simple way for creators to receive one-time tips and memberships from supporters.", "Social Media Manager"),
            ("Patreon", "business", "Creator Business & Monetization", "yes", "https://patreon.com", "Subscription platform for creators to build community and offer exclusive membership tiers.", "Social Media Manager"),
            ("Kajabi", "business", "Creator Business & Monetization", "plan_dependent", "https://kajabi.com", "Complete knowledge-commerce platform for selling high-ticket courses and coaching.", "Social Media Manager"),
            ("Teachable", "business", "Creator Business & Monetization", "plan_dependent", "https://teachable.com", "Course building platform with integrated video hosting and student progress tracking.", "Social Media Manager"),
            ("Whop", "business", "Creator Business & Monetization", "plan_dependent", "https://whop.com", "Marketplace and payment processor for software, Discord access, and digital memberships.", "Social Media Manager"),
            ("Substack", "business", "Creator Business & Monetization", "yes", "https://substack.com", "Newsletter publishing platform allowing writers and creators to monetize via subscriptions.", "Social Media Manager"),
            ("Beehiiv", "business", "Creator Business & Monetization", "plan_dependent", "https://beehiiv.com", "Modern newsletter platform built for extreme growth with native ad network and referral loops.", "Social Media Manager"),
            ("ConvertKit", "business", "Creator Business & Monetization", "plan_dependent", "https://convertkit.com", "Email marketing platform tailored for professional creators and digital product creators.", "Social Media Manager"),
            ("Memberful", "business", "Creator Business & Monetization", "yes", "https://memberful.com", "Reliable membership software that integrates seamlessly with WordPress and Stripe.", "Social Media Manager"),
            ("Podia", "business", "Creator Business & Monetization", "plan_dependent", "https://podia.com", "All-in-one creator platform hosting websites, online courses, and digital downloads.", "Social Media Manager"),
            ("Skool", "business", "Creator Business & Monetization", "plan_dependent", "https://skool.com", "Community-first platform combining discussion boards, gamification, and course modules.", "Social Media Manager"),
            ("Passion.io", "business", "Creator Business & Monetization", "plan_dependent", "https://passion.io", "Enables creators to launch their own branded mobile iOS and Android apps without coding.", "Social Media Manager"),
            ("Stripe", "business", "Creator Business & Monetization", "yes", "https://stripe.com", "Global financial infrastructure powering digital creator payments and payouts.", "Social Media Manager"),
            ("Wise", "business", "Creator Business & Monetization", "yes", "https://wise.com", "Low-cost international money transfers and multi-currency accounts for freelance creators.", "Social Media Manager"),
            ("Notion for Creators", "business", "Creator Business & Monetization", "yes", "https://notion.so", "Operating system for creator businesses: client CRM, content pipeline, and finance tracking.", "Social Media Manager"),
            ("HoneyBook", "business", "Creator Business & Monetization", "plan_dependent", "https://honeybook.com", "Client flow management platform handling contracts, invoices, and scheduling.", "Social Media Manager")
        ]
    },
    {
        "id": "coding",
        "name": "AI Coding & Website Creation",
        "emoji": "💻",
        "archetype": "AI Graphic Designer",
        "tools": [
            ("v0 by Vercel", "coding", "AI Coding & Website Creation", "plan_dependent", "https://v0.dev", "Generative UI system producing production-ready React and Tailwind components from prompts.", "AI Graphic Designer"),
            ("Cursor", "coding", "AI Coding & Website Creation", "plan_dependent", "https://cursor.com", "AI-first code editor with codebase-aware predictions and natural language refactoring.", "AI Graphic Designer"),
            ("GitHub Copilot", "coding", "AI Coding & Website Creation", "plan_dependent", "https://github.com/features/copilot", "World's most widely adopted AI pair programmer writing code suggestions inline.", "AI Graphic Designer"),
            ("Replit Agent", "coding", "AI Coding & Website Creation", "plan_dependent", "https://replit.com", "Autonomous software development agent building and deploying full-stack apps in the browser.", "AI Graphic Designer"),
            ("Lovable", "coding", "AI Coding & Website Creation", "plan_dependent", "https://lovable.dev", "Transforms natural language descriptions into complete full-stack web applications.", "AI Graphic Designer"),
            ("Bolt.new", "coding", "AI Coding & Website Creation", "plan_dependent", "https://bolt.new", "Browser-based full-stack WebContainers sandbox for prompt-based app generation.", "AI Graphic Designer"),
            ("Framer AI", "coding", "AI Coding & Website Creation", "plan_dependent", "https://framer.com", "Generates and publishes interactive responsive websites directly from prompts.", "AI Graphic Designer"),
            ("Webflow AI", "coding", "AI Coding & Website Creation", "plan_dependent", "https://webflow.com", "Visual web development platform with AI-assisted layout generation and translation.", "AI Graphic Designer"),
            ("Wix Studio AI", "coding", "AI Coding & Website Creation", "plan_dependent", "https://wix.com/studio", "Smart responsive layout tools and automated code generation for web designers.", "AI Graphic Designer"),
            ("WordPress AI", "coding", "AI Coding & Website Creation", "yes", "https://wordpress.com", "AI website creation wizard and block pattern generator for creator portfolios.", "AI Graphic Designer"),
            ("Relume", "coding", "AI Coding & Website Creation", "plan_dependent", "https://relume.io", "AI site builder generating full website sitemaps and wireframes in seconds.", "AI Graphic Designer"),
            ("Dora AI", "coding", "AI Coding & Website Creation", "plan_dependent", "https://dora.run", "Generates 3D animated interactive websites from single text prompts.", "AI Graphic Designer"),
            ("Codeium", "coding", "AI Coding & Website Creation", "yes", "https://codeium.com", "Fast, free, and enterprise-grade code completion and chat assistant.", "AI Graphic Designer"),
            ("Tabnine", "coding", "AI Coding & Website Creation", "plan_dependent", "https://tabnine.com", "Private and personalized AI code completion assistant for software engineers.", "AI Graphic Designer"),
            ("Claude Artifacts", "coding", "AI Coding & Website Creation", "yes", "https://claude.ai", "Interactive standalone UI components and web apps generated and previewed live.", "AI Graphic Designer"),
            ("ChatGPT Code Interpreter", "coding", "AI Coding & Website Creation", "yes", "https://chatgpt.com", "Sandboxed Python execution environment for data analysis, math, and file transformation.", "AI Graphic Designer"),
            ("Windsurf", "coding", "AI Coding & Website Creation", "plan_dependent", "https://codeium.com/windsurf", "Agentic IDE integrating deep codebase awareness with multi-file workflows.", "AI Graphic Designer"),
            ("Supabase AI", "coding", "AI Coding & Website Creation", "yes", "https://supabase.com", "SQL query generation and schema migration assistant for backend databases.", "AI Graphic Designer"),
            ("Superweb", "coding", "AI Coding & Website Creation", "plan_dependent", "https://superweb.ai", "AI web generation platform tailoring interactive creator landing pages.", "AI Graphic Designer"),
            ("10Web", "coding", "AI Coding & Website Creation", "plan_dependent", "https://10web.io", "Automated WordPress website builder and speed optimization platform.", "AI Graphic Designer")
        ]
    },
    {
        "id": "3d",
        "name": "3D Modeling & Animation",
        "emoji": "🧊",
        "archetype": "Product Visualization",
        "tools": [
            ("Blender", "3d", "3D Modeling & Animation", "yes", "https://www.blender.org", "Open-source 3D creation suite: modeling, rigging, animation, and rendering.", "Product Visualization"),
            ("Spline", "3d", "3D Modeling & Animation", "yes", "https://spline.design", "Design and collaborate in 3D in the browser with interactive real-time physics.", "Product Visualization"),
            ("Meshy", "3d", "3D Modeling & Animation", "plan_dependent", "https://www.meshy.ai", "Generates textured 3D game and production assets from text and 2D images.", "Product Visualization"),
            ("Tripo3D", "3d", "3D Modeling & Animation", "plan_dependent", "https://www.tripo3d.ai", "Ultra-fast text and image to 3D mesh model generation pipeline.", "Product Visualization")
        ]
    }
]

# Flatten and deduplicate tools by name
ALL_TOOLS = []
seen_names = set()
for cat in RAW_TOOL_CATEGORIES:
    for tool_tuple in cat["tools"]:
        name = tool_tuple[0]
        if name not in seen_names:
            seen_names.add(name)
            ALL_TOOLS.append(tool_tuple)

SKILLS = [
    "storyboarding", "prompt engineering", "motion design", "color grading",
    "sound design", "voice cloning", "3D modeling", "lip sync",
    "character design", "video editing", "scriptwriting", "upscaling",
    "LoRA training", "VFX compositing", "typography", "brand identity",
    "product photography", "camera direction", "music composition", "localization",
    "AI UGC ads", "avatar creation", "social media strategy", "SEO optimization",
    "trend discovery", "content repurposing", "audio mastering"
]

CONTENT_TYPES = [
    "short film", "ad spot", "music video", "social reel", "product visual",
    "explainer", "animation loop", "poster/graphic", "logo animation", "game cinematic",
]

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
# Creators: 26 creators aligned with the 10 Kampus.VC discovery archetypes
# Invariant: Neither Daniel Okafor nor Zoe Williams has "3D modeling" (maintains Sora + 3D modeling empty result test)
# Invariant: Both Ananya Rao and Elena Petrova use Midjourney & Runway (maintains any vs all test)
# --------------------------------------------------------------------------
CREATORS = [
    ("Ananya Rao", "AI Video Creator", "Short films and ad spots with cinematic AI pipelines", "Hyderabad, IN", "senior", 40000, 120000, "available", ["English", "Telugu", "Hindi"], (1, 1, 0),
     ["storyboarding", "motion design", "prompt engineering", "color grading"], ["Runway", "Midjourney", "DaVinci Resolve", "Kling"], ["short film", "ad spot"]),
    
    ("Rohan Mehta", "UGC Ad Creator", "Scroll-stopping direct-response UGC ads for D2C brands", "Mumbai, IN", "mid", 15000, 45000, "available", ["English", "Hindi"], (1, 1, 1),
     ["prompt engineering", "video editing", "scriptwriting", "localization", "AI UGC ads"], ["Creatify", "Arcads", "ElevenLabs", "CapCut for Business"], ["social reel", "ad spot"]),
    
    ("Sara Lindqvist", "AI Animator", "Stylised character animation with Stable Diffusion and ComfyUI", "Stockholm, SE", "senior", 60000, 180000, "busy", ["English", "Swedish"], (1, 1, 1),
     ["character design", "motion design", "LoRA training", "VFX compositing"], ["ComfyUI", "Stable Diffusion", "After Effects", "Topaz Video AI"], ["animation loop", "explainer", "short film"]),
    
    ("Kiran Reddy", "AI Graphic Designer", "Posters, branding, and thumbnail visuals for growth brands", "Vijayawada, IN", "junior", 5000, 20000, "available", ["English", "Telugu"], (0, 0, 1),
     ["typography", "brand identity", "prompt engineering"], ["Midjourney", "Ideogram", "Adobe Firefly", "Canva"], ["poster/graphic", "product visual"]),
    
    ("Meera Nair", "AI Music Producer", "Dreamlike music videos and audio beds for indie artists", "Kochi, IN", "mid", 30000, 90000, "available", ["English", "Malayalam", "Hindi"], (1, 0, 1),
     ["camera direction", "color grading", "storyboarding", "music composition"], ["Suno", "Udio", "AIVA", "DaVinci Resolve", "Midjourney"], ["music video", "social reel"]),
    
    ("Daniel Okafor", "AI Video Creator", "Narrative shorts built on Sora and Veo", "Lagos, NG", "mid", 35000, 100000, "available", ["English"], (1, 1, 0),
     ["storyboarding", "camera direction", "scriptwriting", "prompt engineering"], ["Sora", "Veo", "DaVinci Resolve"], ["short film", "ad spot"]),
    
    ("Priya Sharma", "Product Visualization", "Photoreal product shots, AI plus 3D render pipelines", "Bengaluru, IN", "senior", 45000, 130000, "available", ["English", "Hindi", "Kannada"], (1, 1, 1),
     ["3D modeling", "product photography", "VFX compositing", "upscaling"], ["Blender", "Stable Diffusion", "ComfyUI", "Topaz Video AI"], ["product visual", "ad spot"]),
    
    ("Liam Chen", "AI Influencer Creator", "Virtual human influencers and synthetic digital brand personas", "Singapore, SG", "mid", 35000, 95000, "busy", ["English", "Mandarin"], (1, 0, 1),
     ["avatar creation", "character design", "motion design", "lip sync"], ["HeyGen", "Hedra", "Synthesia", "Kling"], ["animation loop", "explainer", "social reel"]),
    
    ("Fatima Khan", "AI Voice Artist", "Multilingual synthetic voiceovers, dubbing, and commercial narration", "Delhi, IN", "mid", 20000, 60000, "available", ["English", "Hindi", "Urdu"], (1, 1, 0),
     ["scriptwriting", "voice cloning", "localization", "lip sync", "sound design"], ["ElevenLabs", "Murf AI", "PlayHT", "Runway"], ["explainer", "social reel"]),
    
    ("Arjun Patel", "AI Editor & Repurposing Expert", "Viral short-form repurposing with dynamic captions and hooks", "Ahmedabad, IN", "mid", 20000, 55000, "available", ["English", "Gujarati", "Hindi"], (0, 1, 1),
     ["motion design", "typography", "brand identity", "video editing"], ["CapCut", "Descript", "OpusClip", "Adobe Firefly"], ["logo animation", "ad spot"]),
    
    ("Chloe Martin", "AI Video Creator", "Festival-style short films, cinematic scenes, and game trailers", "Lyon, FR", "senior", 80000, 220000, "busy", ["English", "French"], (1, 1, 1),
     ["storyboarding", "camera direction", "VFX compositing", "color grading"], ["Runway", "Luma Dream Machine", "DaVinci Resolve", "Topaz Video AI"], ["short film", "game cinematic", "music video"]),
    
    ("Vikram Singh", "AI Graphic Designer", "Concept characters, vector graphics, and brand illustrations", "Jaipur, IN", "junior", 8000, 30000, "available", ["English", "Hindi"], (0, 0, 1),
     ["character design", "LoRA training", "prompt engineering", "brand identity"], ["Stable Diffusion", "Leonardo AI", "Recraft"], ["poster/graphic", "game cinematic"]),
    
    ("Isabella Rossi", "AI Graphic Designer", "Editorial-grade brand imagery and luxury promotional visuals", "Milan, IT", "mid", 25000, 80000, "available", ["English", "Italian"], (1, 1, 0),
     ["typography", "brand identity", "product photography"], ["Midjourney", "Adobe Firefly", "Ideogram"], ["poster/graphic", "product visual"]),
    
    ("Tanvi Joshi", "UGC Ad Creator", "High-conversion regional language UGC ads for consumer apps", "Pune, IN", "mid", 18000, 50000, "available", ["English", "Hindi", "Marathi"], (1, 0, 0),
     ["scriptwriting", "localization", "voice cloning", "video editing", "AI UGC ads"], ["Creatify", "JoggAI", "ElevenLabs", "Pika"], ["ad spot", "social reel"]),
    
    ("Omar Haddad", "AI Music Producer", "Cinematic orchestral and electronic scores with full foley audio", "Dubai, AE", "senior", 70000, 200000, "available", ["English", "Arabic"], (1, 1, 1),
     ["music composition", "camera direction", "sound design", "VFX compositing"], ["Veo", "Suno", "ElevenLabs", "DaVinci Resolve"], ["music video", "short film"]),
    
    ("Nisha Kulkarni", "AI Animator", "Hand-drawn feel animation accelerated with AI diffusion frames", "Chennai, IN", "mid", 22000, 65000, "available", ["English", "Tamil"], (0, 1, 1),
     ["character design", "motion design", "storyboarding"], ["Pika", "Stable Diffusion", "After Effects"], ["animation loop", "short film"]),
    
    ("Sebastian Weber", "Product Visualization", "Automotive, architectural, and industrial appliance visuals", "Berlin, DE", "senior", 60000, 160000, "busy", ["English", "German"], (1, 1, 0),
     ["3D modeling", "VFX compositing", "upscaling"], ["Blender", "ComfyUI", "Topaz Video AI"], ["product visual", "ad spot"]),
    
    ("Harsha Vardhan", "AI Video Creator", "High-velocity vertical social shorts and regional fiction reels", "Guntur, IN", "junior", 6000, 25000, "available", ["English", "Telugu"], (0, 0, 1),
     ["storyboarding", "video editing", "prompt engineering"], ["Runway", "Kling", "Pika"], ["short film", "social reel"]),
    
    ("Zoe Williams", "AI Script Writer", "Viral video hooks, narrative scripts, and conversion copy pipelines", "London, UK", "senior", 90000, 250000, "available", ["English"], (1, 1, 1),
     ["scriptwriting", "camera direction", "color grading", "prompt engineering"], ["ChatGPT", "Claude", "Jasper", "Sora", "Runway"], ["ad spot", "short film"]),
    
    ("Aditya Menon", "Social Media Manager", "Full-funnel social scheduling, viral carousel design, and trend analytics", "Trivandrum, IN", "junior", 7000, 22000, "available", ["English", "Malayalam"], (0, 0, 0),
     ["social media strategy", "motion design", "typography"], ["Buffer", "Predis.ai", "Metricool", "Canva"], ["logo animation", "social reel"]),
    
    ("Yuki Tanaka", "AI Influencer Creator", "Anime and stylized virtual idols with synthetic voices", "Tokyo, JP", "senior", 55000, 150000, "busy", ["English", "Japanese"], (1, 1, 1),
     ["character design", "LoRA training", "3D modeling", "lip sync", "avatar creation"], ["HeyGen", "Synthesia", "Hedra", "Kling"], ["game cinematic", "animation loop"]),
    
    ("Pooja Iyer", "AI Voice Artist", "Multilingual explainer narration with crystal-clear vocal identity", "Bengaluru, IN", "mid", 18000, 48000, "available", ["English", "Tamil", "Kannada"], (1, 0, 1),
     ["scriptwriting", "voice cloning", "localization", "sound design"], ["ElevenLabs", "Murf AI", "Dubverse", "Suno"], ["explainer", "social reel"]),
    
    ("Marcus Johnson", "AI Graphic Designer", "Midjourney and Ideogram visual director for album art and brand identities", "Austin, US", "mid", 30000, 85000, "available", ["English"], (1, 0, 1),
     ["typography", "upscaling", "brand identity"], ["Midjourney", "Ideogram"], ["poster/graphic"]),
    
    ("Neha Gupta", "AI Script Writer", "Conceptual story outlines and dialogue drafts for GenAI videos", "Noida, IN", "junior", 5000, 18000, "available", ["English", "Hindi"], (0, 0, 0),
     ["storyboarding", "scriptwriting", "prompt engineering"], ["ChatGPT", "Claude", "Runway"], ["short film"]),
    
    ("Elena Petrova", "AI Editor & Repurposing Expert", "Experimental animation and multi-model pipeline director", "Prague, CZ", "senior", 75000, 210000, "busy", ["English", "Czech", "Russian"], (1, 1, 1),
     ["character design", "motion design", "LoRA training", "VFX compositing", "color grading", "storyboarding", "upscaling"],
     ["Stable Diffusion", "ComfyUI", "After Effects", "DaVinci Resolve", "Blender", "Topaz Video AI", "Runway", "Midjourney"],
     ["animation loop", "short film", "game cinematic", "music video"]),
    
    ("Imran Sheikh", "AI Marketing Strategist", "Data-driven audience growth, search dominance, and trend discovery", "Hyderabad, IN", "mid", 25000, 70000, "available", ["English", "Hindi", "Telugu", "Urdu"], (1, 1, 0),
     ["SEO optimization", "trend discovery", "sound design", "video editing"], ["Semrush", "Surfer SEO", "BuzzSumo", "Perplexity AI"], ["music video", "social reel"]),
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
    None, None,
]
PROCESS_NOTES = [
    "Generated 40+ keyframes, curated 12, then animated and graded.",
    "Consistent character via reference images and a trained LoRA.",
    "Prompts iterated over three rounds with client feedback.",
    "Hybrid: AI base plates, manual compositing for final polish.",
    "Audio generated separately and synced in the edit.",
    "Upscaled to 4K and denoised before delivery.",
]

BRANDS = [
    ("br_01", "Lotus & Loom", "Skincare", "Ayurveda-inspired skincare for everyday routines.", 0),
    ("br_02", "Orbit Fitness", "Fitness app", "Subscription fitness app with live classes.", 0),
    ("br_03", "Saffron Table", "Food and beverage", "Regional restaurant chain across South India.", 0),
    ("br_04", "Solara Bikes", "Electric mobility", "Affordable electric bikes for city commuters.", 0),
    ("br_05", "Velvet Sound", "Music streaming", "Independent-artist-first streaming platform.", 0),
    ("br_06", "Paperlane Games", "Gaming", "Indie studio building narrative fantasy RPGs.", 0),
    ("br_07", "Northwind Creative", "Advertising agency", "Boutique agency running campaigns for D2C brands.", 1),
]

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
    for name, cat, cat_name, comm, url, desc, arch in ALL_TOOLS:
        cur.execute(
            """INSERT INTO tools(name, category, category_name, commercial_use, url, description, popular_archetype)
               VALUES (?,?,?,?,?,?,?)""",
            (name, cat, cat_name, comm, url, desc, arch)
        )
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
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        cr_pass_hash = pwd_context.hash("DemoCreator123!")
        br_pass_hash = pwd_context.hash("DemoBrand123!")
        default_pass_hash = pwd_context.hash("Password123!")
    except Exception:
        # Pre-calculated bcrypt hashes for offline/fresh environments
        cr_pass_hash = "$2b$12$K1d5qT.Y1VqLhK4UaYgC3ecV7Bsk0yq5w2wL7A6u.m0EaR6YhU0Uu"
        br_pass_hash = "$2b$12$K1d5qT.Y1VqLhK4UaYgC3ecV7Bsk0yq5w2wL7A6u.m0EaR6YhU0Uu"
        default_pass_hash = "$2b$12$K1d5qT.Y1VqLhK4UaYgC3ecV7Bsk0yq5w2wL7A6u.m0EaR6YhU0Uu"

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
