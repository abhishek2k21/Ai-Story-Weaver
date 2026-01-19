"""
Configuration settings for AI Story Weaver Pro.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "AI Story Weaver Pro"
    app_version: str = "1.0.0"
    debug: bool = False
    env: str = "development"

    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/storyweaver"

    # Redis settings
    redis_url: str = "redis://localhost:6379"

    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None
    elevenlabs_api_key: Optional[str] = None

    # External Services
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "password"

    # Blockchain
    web3_provider_url: str = "https://polygon-rpc.com/"
    private_key: Optional[str] = None

    # CORS settings
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    frontend_url: str = "http://localhost:3000"

    # Agent settings
    max_concurrent_stories: int = 10
    max_agents_per_story: int = 8
    story_timeout_minutes: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @property
    def is_development(self) -> bool:
        return self.env.lower() == "development"

    @property
    def is_production(self) -> bool:
        return self.env.lower() == "production"


# Global settings instance
settings = Settings()