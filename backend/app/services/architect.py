"""
Architect Agent: Goal-oriented planning with causality integration.

This agent handles story planning and outline generation with causal chains.
Uses DeepSeek-V3 model for planning, integrates with causality engine.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI  # Using OpenAI as proxy for DeepSeek
import logging

logger = logging.getLogger(__name__)

class StoryOutline(BaseModel):
    """Pydantic model for story outline structure."""
    title: str
    genre: str
    main_characters: List[Dict[str, str]]
    plot_summary: str
    key_scenes: List[Dict[str, Any]]
    causal_chains: List[Dict[str, Any]]
    themes: List[str]
    estimated_length: str

class ArchitectAgent:
    """Architect Agent for story planning and causal outline generation."""

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        """Initialize the Architect Agent.

        Args:
            model_name: The LLM model to use (default: gpt-4 as proxy for DeepSeek-V3)
            temperature: Creativity level for generation
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=2000
        )
        self.output_parser = JsonOutputParser(pydantic_object=StoryOutline)

    def plan_story(self, prompt: str, story_bible: Optional[Dict] = None) -> StoryOutline:
        """Generate a story outline with causal chains.

        Args:
            prompt: User prompt describing the desired story
            story_bible: Existing story context/bible (optional)

        Returns:
            StoryOutline: Structured story plan with causal relationships
        """
        try:
            # Create the planning prompt
            system_prompt = """You are an expert story architect specializing in narrative design with causal relationships.

Your task is to create a detailed story outline that includes:
1. A compelling title and genre
2. Main characters with motivations and backstories
3. Plot summary (2-3 paragraphs)
4. Key scenes (aim for 15-scene horizon as mentioned)
5. Causal chains showing how choices ripple through the story
6. Central themes
7. Estimated length

For causal chains, identify:
- Trigger events
- Character choices/decisions
- Immediate consequences
- Long-term ripple effects
- Alternative paths that could have occurred

Ensure the story has meaningful choices that create butterfly effects.

Output must be valid JSON matching the StoryOutline schema."""

            human_prompt = f"""Create a story outline for this prompt: {prompt}

{f'Story Bible Context: {json.dumps(story_bible)}' if story_bible else ''}

Generate a comprehensive outline with causal relationships."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            # Create the chain
            chain = prompt_template | self.llm | self.output_parser

            # Generate the outline
            result = chain.invoke({})

            logger.info(f"Generated story outline for prompt: {prompt[:50]}...")

            return StoryOutline(**result)

        except Exception as e:
            logger.error(f"Error in story planning: {str(e)}")
            raise

    def refine_outline(self, outline: StoryOutline, feedback: str) -> StoryOutline:
        """Refine an existing outline based on feedback.

        Args:
            outline: Current story outline
            feedback: User feedback for refinement

        Returns:
            StoryOutline: Refined outline
        """
        try:
            system_prompt = """You are a story architect refining an outline based on feedback.

Maintain the JSON structure while incorporating the feedback.
Focus on improving causal relationships and narrative coherence."""

            human_prompt = f"""Original Outline: {outline.json()}

Feedback: {feedback}

Refine the outline accordingly."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm | self.output_parser
            result = chain.invoke({})

            logger.info("Refined story outline based on feedback")

            return StoryOutline(**result)

        except Exception as e:
            logger.error(f"Error in outline refinement: {str(e)}")
            raise

    def simulate_causal_horizon(self, outline: StoryOutline, choice_point: str) -> Dict[str, Any]:
        """Simulate causal effects of a choice within the 15-scene horizon.

        Args:
            outline: Current story outline
            choice_point: Description of the choice to simulate

        Returns:
            Dict containing causal simulation results
        """
        try:
            system_prompt = """You are a causal reasoning expert.

Given a story outline and a choice point, simulate the causal ripple effects
within a 15-scene horizon. Consider:
- Immediate consequences
- Character reactions
- Plot developments
- Theme reinforcement
- Alternative outcomes

Provide detailed causal analysis."""

            human_prompt = f"""Story Outline: {outline.json()}

Choice Point: {choice_point}

Simulate the causal effects within 15 scenes."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm

            result = chain.invoke({})
            content = result.content if hasattr(result, 'content') else str(result)

            logger.info(f"Simulated causal horizon for choice: {choice_point[:30]}...")

            return {
                "choice_point": choice_point,
                "causal_analysis": content,
                "simulation_timestamp": "2026-01-15T12:00:00Z"  # Current date
            }

        except Exception as e:
            logger.error(f"Error in causal simulation: {str(e)}")
            raise