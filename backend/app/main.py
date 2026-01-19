from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Story Weaver Pro", description="Agentic storytelling platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AI Story Weaver Pro"}

# Lazy import routers to avoid initialization issues
@app.on_event("startup")
async def startup_event():
    """Initialize routers on startup."""
    try:
        from app.api.v1.stories import router as stories_router
        app.include_router(stories_router, prefix="/api/v1/stories", tags=["stories"])
        print("✅ Stories router loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load stories router: {e}")
        # Continue without stories router for basic functionality