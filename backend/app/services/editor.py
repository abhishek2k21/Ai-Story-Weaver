"""
Editor Agent: Self-correction loops with quality assessment.

This agent reviews and improves story drafts using RLHF-tuned models.
Integrates with Vault for ethical checks.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI  # Using OpenAI as proxy for Llama-3.1
import re

logger = logging.getLogger(__name__)

class QualityMetrics(BaseModel):
    """Quality assessment metrics for story evaluation."""
    coherence_score: float  # 0-1, how well the story hangs together
    engagement_score: float  # 0-1, how engaging the narrative is
    character_consistency: float  # 0-1, character development consistency
    pacing_score: float  # 0-1, appropriate pacing
    language_quality: float  # 0-1, prose quality
    causal_integrity: float  # 0-1, how well causality is maintained
    overall_score: float  # 0-1, weighted average
    issues_found: List[str]  # List of identified problems
    suggestions: List[str]  # Improvement suggestions

class EditorAgent:
    """Editor Agent for story review and self-correction."""

    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.3):
        """Initialize the Editor Agent.

        Args:
            model_name: The LLM model to use (default: gpt-4 as proxy for Llama-3.1)
            temperature: Low temperature for consistent evaluation
        """
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=2000
        )
        self.quality_threshold = 0.85  # Minimum quality score to pass

    def evaluate_draft(self, draft_content: str, outline: Dict[str, Any]) -> QualityMetrics:
        """Evaluate the quality of a story draft.

        Args:
            draft_content: The story draft text
            outline: Original story outline for comparison

        Returns:
            QualityMetrics: Detailed quality assessment
        """
        try:
            system_prompt = """You are an expert literary editor and story analyst.

Evaluate the story draft on multiple criteria:
- Coherence: How well the plot hangs together
- Engagement: Reader interest and emotional investment
- Character Consistency: Believable character development
- Pacing: Appropriate rhythm and tension
- Language Quality: Prose style and clarity
- Causal Integrity: Logical consequence of choices

Provide scores from 0-1 and identify specific issues with suggestions for improvement.

Output as JSON with the following structure:
{
    "coherence_score": float,
    "engagement_score": float,
    "character_consistency": float,
    "pacing_score": float,
    "language_quality": float,
    "causal_integrity": float,
    "overall_score": float,
    "issues_found": ["issue1", "issue2"],
    "suggestions": ["suggestion1", "suggestion2"]
}"""

            human_prompt = f"""Story Outline: {outline}

Draft Content: {draft_content[:2000]}...  # Truncated for token limits

Evaluate this story draft comprehensively."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm

            result = chain.invoke({})
            content = result.content if hasattr(result, 'content') else str(result)

            # Parse JSON response
            import json
            metrics_dict = json.loads(content)

            metrics = QualityMetrics(**metrics_dict)

            logger.info(f"Evaluated draft quality: {metrics.overall_score:.2f}")

            return metrics

        except Exception as e:
            logger.error(f"Error evaluating draft: {str(e)}")
            # Return default metrics on error
            return QualityMetrics(
                coherence_score=0.5,
                engagement_score=0.5,
                character_consistency=0.5,
                pacing_score=0.5,
                language_quality=0.5,
                causal_integrity=0.5,
                overall_score=0.5,
                issues_found=["Evaluation failed"],
                suggestions=["Manual review required"]
            )

    def revise_draft(self, draft_content: str, metrics: QualityMetrics) -> str:
        """Revise the draft based on quality metrics.

        Args:
            draft_content: Original draft content
            metrics: Quality assessment results

        Returns:
            str: Revised draft content
        """
        try:
            issues_text = "\n".join(f"- {issue}" for issue in metrics.issues_found)
            suggestions_text = "\n".join(f"- {sugg}" for sugg in metrics.suggestions)

            system_prompt = """You are an expert editor revising a story draft.

Address the identified issues and implement the suggestions while maintaining
the story's core elements and voice. Focus on improving the weakest areas
identified in the quality assessment."""

            human_prompt = f"""Original Draft: {draft_content[:3000]}...

Quality Issues Identified:
{issues_text}

Suggested Improvements:
{suggestions_text}

Please revise the draft accordingly. Maintain the story's length and core plot."""

            prompt_template = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", human_prompt)
            ])

            chain = prompt_template | self.llm
            result = chain.invoke({})
            revised_content = result.content if hasattr(result, 'content') else str(result)

            logger.info("Revised draft based on quality metrics")

            return revised_content

        except Exception as e:
            logger.error(f"Error revising draft: {str(e)}")
            return draft_content  # Return original on error

    def iterative_improvement(self, draft_content: str, outline: Dict[str, Any],
                            max_iterations: int = 3) -> Tuple[str, QualityMetrics]:
        """Perform iterative improvement until quality threshold is met.

        Args:
            draft_content: Initial draft content
            outline: Story outline
            max_iterations: Maximum number of revision cycles

        Returns:
            Tuple of (final_content, final_metrics)
        """
        current_content = draft_content

        for iteration in range(max_iterations):
            logger.info(f"Starting iteration {iteration + 1}/{max_iterations}")

            # Evaluate current draft
            metrics = self.evaluate_draft(current_content, outline)

            logger.info(f"Iteration {iteration + 1} score: {metrics.overall_score:.2f}")

            # Check if quality threshold met
            if metrics.overall_score >= self.quality_threshold:
                logger.info(f"Quality threshold met after {iteration + 1} iterations")
                break

            # Revise based on metrics
            current_content = self.revise_draft(current_content, metrics)

        # Final evaluation
        final_metrics = self.evaluate_draft(current_content, outline)

        return current_content, final_metrics

    def check_ethical_compliance(self, content: str) -> Dict[str, Any]:
        """Check for ethical issues in the content (integrates with Vault).

        Args:
            content: Story content to check

        Returns:
            Dict with ethical assessment
        """
        try:
            # This would integrate with the Vault agent
            # For now, basic checks
            ethical_issues = []

            # Check for potentially harmful content patterns
            harmful_patterns = [
                r'\b(kill|murder|death)\b.*\b(child|kid|children)\b',
                r'\b(rape|sexual assault)\b',
                r'\b(self-harm|suicide)\b.*\b(method|how)\b'
            ]

            for pattern in harmful_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    ethical_issues.append(f"Potentially harmful content detected: {pattern}")

            return {
                "compliant": len(ethical_issues) == 0,
                "issues": ethical_issues,
                "recommendations": ["Review content for sensitive themes"] if ethical_issues else []
            }

        except Exception as e:
            logger.error(f"Error in ethical check: {str(e)}")
            return {"compliant": False, "issues": ["Ethical check failed"], "recommendations": []}