"""
Scribe Agent: Creative writing and prose generation.

This agent handles the actual writing of story content based on outlines.
Uses Qwen2.5-Instruct model for creative writing.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  # Using OpenAI as proxy for Qwen2.5

logger = logging.getLogger(__name__)

class StoryDraft(BaseModel):
    """Pydantic model for story draft structure."""
    title: str
    content: str
    word_count: int
    scenes: List[Dict[str, Any]]
    writing_style: str
    tone: str

class ScribeAgent:
    """Scribe Agent for creative writing and prose generation."""

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.8):
        """Initialize the Scribe Agent.

        Args:
            model_name: The LLM model to use (default: gpt-4 as proxy for Qwen2.5-Instruct)
            temperature: Creativity level for writing (higher for more creative)
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=4000
        )

    def write_scene(self, outline: Dict[str, Any], scene_index: int,
                   previous_scenes: Optional[List[str]] = None) -> str:
        """Write a single scene based on the outline.

        Args:
            outline: Story outline dictionary
            scene_index: Index of the scene to write
            previous_scenes: Content of previous scenes for continuity

        Returns:
            str: Written scene content
        """
        try:
            key_scenes = outline.get('key_scenes', [])
            if scene_index >= len(key_scenes):
                raise ValueError(f"Scene index {scene_index} out of range")

            scene_info = key_scenes[scene_index]

            system_prompt = """You are a master storyteller and prose writer.

Write engaging, vivid scenes that advance the plot while maintaining character consistency.
Focus on:
- Sensory details and atmosphere
- Character emotions and motivations
- Natural dialogue
- Pacing appropriate to the scene's importance
- Foreshadowing and thematic elements

Write in a style that matches the story's genre and tone."""

            context = f"Previous scenes: {' '.join(previous_scenes[-2:]) if previous_scenes else 'None'}"

            human_prompt = f"""Story Title: {outline.get('title', 'Untitled')}
Genre: {outline.get('genre', 'Unknown')}
Main Characters: {outline.get('main_characters', [])}

Scene {scene_index + 1}: {scene_info}

Context from previous scenes: {context}

Write this scene in 400-800 words. Make it engaging and true to the story's causal relationships."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm
            result = chain.invoke({})
            content = result.content if hasattr(result, 'content') else str(result)

            logger.info(f"Written scene {scene_index + 1} for story: {outline.get('title', 'Untitled')}")

            return content

        except Exception as e:
            logger.error(f"Error writing scene {scene_index}: {str(e)}")
            raise

    def write_draft(self, outline: Dict[str, Any], target_length: str = "short_story") -> StoryDraft:
        """Write a complete story draft based on the outline.

        Args:
            outline: Story outline dictionary
            target_length: Target length ("short_story", "novella", "novel")

        Returns:
            StoryDraft: Complete story draft
        """
        try:
            length_targets = {
                "short_story": 15,  # scenes
                "novella": 30,
                "novel": 60
            }

            target_scenes = length_targets.get(target_length, 15)
            key_scenes = outline.get('key_scenes', [])

            # Limit to available scenes or target
            num_scenes = min(len(key_scenes), target_scenes)

            written_scenes = []
            full_content = []

            for i in range(num_scenes):
                scene_content = self.write_scene(outline, i, full_content)
                written_scenes.append({
                    "scene_number": i + 1,
                    "content": scene_content,
                    "word_count": len(scene_content.split())
                })
                full_content.append(scene_content)

            complete_story = "\n\n".join(full_content)

            draft = StoryDraft(
                title=outline.get('title', 'Untitled Story'),
                content=complete_story,
                word_count=sum(scene['word_count'] for scene in written_scenes),
                scenes=written_scenes,
                writing_style=self._determine_style(outline),
                tone=self._determine_tone(outline)
            )

            logger.info(f"Completed story draft: {draft.title} ({draft.word_count} words)")

            return draft

        except Exception as e:
            logger.error(f"Error writing story draft: {str(e)}")
            raise

    def revise_scene(self, scene_content: str, feedback: str) -> str:
        """Revise a scene based on feedback.

        Args:
            scene_content: Original scene content
            feedback: Revision feedback

        Returns:
            str: Revised scene content
        """
        try:
            system_prompt = """You are an expert editor revising a scene.

Incorporate the feedback while maintaining the scene's core elements.
Improve prose quality, pacing, and emotional impact."""

            human_prompt = f"""Original Scene:
{scene_content}

Feedback: {feedback}

Please revise the scene accordingly."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm
            result = chain.invoke({})
            revised_content = result.content if hasattr(result, 'content') else str(result)

            logger.info("Revised scene based on feedback")

            return revised_content

        except Exception as e:
            logger.error(f"Error revising scene: {str(e)}")
            raise

    def _determine_style(self, outline: Dict[str, Any]) -> str:
        """Determine writing style based on outline."""
        genre = outline.get('genre', '').lower()
        if 'fantasy' in genre:
            return "Epic and descriptive"
        elif 'mystery' in genre:
            return "Suspenseful and atmospheric"
        elif 'romance' in genre:
            return "Intimate and emotional"
        elif 'sci-fi' in genre:
            return "Technical and imaginative"
        else:
            return "Engaging and narrative"

    def _determine_tone(self, outline: Dict[str, Any]) -> str:
        """Determine tone based on outline."""
        themes = outline.get('themes', [])
        if any(word in ' '.join(themes).lower() for word in ['dark', 'horror', 'tragedy']):
            return "Dark and serious"
        elif any(word in ' '.join(themes).lower() for word in ['hope', 'love', 'redemption']):
            return "Hopeful and uplifting"
        elif any(word in ' '.join(themes).lower() for word in ['adventure', 'exploration']):
            return "Exciting and adventurous"
        else:
            return "Balanced and engaging"