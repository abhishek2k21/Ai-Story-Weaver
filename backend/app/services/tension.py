"""
Tension Agent: Game theory-based collaborative orchestration.

This agent manages multi-user collaboration, injects creative conflicts,
and balances contributions using Shapley values.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel
import logging
import numpy as np
from datetime import datetime

# Note: NashPy import would be added when available
# import nashpy

logger = logging.getLogger(__name__)

class CollaborationSession(BaseModel):
    """Represents a multi-user collaboration session."""
    session_id: str
    participants: List[Dict[str, Any]]
    current_conflicts: List[Dict[str, Any]]
    contribution_scores: Dict[str, float]
    game_state: Dict[str, Any]
    created_at: datetime

class CreativeConflict(BaseModel):
    """Represents a creative conflict in the collaboration."""
    conflict_id: str
    type: str  # 'narrative_choice', 'character_development', 'thematic_direction'
    description: str
    options: List[Dict[str, Any]]
    stakes: float  # 0-1, importance level
    resolution_deadline: Optional[datetime] = None
    participants_involved: List[str]

class ContributionMetrics(BaseModel):
    """Metrics for participant contributions."""
    user_id: str
    shapley_value: float
    contribution_quality: float
    collaboration_score: float
    creativity_index: float
    consensus_building: float

class TensionAgent:
    """Tension Agent for managing collaborative storytelling dynamics."""

    def __init__(self, max_participants: int = 6):
        """Initialize the Tension Agent.

        Args:
            max_participants: Maximum participants per session
        """
        self.max_participants = max_participants
        self.active_sessions = {}
        self.conflict_history = []

    def create_session(self, participants: List[Dict[str, Any]]) -> CollaborationSession:
        """Create a new collaboration session.

        Args:
            participants: List of participant information

        Returns:
            CollaborationSession: New session object
        """
        try:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            session = CollaborationSession(
                session_id=session_id,
                participants=participants,
                current_conflicts=[],
                contribution_scores={p["user_id"]: 0.0 for p in participants},
                game_state={
                    "round": 1,
                    "total_conflicts_resolved": 0,
                    "collaboration_efficiency": 1.0
                },
                created_at=datetime.now()
            )

            self.active_sessions[session_id] = session

            logger.info(f"Created collaboration session: {session_id} with {len(participants)} participants")

            return session

        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise

    def inject_creative_conflict(self, session: CollaborationSession,
                               story_context: Dict[str, Any]) -> CreativeConflict:
        """Inject a creative conflict to spark collaboration.

        Args:
            session: Current collaboration session
            story_context: Current story state

        Returns:
            CreativeConflict: New conflict to resolve
        """
        try:
            conflict_types = [
                "narrative_choice",
                "character_development",
                "thematic_direction",
                "pacing_decision",
                "world_building"
            ]

            # Choose conflict type based on story needs
            conflict_type = self._select_optimal_conflict_type(story_context, session)

            # Generate conflict options
            options = self._generate_conflict_options(conflict_type, story_context, session)

            # Calculate stakes
            stakes = self._calculate_conflict_stakes(conflict_type, story_context)

            conflict = CreativeConflict(
                conflict_id=f"conflict_{datetime.now().strftime('%H%M%S')}",
                type=conflict_type,
                description=self._generate_conflict_description(conflict_type, options),
                options=options,
                stakes=stakes,
                resolution_deadline=datetime.now().replace(hour=datetime.now().hour + 1),
                participants_involved=[p["user_id"] for p in session.participants]
            )

            # Add to session
            session.current_conflicts.append(conflict.dict())

            # Store in history
            self.conflict_history.append({
                "conflict": conflict,
                "session_id": session.session_id,
                "injected_at": datetime.now()
            })

            logger.info(f"Injected creative conflict: {conflict.type} in session {session.session_id}")

            return conflict

        except Exception as e:
            logger.error(f"Error injecting conflict: {str(e)}")
            raise

    def resolve_conflict(self, session: CollaborationSession, conflict_id: str,
                        votes: Dict[str, str]) -> Dict[str, Any]:
        """Resolve a creative conflict based on participant votes.

        Args:
            session: Current session
            conflict_id: ID of conflict to resolve
            votes: Dictionary of user_id -> chosen_option_id

        Returns:
            Resolution results
        """
        try:
            # Find the conflict
            conflict_data = None
            for conflict in session.current_conflicts:
                if conflict["conflict_id"] == conflict_id:
                    conflict_data = conflict
                    break

            if not conflict_data:
                raise ValueError(f"Conflict {conflict_id} not found")

            # Analyze voting patterns
            voting_analysis = self._analyze_voting_patterns(votes, session.participants)

            # Determine winning option
            winner = self._determine_conflict_winner(votes, voting_analysis)

            # Update contribution scores
            contribution_updates = self._update_contribution_scores(
                session, votes, winner, voting_analysis
            )

            # Calculate Shapley values
            shapley_values = self._calculate_shapley_values(session, votes)

            # Update session state
            session.game_state["total_conflicts_resolved"] += 1
            session.contribution_scores.update(contribution_updates)

            resolution = {
                "conflict_id": conflict_id,
                "winning_option": winner,
                "voting_analysis": voting_analysis,
                "shapley_values": shapley_values,
                "contribution_updates": contribution_updates,
                "collaboration_quality": voting_analysis["consensus_level"]
            }

            logger.info(f"Resolved conflict {conflict_id} with winner: {winner}")

            return resolution

        except Exception as e:
            logger.error(f"Error resolving conflict: {str(e)}")
            raise

    def calculate_contribution_metrics(self, session: CollaborationSession) -> List[ContributionMetrics]:
        """Calculate comprehensive contribution metrics for all participants.

        Args:
            session: Collaboration session

        Returns:
            List of contribution metrics
        """
        try:
            metrics = []

            for participant in session.participants:
                user_id = participant["user_id"]

                # Calculate various metrics
                shapley_value = session.contribution_scores.get(user_id, 0.0)
                quality_score = self._assess_contribution_quality(session, user_id)
                collaboration_score = self._assess_collaboration_score(session, user_id)
                creativity_index = self._calculate_creativity_index(session, user_id)
                consensus_score = self._calculate_consensus_building(session, user_id)

                metric = ContributionMetrics(
                    user_id=user_id,
                    shapley_value=shapley_value,
                    contribution_quality=quality_score,
                    collaboration_score=collaboration_score,
                    creativity_index=creativity_index,
                    consensus_building=consensus_score
                )

                metrics.append(metric)

            logger.info(f"Calculated contribution metrics for {len(metrics)} participants")

            return metrics

        except Exception as e:
            logger.error(f"Error calculating contribution metrics: {str(e)}")
            raise

    def optimize_collaboration(self, session: CollaborationSession) -> Dict[str, Any]:
        """Optimize collaboration dynamics using game theory.

        Args:
            session: Current session

        Returns:
            Optimization recommendations
        """
        try:
            # Analyze current collaboration state
            collaboration_state = self._analyze_collaboration_state(session)

            # Identify optimization opportunities
            optimizations = {
                "role_assignments": self._optimize_role_assignments(session),
                "conflict_frequency": self._optimize_conflict_frequency(collaboration_state),
                "participant_balance": self._balance_participant_contributions(session),
                "creativity_boosters": self._identify_creativity_boosters(session)
            }

            logger.info(f"Generated collaboration optimizations for session {session.session_id}")

            return optimizations

        except Exception as e:
            logger.error(f"Error optimizing collaboration: {str(e)}")
            raise

    def _select_optimal_conflict_type(self, story_context: Dict[str, Any],
                                    session: CollaborationSession) -> str:
        """Select the most beneficial conflict type for current story state."""
        # Analyze story needs and participant dynamics
        story_phase = story_context.get("phase", "development")

        if story_phase == "setup":
            return "character_development"
        elif story_phase == "rising_action":
            return "narrative_choice"
        elif story_phase == "climax":
            return "thematic_direction"
        else:
            return "pacing_decision"

    def _generate_conflict_options(self, conflict_type: str, story_context: Dict[str, Any],
                                 session: CollaborationSession) -> List[Dict[str, Any]]:
        """Generate options for a creative conflict."""
        options = []

        if conflict_type == "narrative_choice":
            options = [
                {"id": "option_1", "description": "Take the high-risk path", "risk_level": 0.8},
                {"id": "option_2", "description": "Choose the safe route", "risk_level": 0.3},
                {"id": "option_3", "description": "Find a creative compromise", "risk_level": 0.5}
            ]
        elif conflict_type == "character_development":
            options = [
                {"id": "option_1", "description": "Make character more complex", "depth": 0.9},
                {"id": "option_2", "description": "Keep character straightforward", "depth": 0.4},
                {"id": "option_3", "description": "Add mysterious background", "depth": 0.7}
            ]

        return options

    def _calculate_conflict_stakes(self, conflict_type: str, story_context: Dict[str, Any]) -> float:
        """Calculate the importance stakes of a conflict."""
        base_stakes = {
            "narrative_choice": 0.7,
            "character_development": 0.8,
            "thematic_direction": 0.9,
            "pacing_decision": 0.5,
            "world_building": 0.6
        }

        return base_stakes.get(conflict_type, 0.5)

    def _generate_conflict_description(self, conflict_type: str, options: List[Dict[str, Any]]) -> str:
        """Generate a compelling conflict description."""
        descriptions = {
            "narrative_choice": f"At this critical junction, the story could go in {len(options)} different directions. Which path should we take?",
            "character_development": f"Our protagonist's development hangs in the balance. How should we shape their growth?",
            "thematic_direction": f"The story's core message needs clarification. What themes should we emphasize?"
        }

        return descriptions.get(conflict_type, "A creative decision needs to be made.")

    def _analyze_voting_patterns(self, votes: Dict[str, str],
                               participants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze voting patterns and consensus levels."""
        total_votes = len(votes)
        vote_counts = {}

        for vote in votes.values():
            vote_counts[vote] = vote_counts.get(vote, 0) + 1

        # Calculate consensus
        max_votes = max(vote_counts.values())
        consensus_level = max_votes / total_votes if total_votes > 0 else 0

        # Identify voting blocs
        blocs = len([count for count in vote_counts.values() if count > 1])

        return {
            "total_votes": total_votes,
            "vote_distribution": vote_counts,
            "consensus_level": consensus_level,
            "voting_blocs": blocs,
            "participation_rate": total_votes / len(participants)
        }

    def _determine_conflict_winner(self, votes: Dict[str, str],
                                 voting_analysis: Dict[str, Any]) -> str:
        """Determine the winning option from votes."""
        vote_counts = voting_analysis["vote_distribution"]
        return max(vote_counts.keys(), key=lambda x: vote_counts[x])

    def _update_contribution_scores(self, session: CollaborationSession,
                                  votes: Dict[str, str], winner: str,
                                  voting_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Update participant contribution scores."""
        updates = {}

        for participant in session.participants:
            user_id = participant["user_id"]
            if user_id in votes:
                # Reward voting for winning option
                if votes[user_id] == winner:
                    updates[user_id] = session.contribution_scores.get(user_id, 0) + 0.1
                else:
                    updates[user_id] = session.contribution_scores.get(user_id, 0) + 0.05

        return updates

    def _calculate_shapley_values(self, session: CollaborationSession,
                                votes: Dict[str, str]) -> Dict[str, float]:
        """Calculate Shapley values for fair contribution assessment."""
        # Simplified Shapley value calculation
        shapley_values = {}

        for participant in session.participants:
            user_id = participant["user_id"]
            # Base value from voting participation
            base_value = 1.0 if user_id in votes else 0.0
            # Bonus for consensus building
            consensus_bonus = 0.2 if votes.get(user_id) else 0.0

            shapley_values[user_id] = base_value + consensus_bonus

        return shapley_values

    def _assess_contribution_quality(self, session: CollaborationSession, user_id: str) -> float:
        """Assess the quality of a user's contributions."""
        # Placeholder - would analyze contribution history
        return 0.75

    def _assess_collaboration_score(self, session: CollaborationSession, user_id: str) -> float:
        """Assess how well a user collaborates."""
        # Placeholder - would analyze interaction patterns
        return 0.8

    def _calculate_creativity_index(self, session: CollaborationSession, user_id: str) -> float:
        """Calculate creativity index for a user."""
        # Placeholder - would analyze creative contributions
        return 0.7

    def _calculate_consensus_building(self, session: CollaborationSession, user_id: str) -> float:
        """Calculate consensus building ability."""
        # Placeholder - would analyze voting and discussion patterns
        return 0.6

    def _analyze_collaboration_state(self, session: CollaborationSession) -> Dict[str, Any]:
        """Analyze the current state of collaboration."""
        return {
            "efficiency": session.game_state.get("collaboration_efficiency", 1.0),
            "conflicts_resolved": session.game_state.get("total_conflicts_resolved", 0),
            "participant_balance": len(session.participants)
        }

    def _optimize_role_assignments(self, session: CollaborationSession) -> Dict[str, str]:
        """Optimize role assignments for better collaboration."""
        roles = ["Plot Driver", "Emotional Weaver", "Conflict Architect", "World Builder"]
        assignments = {}

        for i, participant in enumerate(session.participants):
            assignments[participant["user_id"]] = roles[i % len(roles)]

        return assignments

    def _optimize_conflict_frequency(self, collaboration_state: Dict[str, Any]) -> str:
        """Determine optimal conflict injection frequency."""
        efficiency = collaboration_state.get("efficiency", 1.0)

        if efficiency > 0.8:
            return "increase_frequency"
        elif efficiency < 0.5:
            return "decrease_frequency"
        else:
            return "maintain_frequency"

    def _balance_participant_contributions(self, session: CollaborationSession) -> List[str]:
        """Generate recommendations to balance contributions."""
        scores = session.contribution_scores
        avg_score = np.mean(list(scores.values()))

        recommendations = []
        for user_id, score in scores.items():
            if score < avg_score * 0.8:
                recommendations.append(f"Encourage more participation from {user_id}")
            elif score > avg_score * 1.2:
                recommendations.append(f"Balance contributions - {user_id} is dominating")

        return recommendations

    def _identify_creativity_boosters(self, session: CollaborationSession) -> List[str]:
        """Identify ways to boost creativity in the session."""
        return [
            "Introduce time constraints for decisions",
            "Add random creative prompts",
            "Rotate role assignments",
            "Encourage wild card ideas"
        ]