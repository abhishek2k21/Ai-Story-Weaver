#!/usr/bin/env python3
"""
Debug server startup
"""

import os
import sys
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add backend to path
sys.path.insert(0, 'backend')

app = FastAPI(title="AI Story Weaver Pro", description="Agentic storytelling platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Story Weaver Pro"}

@app.on_event("startup")
async def startup_event():
    """Initialize routers on startup."""
    try:
        from app.api.v1.stories import router as stories_router
        app.include_router(stories_router, prefix="/api/v1/stories", tags=["stories"])
        print("✅ Stories router loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load stories router: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")