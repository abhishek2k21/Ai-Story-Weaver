#!/usr/bin/env python3
"""
Startup script for AI Story Weaver Pro backend
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "backend"))

if __name__ == "__main__":
    try:
        # Import and run the FastAPI app
        from backend.app.main import app
        import uvicorn

        print("🚀 Starting AI Story Weaver Pro Backend")
        print("=" * 50)

        uvicorn.run(
            "backend.app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for stable production-like operation
            log_level="info"
        )

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup error: {e}")
        sys.exit(1)