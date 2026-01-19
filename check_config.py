#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
import os
from dotenv import load_dotenv
load_dotenv()

from app.api.v1.stories import USE_REAL_AGENTS, check_api_keys_configured

print('API keys configured:', check_api_keys_configured())
print('USE_REAL_AGENTS:', USE_REAL_AGENTS)
print('OPENAI_API_KEY exists:', bool(os.getenv('OPENAI_API_KEY')))
print('OPENAI_API_KEY length:', len(os.getenv('OPENAI_API_KEY', '')))