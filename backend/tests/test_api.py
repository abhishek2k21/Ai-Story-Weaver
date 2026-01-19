"""
API integration tests for AI Story Weaver Pro.
Tests FastAPI endpoints and request/response handling.
"""
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.db.base import get_db, create_tables, drop_tables
from app.db.models import User, Story
from app.core.security import create_access_token


class TestAPIIntegration:
    """Test API endpoints integration."""

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

    @pytest.fixture
    def auth_headers(self, client):
        """Authentication headers fixture."""
        # Create test user
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User"
        }

        # Register user
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        # Login to get token
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200

        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_user_registration(self, client):
        """Test user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User"
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_user_login(self, client):
        """Test user login."""
        # First register user
        user_data = {
            "email": "loginuser@example.com",
            "username": "loginuser",
            "password": "password123",
            "full_name": "Login User"
        }
        client.post("/api/v1/auth/register", json=user_data)

        # Then login
        login_data = {
            "username": "loginuser",
            "password": "password123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "token_type" in data

    def test_get_current_user(self, client, auth_headers):
        """Test get current user endpoint."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["full_name"] == "Test User"

    def test_create_story(self, client, auth_headers):
        """Test story creation."""
        story_data = {
            "title": "Test Story",
            "description": "A test story for integration testing",
            "genre": "fantasy",
            "themes": ["adventure", "friendship"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["anxiety_management"],
            "user_preferences": {
                "tone": "hopeful",
                "pacing": "moderate"
            }
        }

        response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == "Test Story"
        assert data["genre"] == "fantasy"
        assert data["status"] == "draft"
        assert "id" in data

    def test_get_stories(self, client, auth_headers):
        """Test get user stories."""
        # Create a story first
        story_data = {
            "title": "My Test Story",
            "description": "Another test story",
            "genre": "drama",
            "themes": ["growth"],
            "target_audience": "adult",
            "length_preference": "short",
            "therapeutic_goals": ["self_esteem"]
        }
        client.post("/api/v1/stories/", json=story_data, headers=auth_headers)

        # Get stories
        response = client.get("/api/v1/stories/", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Check the created story
        story = next((s for s in data if s["title"] == "My Test Story"), None)
        assert story is not None
        assert story["genre"] == "drama"
        assert story["status"] == "draft"

    def test_get_story_by_id(self, client, auth_headers):
        """Test get specific story by ID."""
        # Create a story first
        story_data = {
            "title": "Specific Story",
            "description": "Story for ID testing",
            "genre": "mystery",
            "themes": ["suspense"],
            "target_audience": "adult",
            "length_preference": "medium",
            "therapeutic_goals": ["stress_relief"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Get the story by ID
        response = client.get(f"/api/v1/stories/{story_id}", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == story_id
        assert data["title"] == "Specific Story"
        assert data["genre"] == "mystery"

    def test_update_story(self, client, auth_headers):
        """Test story update."""
        # Create a story first
        story_data = {
            "title": "Original Title",
            "description": "Original description",
            "genre": "fantasy",
            "themes": ["magic"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["confidence_building"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Update the story
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "in_progress"
        }
        response = client.put(f"/api/v1/stories/{story_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["status"] == "in_progress"

    def test_delete_story(self, client, auth_headers):
        """Test story deletion."""
        # Create a story first
        story_data = {
            "title": "Story to Delete",
            "description": "This story will be deleted",
            "genre": "horror",
            "themes": ["fear"],
            "target_audience": "adult",
            "length_preference": "short",
            "therapeutic_goals": ["fear_management"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Delete the story
        response = client.delete(f"/api/v1/stories/{story_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify story is deleted
        get_response = client.get(f"/api/v1/stories/{story_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_generate_story_content(self, client, auth_headers):
        """Test story content generation."""
        # Create a story first
        story_data = {
            "title": "AI Generated Story",
            "description": "Story with AI-generated content",
            "genre": "science_fiction",
            "themes": ["exploration", "discovery"],
            "target_audience": "young_adult",
            "length_preference": "medium",
            "therapeutic_goals": ["curiosity_stimulation"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Generate content
        generate_data = {
            "scene_type": "introduction",
            "parameters": {
                "tone": "exciting",
                "focus": "character_introduction"
            }
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/generate",
            json=generate_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert "content" in data
        assert "scene_type" in data
        assert data["scene_type"] == "introduction"
        assert isinstance(data["content"], str)
        assert len(data["content"]) > 0

    def test_story_analytics(self, client, auth_headers):
        """Test story analytics endpoint."""
        # Create a story first
        story_data = {
            "title": "Analytics Test Story",
            "description": "Story for analytics testing",
            "genre": "drama",
            "themes": ["relationships"],
            "target_audience": "adult",
            "length_preference": "medium",
            "therapeutic_goals": ["emotional_intelligence"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Get analytics
        response = client.get(f"/api/v1/stories/{story_id}/analytics", headers=auth_headers)
        assert response.status_code == 200

        data = response.json()
        assert "emotional_resonance" in data
        assert "engagement_score" in data
        assert "therapeutic_alignment" in data
        assert "readability_metrics" in data

    def test_story_collaboration(self, client, auth_headers):
        """Test story collaboration features."""
        # Create a story first
        story_data = {
            "title": "Collaborative Story",
            "description": "Story for collaboration testing",
            "genre": "fantasy",
            "themes": ["teamwork"],
            "target_audience": "young_adult",
            "length_preference": "long",
            "therapeutic_goals": ["social_skills"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Add collaboration session
        collab_data = {
            "session_type": "brainstorming",
            "participants": ["agent_architect", "agent_scribe"],
            "parameters": {
                "focus": "character_development",
                "time_limit": 30
            }
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/collaborate",
            json=collab_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert "session_id" in data
        assert "status" in data
        assert "participants" in data
        assert len(data["participants"]) == 2

    def test_story_export(self, client, auth_headers):
        """Test story export functionality."""
        # Create a story first
        story_data = {
            "title": "Export Test Story",
            "description": "Story for export testing",
            "genre": "mystery",
            "themes": ["investigation"],
            "target_audience": "adult",
            "length_preference": "medium",
            "therapeutic_goals": ["critical_thinking"]
        }
        create_response = client.post("/api/v1/stories/", json=story_data, headers=auth_headers)
        story_id = create_response.json()["id"]

        # Export story
        export_data = {
            "format": "pdf",
            "include_analytics": True,
            "include_metadata": True
        }

        response = client.post(
            f"/api/v1/stories/{story_id}/export",
            json=export_data,
            headers=auth_headers
        )
        assert response.status_code == 200

        data = response.json()
        assert "export_url" in data
        assert "format" in data
        assert data["format"] == "pdf"
        assert "expires_at" in data

    def test_unauthorized_access(self, client):
        """Test unauthorized access to protected endpoints."""
        # Try to access protected endpoint without auth
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401

        # Try to create story without auth
        story_data = {"title": "Unauthorized Story", "genre": "test"}
        response = client.post("/api/v1/stories/", json=story_data)
        assert response.status_code == 401

    def test_invalid_story_data(self, client, auth_headers):
        """Test validation of invalid story data."""
        # Try to create story with invalid data
        invalid_data = {
            "title": "",  # Empty title should fail
            "genre": "invalid_genre",  # Invalid genre
            "length_preference": "invalid_length"  # Invalid length
        }

        response = client.post("/api/v1/stories/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    def test_story_not_found(self, client, auth_headers):
        """Test accessing non-existent story."""
        response = client.get("/api/v1/stories/99999", headers=auth_headers)
        assert response.status_code == 404

        response = client.put("/api/v1/stories/99999", json={"title": "Update"}, headers=auth_headers)
        assert response.status_code == 404

        response = client.delete("/api/v1/stories/99999", headers=auth_headers)
        assert response.status_code == 404