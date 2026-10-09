#!/usr/bin/env python3
"""
One-command local runner for AI Content Creator Marketplace.
Starts FastAPI backend server and Vite frontend dev server concurrently.
"""
import os
import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
DB_PATH = BASE_DIR / "dataset" / "marketplace.db"
SEED_SCRIPT = BASE_DIR / "dataset" / "seed.py"

def main():
    print("=" * 70)
    print("🚀 AI Content Creator Marketplace - Launcher")
    print("=" * 70)

    # 1. Ensure database exists
    if not DB_PATH.exists():
        print(f"📦 Database missing. Running seed script...")
        subprocess.run([sys.executable, str(SEED_SCRIPT)], check=True)
    else:
        print(f"✓ Database verified at {DB_PATH}")

    # 2. Launch Backend Process
    print("⚡ Starting FastAPI Backend on http://127.0.0.1:8000...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=str(BASE_DIR)
    )

    # 3. Launch Frontend Process
    print("🎨 Starting Vite Frontend on http://127.0.0.1:3000...")
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    frontend_proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(FRONTEND_DIR)
    )

    time.sleep(2)
    print("\n" + "=" * 70)
    print("✨ Both Backend and Frontend are running!")
    print("🌐 Frontend App:      http://localhost:3000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("=" * 70)
    print("Press Ctrl+C to stop servers.\n")

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping processes...")
        backend_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
