"""
End-to-end integration tests for AI Story Weaver Pro.
Tests complete user workflows from registration to story completion.
"""
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import create_tables, drop_tables
from app.core.config import settings


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""

    def setup_method(self):
        """Setup test database."""
        create_tables()

    def teardown_method(self):
        """Clean up test database."""
        drop_tables()

    @pytest.fixture
    def client(self):
        """Test client fixture."""
        return TestClient(app)

    def test_complete_user_story_workflow(self, client):
        """Test complete workflow: register -> login -> create story -> generate content -> complete."""
        # Step 1: User Registration
        user_data = {
            "email": "therapist@example.com",
            "username": "therapist",
            "password": "securepass123",
            "full_name": "Dr. Sarah Johnson"
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

        # Step 2: User Login
        login_data = {
            "username": "therapist",
            "password": "securepass123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200

        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Step 3: Verify User Profile
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        user_profile = response.json()
        assert user_profile["username"] == "therapist"
        assert user_profile["email"] == "therapist@example.com"

        # Step 4: Create Story
        story_data = {
            "title": "The Courage Within",
            "description": "A therapeutic story about overcoming anxiety through courage and friendship",
            "genre": "fantasy",
            "themes": ["courage", "friendship", "self-discovery"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["anxiety_management", "self_esteem", "social_confidence"],
            "user_preferences": {
                "tone": "hopeful",
                "pacing": "moderate",
                "character_types": ["relatable_hero", "supportive_friend", "wise_mentor"],
                "setting": "magical_forest",
                "conflict_style": "internal_struggle"
            }
        }

        response = client.post("/api/v1/stories/", json=story_data, headers=headers)
        assert response.status_code == 201

        story = response.json()
        story_id = story["id"]
        assert story["title"] == "The Courage Within"
        assert story["status"] == "draft"
        assert story["genre"] == "fantasy"

        # Step 5: Generate Story Content (Introduction)
        generate_data = {
            "scene_type": "introduction",
            "parameters": {
                "tone": "gentle",
                "focus": "character_introduction",
                "therapeutic_elements": ["comfort", "curiosity"]
            }
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/generate",
            json=generate_data,
            headers=headers
        )
        assert response.status_code == 200

        content_response = response.json()
        assert "content" in content_response
        assert content_response["scene_type"] == "introduction"
        assert isinstance(content_response["content"], str)
        assert len(content_response["content"]) > 100  # Substantial content

        # Step 6: Generate Additional Scenes
        scenes_to_generate = ["rising_action", "climax", "resolution"]

        for scene_type in scenes_to_generate:
            scene_data = {
                "scene_type": scene_type,
                "parameters": {
                    "tone": "hopeful" if scene_type != "climax" else "intense",
                    "focus": "emotional_development",
                    "therapeutic_elements": ["growth", "resolution"]
                }
            }

            response = client.post(
                f"/api/v1/stories/{story_id}/generate",
                json=scene_data,
                headers=headers
            )
            assert response.status_code == 200

            scene_content = response.json()
            assert scene_content["scene_type"] == scene_type
            assert len(scene_content["content"]) > 50

        # Step 7: Get Story Analytics
        response = client.get(f"/api/v1/stories/{story_id}/analytics", headers=headers)
        assert response.status_code == 200

        analytics = response.json()
        assert "emotional_resonance" in analytics
        assert "engagement_score" in analytics
        assert "therapeutic_alignment" in analytics
        assert isinstance(analytics["emotional_resonance"], (int, float))
        assert isinstance(analytics["engagement_score"], (int, float))

        # Step 8: Update Story Status to Completed
        update_data = {
            "status": "completed",
            "content": {
                "scenes": ["introduction", "rising_action", "climax", "resolution"],
                "final_narrative": "Complete story content...",
                "therapeutic_summary": "Story successfully addresses anxiety management goals"
            }
        }

        response = client.put(f"/api/v1/stories/{story_id}", json=update_data, headers=headers)
        assert response.status_code == 200

        updated_story = response.json()
        assert updated_story["status"] == "completed"
        assert "content" in updated_story

        # Step 9: List User's Stories
        response = client.get("/api/v1/stories/", headers=headers)
        assert response.status_code == 200

        stories = response.json()
        assert isinstance(stories, list)
        assert len(stories) >= 1

        # Find our completed story
        completed_story = next((s for s in stories if s["id"] == story_id), None)
        assert completed_story is not None
        assert completed_story["title"] == "The Courage Within"
        assert completed_story["status"] == "completed"

        # Step 10: Export Story
        export_data = {
            "format": "pdf",
            "include_analytics": True,
            "include_metadata": True
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/export",
            json=export_data,
            headers=headers
        )
        assert response.status_code == 200

        export_result = response.json()
        assert "export_url" in export_result
        assert export_result["format"] == "pdf"

    def test_collaborative_story_workflow(self, client):
        """Test collaborative story creation with multiple users."""
        # Create first user (therapist)
        therapist_data = {
            "email": "therapist1@example.com",
            "username": "therapist1",
            "password": "pass123",
            "full_name": "Dr. Smith"
        }
        client.post("/api/v1/auth/register", json=therapist_data)

        therapist_login = client.post("/api/v1/auth/login", json={
            "username": "therapist1",
            "password": "pass123"
        })
        therapist_token = therapist_login.json()["access_token"]
        therapist_headers = {"Authorization": f"Bearer {therapist_token}"}

        # Create second user (co-therapist)
        cotherapist_data = {
            "email": "cotherapist@example.com",
            "username": "cotherapist",
            "password": "pass123",
            "full_name": "Dr. Jones"
        }
        client.post("/api/v1/auth/register", json=cotherapist_data)

        cotherapist_login = client.post("/api/v1/auth/login", json={
            "username": "cotherapist",
            "password": "pass123"
        })
        cotherapist_token = cotherapist_login.json()["access_token"]
        cotherapist_headers = {"Authorization": f"Bearer {cotherapist_token}"}

        # Therapist creates collaborative story
        story_data = {
            "title": "Team Healing Journey",
            "description": "Collaborative therapeutic story",
            "genre": "adventure",
            "themes": ["teamwork", "healing"],
            "target_audience": "adult",
            "length_preference": "long",
            "therapeutic_goals": ["team_building", "emotional_support"],
            "collaboration_settings": {
                "allow_contributors": True,
                "max_contributors": 3,
                "review_required": True
            }
        }

        response = client.post("/api/v1/stories/", json=story_data, headers=therapist_headers)
        assert response.status_code == 201
        story = response.json()
        story_id = story["id"]

        # Co-therapist joins collaboration
        collab_data = {
            "story_id": story_id,
            "role": "contributor",
            "permissions": ["generate_content", "review_content"]
        }

        response = client.post(
            "/api/v1/stories/collaborate/join",
            json=collab_data,
            headers=cotherapist_headers
        )
        assert response.status_code == 200

        # Start collaboration session
        session_data = {
            "session_type": "brainstorming",
            "participants": ["therapist1", "cotherapist"],
            "parameters": {
                "focus": "character_development",
                "time_limit": 45,
                "goal": "develop_supportive_character_relationships"
            }
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/collaborate",
            json=session_data,
            headers=therapist_headers
        )
        assert response.status_code == 200

        collab_session = response.json()
        assert "session_id" in collab_session
        assert len(collab_session["participants"]) == 2

        # Both users generate content
        for user_headers, user_name in [(therapist_headers, "therapist"), (cotherapist_headers, "cotherapist")]:
            generate_data = {
                "scene_type": f"{user_name}_scene",
                "parameters": {
                    "tone": "supportive",
                    "focus": "relationship_building",
                    "contribution_type": "collaborative"
                }
            }

            response = client.post(
                f"/api/v1/stories/{story_id}/generate",
                json=generate_data,
                headers=user_headers
            )
            assert response.status_code == 200

        # Review and merge contributions
        review_data = {
            "contributions": ["therapist_scene", "cotherapist_scene"],
            "merge_strategy": "integrate",
            "review_criteria": ["therapeutic_alignment", "narrative_flow"]
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/collaborate/review",
            json=review_data,
            headers=therapist_headers
        )
        assert response.status_code == 200

        review_result = response.json()
        assert "merged_content" in review_result
        assert "review_score" in review_result

    def test_therapeutic_story_customization(self, client):
        """Test story customization for specific therapeutic needs."""
        # Register user with specific therapeutic focus
        user_data = {
            "email": "specialist@example.com",
            "username": "specialist",
            "password": "pass123",
            "full_name": "Therapeutic Specialist",
            "specializations": ["anxiety", "depression", "trauma"]
        }
        client.post("/api/v1/auth/register", json=user_data)

        login_response = client.post("/api/v1/auth/login", json={
            "username": "specialist",
            "password": "pass123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create highly customized therapeutic story
        therapeutic_story = {
            "title": "Finding Inner Peace",
            "description": "Personalized anxiety management story",
            "genre": "contemporary_realism",
            "themes": ["mindfulness", "acceptance", "resilience"],
            "target_audience": "adult",
            "length_preference": "medium",
            "therapeutic_goals": ["anxiety_reduction", "mindfulness_practice", "emotional_regulation"],
            "therapeutic_parameters": {
                "anxiety_triggers_to_address": ["social_anxiety", "performance_anxiety"],
                "coping_strategies": ["deep_breathing", "positive_self_talk", "gradual_exposure"],
                "character_archetypes": ["anxious_hero", "calm_mentor", "supportive_friend"],
                "narrative_techniques": ["metaphorical_journey", "internal_monologue", "reflective_pauses"]
            },
            "customization_settings": {
                "adaptability": "high",
                "user_feedback_integration": True,
                "progress_tracking": True,
                "follow_up_suggestions": True
            }
        }

        response = client.post("/api/v1/stories/", json=therapeutic_story, headers=headers)
        assert response.status_code == 201
        story = response.json()

        # Generate personalized content
        personalized_scenes = [
            {"type": "anxiety_introduction", "focus": "relatable_struggle"},
            {"type": "coping_strategy_introduction", "focus": "breathing_exercise"},
            {"type": "support_system_building", "focus": "friendship_development"},
            {"type": "gradual_progress", "focus": "small_victories"},
            {"type": "integration_reflection", "focus": "personal_growth"}
        ]

        generated_content = []
        for scene in personalized_scenes:
            generate_data = {
                "scene_type": scene["type"],
                "parameters": {
                    "therapeutic_focus": scene["focus"],
                    "personalization_level": "high",
                    "user_adaptations": ["anxiety_specific", "coping_oriented"]
                }
            }

            response = client.post(
                f"/api/v1/stories/{story['id']}/generate",
                json=generate_data,
                headers=headers
            )
            assert response.status_code == 200
            generated_content.append(response.json())

        assert len(generated_content) == 5

        # Test therapeutic alignment analysis
        response = client.get(f"/api/v1/stories/{story['id']}/therapeutic-analysis", headers=headers)
        assert response.status_code == 200

        analysis = response.json()
        assert "anxiety_alignment_score" in analysis
        assert "coping_strategy_coverage" in analysis
        assert "personalization_effectiveness" in analysis
        assert analysis["anxiety_alignment_score"] >= 0.8  # High therapeutic alignment

    def test_story_iteration_and_refinement(self, client):
        """Test iterative story development and refinement."""
        # Register user
        user_data = {
            "email": "writer@example.com",
            "username": "writer",
            "password": "pass123",
            "full_name": "Creative Writer"
        }
        client.post("/api/v1/auth/register", json=user_data)

        login_response = client.post("/api/v1/auth/login", json={
            "username": "writer",
            "password": "pass123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create initial story
        story_data = {
            "title": "Iterative Tale",
            "description": "Story developed through iterations",
            "genre": "fantasy",
            "themes": ["growth", "discovery"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["self_discovery"]
        }

        response = client.post("/api/v1/stories/", json=story_data, headers=headers)
        story = response.json()
        story_id = story["id"]

        # Generate initial version
        initial_content = []
        for scene_type in ["introduction", "development", "climax"]:
            generate_data = {
                "scene_type": scene_type,
                "parameters": {"version": "initial"}
            }

            response = client.post(
                f"/api/v1/stories/{story_id}/generate",
                json=generate_data,
                headers=headers
            )
            initial_content.append(response.json()["content"])

        # Get feedback and iterate
        feedback_data = {
            "feedback_type": "user_input",
            "comments": "Make the character more relatable and increase emotional depth",
            "ratings": {
                "emotional_engagement": 6,
                "character_relatable": 5,
                "pacing": 7
            }
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/feedback",
            json=feedback_data,
            headers=headers
        )
        assert response.status_code == 200

        # Generate improved version based on feedback
        for scene_type in ["introduction", "development", "climax"]:
            generate_data = {
                "scene_type": scene_type,
                "parameters": {
                    "version": "improved",
                    "incorporate_feedback": True,
                    "focus_improvements": ["character_depth", "emotional_resonance"]
                }
            }

            response = client.post(
                f"/api/v1/stories/{story_id}/generate",
                json=generate_data,
                headers=headers
            )
            assert response.status_code == 200

        # Compare versions
        response = client.get(f"/api/v1/stories/{story_id}/versions", headers=headers)
        assert response.status_code == 200

        versions = response.json()
        assert len(versions) >= 2  # Initial and improved versions

        # Finalize story
        finalize_data = {
            "selected_version": "improved",
            "final_edits": "Minor polishing for clarity",
            "status": "completed"
        }

        response = client.put(f"/api/v1/stories/{story_id}", json=finalize_data, headers=headers)
        assert response.status_code == 200

        final_story = response.json()
        assert final_story["status"] == "completed"