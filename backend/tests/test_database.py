"""
Database connection tests for AI Story Weaver Pro.
"""
import pytest
from sqlalchemy.orm import Session
from app.db.base import (
    get_db, test_database_connection, test_redis_connection,
    test_pinecone_connection, test_neo4j_connection, create_tables, drop_tables
)
from app.db.models import User, Story, Agent, Session as StorySession


"""
Database connection tests for AI Story Weaver Pro.
"""
import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import Session
from app.db.base import (
    get_db, test_database_connection, test_redis_connection,
    test_pinecone_connection, test_neo4j_connection, create_tables, drop_tables
)
from app.db.models import User, Story, Agent, Session as StorySession


class TestDatabaseConnections:
    """Test database connections."""

    def test_postgresql_connection_mock(self):
        """Test PostgreSQL connection with mock."""
        with patch('app.db.base.create_engine') as mock_engine:
            mock_engine.return_value = MagicMock()
            # Mock successful connection
            result = test_database_connection()
            # Should not raise exception
            assert isinstance(result, bool)

    def test_redis_connection_mock(self):
        """Test Redis connection with mock."""
        with patch('app.db.base.redis.Redis') as mock_redis:
            mock_instance = MagicMock()
            mock_redis.return_value = mock_instance
            mock_instance.ping.return_value = True

            result = test_redis_connection()
            assert isinstance(result, bool)

    def test_pinecone_connection_mock(self):
        """Test Pinecone connection with mock."""
        with patch('app.db.base.Pinecone') as mock_pinecone:
            mock_instance = MagicMock()
            mock_pinecone.return_value = mock_instance

            result = test_pinecone_connection()
            assert isinstance(result, bool)

    def test_neo4j_connection_mock(self):
        """Test Neo4j connection with mock."""
        with patch('app.db.base.GraphDatabase') as mock_neo4j:
            mock_driver = MagicMock()
            mock_neo4j.driver.return_value = mock_driver
            mock_session = MagicMock()
            mock_driver.session.return_value.__enter__.return_value = mock_session

            result = test_neo4j_connection()
            assert isinstance(result, bool)


class TestDatabaseOperations:
    """Test database operations."""

    @pytest.fixture
    def test_db_session(self):
        """Create a test database session with SQLite."""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.db.models import Base

        # Use SQLite for testing
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()

        try:
            yield session
        finally:
            session.rollback()
            session.close()
            Base.metadata.drop_all(engine)

    def test_create_user(self, test_db_session: Session):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            full_name="Test User"
        )
        test_db_session.add(user)
        test_db_session.commit()
        test_db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"

    def test_create_story(self, test_db_session: Session):
        """Test creating a story."""
        story = Story(
            title="Test Story",
            description="A test story",
            genre="fantasy",
            status="draft",
            content={"scenes": []},
            metadata={"test": True}
        )
        test_db_session.add(story)
        test_db_session.commit()
        test_db_session.refresh(story)

        assert story.id is not None
        assert story.title == "Test Story"
        assert story.status == "draft"

    def test_user_story_relationship(self, test_db_session: Session):
        """Test user-story many-to-many relationship."""
        # Create user
        user = User(
            email="author@example.com",
            username="author",
            hashed_password="hashed_password"
        )
        test_db_session.add(user)

        # Create story
        story = Story(
            title="Author's Story",
            description="Story by author",
            genre="drama",
            status="published"
        )
        test_db_session.add(story)
        test_db_session.commit()

        # Associate user with story
        user.stories.append(story)
        test_db_session.commit()

        # Verify relationship
        test_db_session.refresh(user)
        assert len(user.stories) == 1
        assert user.stories[0].title == "Author's Story"

    def test_create_agent(self, test_db_session: Session):
        """Test creating an agent."""
        agent = Agent(
            name="Test Agent",
            type="architect",
            description="Test agent for integration testing",
            capabilities=["planning", "analysis"],
            status="active",
            config={"test_mode": True}
        )
        test_db_session.add(agent)
        test_db_session.commit()
        test_db_session.refresh(agent)

        assert agent.id is not None
        assert agent.name == "Test Agent"
        assert agent.type == "architect"
        assert agent.status == "active"

    def test_create_session(self, test_db_session: Session):
        """Test creating a story session."""
        # Create user first
        user = User(
            email="session_user@example.com",
            username="sessionuser",
            hashed_password="hashed_password"
        )
        test_db_session.add(user)
        test_db_session.commit()

        session = StorySession(
            user_id=user.id,
            type="storytelling",
            status="active",
            context={"current_scene": 1},
            metadata={"test_session": True}
        )
        test_db_session.add(session)
        test_db_session.commit()
        test_db_session.refresh(session)

        assert session.id is not None
        assert session.user_id == user.id
        assert session.type == "storytelling"
        assert session.status == "active"

