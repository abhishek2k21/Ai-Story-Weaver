#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
import os
from dotenv import load_dotenv
load_dotenv()

try:
    from app.api.v1.stories import architect, scribe, editor, causality_agent
    print('Architect agent:', type(architect).__name__ if architect else 'None')
    print('Scribe agent:', type(scribe).__name__ if scribe else 'None')
    print('Editor agent:', type(editor).__name__ if editor else 'None')
    print('Causality agent:', type(causality_agent).__name__ if causality_agent else 'None')
except Exception as e:
    print('Error importing agents:', e)
    import traceback
    traceback.print_exc()