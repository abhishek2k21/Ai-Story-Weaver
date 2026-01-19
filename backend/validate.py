#!/usr/bin/env python3
"""
Simple test script to validate database models and basic functionality.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, User, Story, Agent, Session

def test_database_models():
    """Test database models with SQLite."""
    print("Testing database models...")

    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        # Test User creation
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashed_password",
            full_name="Test User"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"✓ User created: {user.username}")

        # Test Story creation
        story = Story(
            title="Test Story",
            description="A test story",
            genre="fantasy",
            status="draft",
            story_bible={"scenes": [], "test": True}
        )
        session.add(story)
        session.commit()
        session.refresh(story)
        print(f"✓ Story created: {story.title}")

        # Test Agent creation
        agent = Agent(
            name="Test Agent",
            type="architect",
            description="Test agent",
            configuration={"test_mode": True}
        )
        session.add(agent)
        session.commit()
        session.refresh(agent)
        print(f"✓ Agent created: {agent.name}")

        # Test Session creation
        story_session = Session(
            user_id=user.id,
            story_id=story.id,
            agent_id=agent.id,
            session_type="storytelling",
            status="active",
            session_data={"current_scene": 1, "test_session": True}
        )
        session.add(story_session)
        session.commit()
        session.refresh(story_session)
        print(f"✓ Session created: {story_session.session_type}")

        # Test relationships
        user.stories.append(story)
        session.commit()
        session.refresh(user)
        print(f"✓ User-Story relationship: {len(user.stories)} stories")

        print("🎉 All database model tests passed!")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        session.close()

def test_imports():
    """Test that all imports work."""
    print("Testing imports...")

    try:
        from app.db.base import get_db, test_database_connection
        from app.core.config import settings
        from app.db.models import User, Story, Agent, Session
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running AI Story Weaver Pro validation tests...\n")

    success = True

    if not test_imports():
        success = False

    if not test_database_models():
        success = False

    if success:
        print("\n🎉 All validation tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)