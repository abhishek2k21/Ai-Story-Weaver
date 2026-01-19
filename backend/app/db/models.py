"""
Database models for AI Story Weaver Pro.
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()

# Association tables for many-to-many relationships
story_agents = Table(
    'story_agents',
    Base.metadata,
    Column('story_id', Integer, ForeignKey('stories.id'), primary_key=True),
    Column('agent_id', Integer, ForeignKey('agents.id'), primary_key=True)
)

user_stories = Table(
    'user_stories',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('story_id', Integer, ForeignKey('stories.id'), primary_key=True)
)

class User(Base):
    """User model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    tier = Column(String(50), default="free")  # free, premium, enterprise
    credits = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stories = relationship("Story", secondary=user_stories, back_populates="collaborators")
    sessions = relationship("Session", back_populates="user")

class Story(Base):
    """Story model."""
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    genre = Column(String(100))
    status = Column(String(50), default="draft")  # draft, in_progress, completed, archived
    story_bible = Column(JSON)  # Complete story structure and metadata
    current_branch = Column(String(100), default="main")
    branches = Column(JSON)  # Available story branches
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    collaborators = relationship("User", secondary=user_stories, back_populates="stories")
    sessions = relationship("Session", back_populates="story")
    agents = relationship("Agent", secondary=story_agents, back_populates="stories")

class Agent(Base):
    """AI Agent model."""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # architect, scribe, editor, etc.
    description = Column(Text)
    configuration = Column(JSON)  # Agent-specific settings
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    stories = relationship("Story", secondary=story_agents, back_populates="agents")
    sessions = relationship("Session", back_populates="agent")

class Session(Base):
    """User session model."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    story_id = Column(Integer, ForeignKey("stories.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    session_type = Column(String(50))  # story_creation, collaboration, therapy
    status = Column(String(50), default="active")  # active, completed, paused
    session_data = Column(JSON)  # Session state and metadata
    biometric_data = Column(JSON)  # Emotional state tracking
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="sessions")
    story = relationship("Story", back_populates="sessions")
    agent = relationship("Agent", back_populates="sessions")

class AuditLog(Base):
    """Audit log for ethical oversight."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))  # story, session, agent
    resource_id = Column(Integer)
    details = Column(JSON)
    ethical_score = Column(Float)
    risk_level = Column(String(20))  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models for API responses
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    tier: str
    credits: int
    created_at: datetime

    class Config:
        orm_mode = True

class StoryResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    genre: Optional[str]
    status: str
    current_branch: str
    created_at: datetime
    collaborators: List[UserResponse] = []

    class Config:
        orm_mode = True

class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class SessionResponse(BaseModel):
    id: int
    user_id: int
    story_id: int
    agent_id: Optional[int]
    session_type: Optional[str]
    status: str
    started_at: datetime
    ended_at: Optional[datetime]

    class Config:
        orm_mode = True