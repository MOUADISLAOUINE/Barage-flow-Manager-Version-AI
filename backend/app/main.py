"""
Barrage-Flow Manager — FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# ── App instance ────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Smart dam management system for Youssef Ibn Tachfine Dam, Tiznit — Morocco.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS ────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health check (used by Docker & CI) ──────────────────────────────
@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


# ── API Router ──────────────────────────────────────────────────────
# TODO: Uncomment once api router is built:
# from app.api.v1.router import api_router
# app.include_router(api_router, prefix="/api/v1")
