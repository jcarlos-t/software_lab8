"""Pytest configuration for notification-service."""

import sys
from pathlib import Path

# Add shared module to Python path
shared_path = Path(__file__).parent.parent.parent / "shared"
if str(shared_path) not in sys.path:
    sys.path.insert(0, str(shared_path))
