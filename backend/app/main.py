from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ App started")
    yield
    print("✅ App shut down")

app = FastAPI(title="AI Story Weaver Pro", description="Agentic storytelling platform", lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Configure for production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Lazy import routers to avoid initialization issues
try:
    from .api.v1.stories import router as stories_router
    app.include_router(stories_router, prefix="/api/v1/stories", tags=["stories"])
    print("✅ Stories router loaded successfully")
except Exception as e:
    print(f"❌ Failed to load stories router: {e}")
    # Continue without stories router for basic functionality