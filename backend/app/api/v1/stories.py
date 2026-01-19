# Generation, branching, exports

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

def check_api_keys_configured() -> bool:
    """Check if real API keys are configured (not placeholder values)."""
    openai_key = os.getenv("OPENAI_API_KEY", "")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

    # Check if keys are configured and not placeholder values
    openai_valid = openai_key and not openai_key.startswith("your-") and len(openai_key) > 20
    anthropic_valid = anthropic_key and not anthropic_key.startswith("your-") and len(anthropic_key) > 20

    return openai_valid or anthropic_valid

# Initialize agents - will be None if API keys not configured
USE_REAL_AGENTS = check_api_keys_configured()

if USE_REAL_AGENTS:
    try:
        # Only import agents if we have API keys
        from ...services.architect import ArchitectAgent
        from ...services.scribe import ScribeAgent
        from ...services.editor import EditorAgent
        from ...services.causality import CausalityAgent

        logger.info("Real API keys detected - initializing real AI agents")
        architect = ArchitectAgent()
        scribe = ScribeAgent()
        editor = EditorAgent()
        causality_agent = CausalityAgent()
    except Exception as e:
        logger.warning(f"Failed to initialize real agents: {e}. Using mock responses.")
        USE_REAL_AGENTS = False
        architect = None
        scribe = None
        editor = None
        causality_agent = None
else:
    logger.info("Using mock responses - configure real API keys for AI agent integration")
    architect = None
    scribe = None
    editor = None
    causality_agent = None

class StoryRequest(BaseModel):
    prompt: str
    genre: Optional[str] = None
    length: Optional[str] = "short_story"
    story_bible: Optional[Dict[str, Any]] = None

class StoryResponse(BaseModel):
    story_id: str
    title: str
    content: str
    outline: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    created_at: datetime

@router.post("/generate", response_model=StoryResponse)
async def generate_story(request: StoryRequest, background_tasks: BackgroundTasks):
    """Generate a complete story from a prompt."""
    try:
        logger.info(f"Generating story for prompt: {request.prompt[:50]}...")

        if USE_REAL_AGENTS and architect and scribe and editor and causality_agent:
            # Use real AI agents
            logger.info("Using real AI agents for story generation")

            # Step 1: Plan the story with Architect
            outline = architect.plan_story(request.prompt, request.story_bible)

            # Step 2: Write the draft with Scribe
            draft = scribe.write_draft(outline.dict(), request.length)

            # Step 3: Edit and improve with Editor
            final_content, metrics = editor.iterative_improvement(
                draft.content,
                outline.dict()
            )

            # Step 4: Validate causality
            causal_check = causality_agent.validate_causal_consistency(
                outline.causal_chains
            )

            # Create response
            response = StoryResponse(
                story_id=f"story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                title=outline.title,
                content=final_content,
                outline=outline.dict(),
                quality_metrics={
                    "overall_score": metrics.overall_score,
                    "causal_integrity": causal_check["confidence_score"],
                    "issues": metrics.issues_found,
                    "suggestions": metrics.suggestions
                },
                created_at=datetime.now()
            )
        else:
            # Use mock response for testing/development
            logger.info("Using mock response for story generation (configure API keys for real AI)")

            mock_story = {
                "story_id": f"mock_story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "title": "The Enchanted Forest Journey",
                "content": f"""In the heart of an ancient forest, young Alex stood at the crossroads of fear and courage. The prompt you gave was: "{request.prompt}"

This is a therapeutic story about overcoming anxiety through magical means. The forest represents the subconscious mind, where fears lurk in the shadows but wisdom waits in the light.

As Alex took the first step forward, the trees seemed to whisper encouragement. "Every journey begins with a single step," they rustled. The path ahead was unclear, but Alex remembered that anxiety often feels overwhelming, yet it's just a feeling - not a fact.

Deeper in the forest, Alex encountered a wise old owl perched on a glowing branch. "Anxiety is like a storm cloud," the owl hooted. "It passes, but the sun always returns." With this wisdom, Alex learned that feelings are temporary visitors.

The journey continued through meadows of wildflowers, each petal representing a moment of peace. Alex collected these petals as reminders that calm exists within the chaos.

Finally, at the forest's heart, Alex found a crystal-clear lake reflecting the sky above. Looking into the water, Alex saw not just their reflection, but their inner strength shining through.

The forest had taught its lesson: anxiety may visit, but it doesn't define us. We are the courageous explorers of our own minds, capable of finding peace even in the wildest storms.

*This is a mock story generated for testing. Configure real API keys to enable AI-powered therapeutic storytelling.*""",
                "outline": {
                    "title": "The Enchanted Forest Journey",
                    "genre": "therapeutic_fantasy",
                    "main_characters": [
                        {"name": "Alex", "role": "protagonist", "traits": ["anxious", "courageous", "curious"]},
                        {"name": "Wise Owl", "role": "mentor", "traits": ["wise", "compassionate"]}
                    ],
                    "plot_summary": "A journey through a magical forest teaching anxiety management",
                    "key_scenes": [
                        {"scene": "Forest Entrance", "purpose": "Facing initial fears"},
                        {"scene": "Owl Encounter", "purpose": "Learning wisdom"},
                        {"scene": "Crystal Lake", "purpose": "Self-discovery"}
                    ],
                    "themes": ["anxiety_management", "inner_strength", "mindfulness"]
                },
                "quality_metrics": {
                    "overall_score": 8.5,
                    "causal_integrity": 0.85,
                    "issues": ["Mock data - not analyzed"],
                    "suggestions": ["Configure API keys for real AI analysis"]
                },
                "created_at": datetime.now()
            }

            response = StoryResponse(**mock_story)

        logger.info(f"Successfully generated story: {response.title}")

        return response

    except Exception as e:
        logger.error(f"Error generating story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")

