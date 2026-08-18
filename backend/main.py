"""
Code Analyzer - FastAPI Backend
================================
Entry point for the FastAPI application.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.db.database import engine, Base
from analysis.routers import analyze, history, home


# ─────────────────────────────────────────────
# Lifespan: create DB tables on startup
# ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all database tables on startup."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created / verified.")
    yield
    print("🔴 Server shutting down.")


# ─────────────────────────────────────────────
# App instance
# ─────────────────────────────────────────────
app = FastAPI(
    title="Code Analyzer API",
    description="Analyze, correct, and optimize code using Gemini AI",
    version="1.0.0",
    lifespan=lifespan,
)

# ─────────────────────────────────────────────
# CORS — allow React dev server on port 3000
# ─────────────────────────────────────────────


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Routers
# ─────────────────────────────────────────────
app.include_router(home.router,    prefix="/api",         tags=["Home"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(history.router, prefix="/api/history", tags=["History"])

@app.get("/", tags=["Root"])
def root():
    return {"message": "Code Analyzer API is running 🚀", "docs": "/docs"}
