"""
Config file loader.
"""

import json
from pathlib import Path

def load_config() -> dict:
    """Load ~/.filetreerc if it exists."""
    config_path = Path.home() / ".filetreerc"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}