@router.post("/outline")
async def create_outline(request: StoryRequest):
    """Generate just a story outline."""
    try:
        outline = architect.plan_story(request.prompt, request.story_bible)
        return {
            "outline": outline.dict(),
            "causal_analysis": outline.causal_chains
        }
    except Exception as e:
        logger.error(f"Error creating outline: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Outline creation failed: {str(e)}")

@router.post("/revise")
async def revise_story(story_content: str, feedback: str):
    """Revise an existing story based on feedback."""
    try:
        # Use Editor to revise
        revised = scribe.revise_scene(story_content, feedback)
        return {"revised_content": revised}
    except Exception as e:
        logger.error(f"Error revising story: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Story revision failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": {
            "architect": "ready" if USE_REAL_AGENTS else "mock",
            "scribe": "ready" if USE_REAL_AGENTS else "mock",
            "editor": "ready" if USE_REAL_AGENTS else "mock",
            "causality": "ready" if USE_REAL_AGENTS else "mock"
        },
        "ai_integration": "enabled" if USE_REAL_AGENTS else "disabled (configure API keys)",
        "timestamp": datetime.now()
    }

@router.post("/test-generate", response_model=StoryResponse)
async def test_generate_story(request: StoryRequest):
    """Test endpoint that returns a mock story for frontend testing (always uses mock responses)."""
    try:
        logger.info(f"Test generating story for prompt: {request.prompt[:50]}...")

        # Mock response for testing
        mock_story = {
            "story_id": f"test_story_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "title": "The Enchanted Forest Journey (Test Mode)",
            "content": f"""In the heart of an ancient forest, young Alex stood at the crossroads of fear and courage. The prompt you gave was: "{request.prompt}"

This is a therapeutic story about overcoming anxiety through magical means. The forest represents the subconscious mind, where fears lurk in the shadows but wisdom waits in the light.

As Alex took the first step forward, the trees seemed to whisper encouragement. "Every journey begins with a single step," they rustled. The path ahead was unclear, but Alex remembered that anxiety often feels overwhelming, yet it's just a feeling - not a fact.

Deeper in the forest, Alex encountered a wise old owl perched on a glowing branch. "Anxiety is like a storm cloud," the owl hooted. "It passes, but the sun always returns." With this wisdom, Alex learned that feelings are temporary visitors.

The journey continued through meadows of wildflowers, each petal representing a moment of peace. Alex collected these petals as reminders that calm exists within the chaos.

Finally, at the forest's heart, Alex found a crystal-clear lake reflecting the sky above. Looking into the water, Alex saw not just their reflection, but their inner strength shining through.

The forest had taught its lesson: anxiety may visit, but it doesn't define us. We are the courageous explorers of our own minds, capable of finding peace even in the wildest storms.

*This is a TEST story generated for development/testing. Configure real API keys to enable AI-powered therapeutic storytelling.*""",
            "outline": {
                "title": "The Enchanted Forest Journey (Test Mode)",
                "genre": "therapeutic_fantasy",
                "main_characters": [
                    {"name": "Alex", "role": "protagonist", "traits": ["anxious", "courageous", "curious"]},
                    {"name": "Wise Owl", "role": "mentor", "traits": ["wise", "compassionate"]}
                ],
                "plot_summary": "A journey through a magical forest teaching anxiety management",
                "key_scenes": [
                    {"scene": "Forest Entrance", "purpose": "Facing initial fears"},
                    {"scene": "Owl Encounter", "purpose": "Learning wisdom"},
                    {"scene": "Crystal Lake", "purpose": "Self-discovery"}
                ],
                "themes": ["anxiety_management", "inner_strength", "mindfulness"]
            },
            "quality_metrics": {
                "overall_score": 8.5,
                "causal_integrity": 0.85,
                "issues": ["Test mode - not analyzed by AI"],
                "suggestions": ["Configure API keys for real AI analysis"]
            },
            "created_at": datetime.now()
        }

        return mock_story

    except Exception as e:
        logger.error(f"Error in test story generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Test story generation failed: {str(e)}")