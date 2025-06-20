import json
import os

CONFIG_FILE = "config.json"


def load_theme() -> str:
    """Return the saved theme name or a default."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", "superhero")
        except (json.JSONDecodeError, OSError):
            pass
    return "superhero"


def save_theme(theme: str) -> None:
    """Persist the selected theme."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({"theme": theme}, f)
