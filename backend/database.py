import os
import sqlite3
import subprocess
from pathlib import Path

# Path resolution: find dataset/marketplace.db relative to backend or root
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dataset" / "marketplace.db"
SEED_SCRIPT_PATH = BASE_DIR / "dataset" / "seed.py"

def ensure_db():
    """Ensure marketplace.db exists and has the latest schema and tools."""
    needs_seed = False
    if not DB_PATH.exists():
        needs_seed = True
    else:
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(tools);")
            cols = [row[1] for row in cursor.fetchall()]
            if "category_name" not in cols or "popular_archetype" not in cols:
                needs_seed = True
            else:
                cursor.execute("SELECT COUNT(*) FROM tools;")
                count = cursor.fetchone()[0]
                if count < 50:
                    needs_seed = True
            conn.close()
        except Exception:
            needs_seed = True

    if needs_seed:
        print(f"Database missing or outdated at {DB_PATH}. Initializing database...")
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("seed", str(SEED_SCRIPT_PATH))
            seed_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(seed_module)
            seed_module.build_db(str(DB_PATH))
            print("Successfully initialized marketplace.db with 250+ tools in-process!")
        except Exception as e:
            print(f"In-process seeding failed ({e}), attempting subprocess fallback...")
            try:
                subprocess.run(["python", str(SEED_SCRIPT_PATH)], check=True)
            except Exception as e2:
                print(f"Subprocess seeding also failed: {e2}")

def get_db():
    """Returns a new sqlite3 connection with Row factory enabled."""
    ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")

    # Ensure auxiliary tables exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS brief_applications (
            id                 TEXT PRIMARY KEY,
            brief_id           TEXT NOT NULL REFERENCES briefs(id) ON DELETE CASCADE,
            creator_id         TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
            pitch              TEXT,
            proposed_rate_inr  INTEGER,
            estimated_days     INTEGER,
            status             TEXT NOT NULL DEFAULT 'applied',
            delivery_url       TEXT,
            delivery_notes     TEXT,
            revision_feedback  TEXT,
            payment_status     TEXT DEFAULT 'escrow_held',
            created_at         TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at         TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(brief_id, creator_id)
        );
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS starter_studio_projects (
            id           TEXT PRIMARY KEY,
            creator_id   TEXT NOT NULL REFERENCES creators(id) ON DELETE CASCADE,
            title        TEXT NOT NULL,
            project_type TEXT NOT NULL,
            status       TEXT NOT NULL DEFAULT 'in_progress',
            notes        TEXT,
            created_at   TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn

