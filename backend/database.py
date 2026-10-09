import os
import sqlite3
import subprocess
from pathlib import Path

# Path resolution: find dataset/marketplace.db relative to backend or root
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dataset" / "marketplace.db"
SEED_SCRIPT_PATH = BASE_DIR / "dataset" / "seed.py"

def ensure_db():
    """Ensure marketplace.db exists. If missing, run seed.py to create it."""
    if not DB_PATH.exists():
        print(f"Database missing at {DB_PATH}. Executing seed script...")
        subprocess.run(["python", str(SEED_SCRIPT_PATH)], check=True)

def get_db():
    """Returns a new sqlite3 connection with Row factory enabled."""
    ensure_db()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
