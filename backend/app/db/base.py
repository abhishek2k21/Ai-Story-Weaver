"""
Database connection and session management for AI Story Weaver Pro.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import redis

# Optional imports for testing
try:
    import pinecone
    PINECONE_AVAILABLE = True
except ImportError:
    PINECONE_AVAILABLE = False
    pinecone = None

try:
    import neo4j
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    neo4j = None

from app.core.config import settings

# SQLAlchemy setup - lazy initialization for testing
engine = None
SessionLocal = None

def get_engine():
    """Get or create the database engine."""
    global engine
    if engine is None:
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            echo=settings.debug
        )
    return engine

def get_session_local():
    """Get or create the session local."""
    global SessionLocal
    if SessionLocal is None:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return SessionLocal

Base = declarative_base()

# Redis connection
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

# Pinecone setup
pinecone_client = None
if PINECONE_AVAILABLE and settings.pinecone_api_key and settings.pinecone_environment:
    try:
        pinecone.init(api_key=settings.pinecone_api_key, environment=settings.pinecone_environment)
        pinecone_client = pinecone
    except Exception as e:
        print(f"Pinecone initialization failed: {e}")

# Neo4j setup
neo4j_driver = None
if NEO4J_AVAILABLE:
    try:
        neo4j_driver = neo4j.GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password)
        )
    except Exception as e:
        print(f"Neo4j driver initialization failed: {e}")

def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

def test_database_connection() -> bool:
    """Test database connection."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def test_redis_connection() -> bool:
    """Test Redis connection."""
    try:
        redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {e}")
        return False

def test_pinecone_connection() -> bool:
    """Test Pinecone connection."""
    try:
        if pinecone_client:
            pinecone_client.list_indexes()
            return True
        return False
    except Exception as e:
        print(f"Pinecone connection failed: {e}")
        return False

def test_neo4j_connection() -> bool:
    """Test Neo4j connection."""
    try:
        if neo4j_driver:
            with neo4j_driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                return record["test"] == 1
        return False
    except Exception as e:
        print(f"Neo4j connection failed: {e}")
        return False

def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=get_engine())
    print("Database tables created successfully")

def drop_tables():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=get_engine())
    print("Database tables dropped successfully")