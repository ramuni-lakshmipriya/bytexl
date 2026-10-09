import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import meta, creators, briefs, auth, dashboard
from backend.database import ensure_db

app = FastAPI(
    title="AI Content Creator Marketplace API",
    description="API connecting AI creators with brands and creative agencies.",
    version="1.0.0"
)

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")

# Enable CORS for exact frontend origins (no wildcard when allow_credentials=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    ensure_db()

# Mount routers
app.include_router(auth.router)
app.include_router(meta.router)
app.include_router(creators.router)
app.include_router(briefs.router)
app.include_router(dashboard.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
