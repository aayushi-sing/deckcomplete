from pathlib import Path

from app.core.models import Decklist


def load_decklists(directory: Path) -> list[Decklist]:
    return [
        Decklist.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(directory.glob("*.json"))
        if path.is_file()
    ]
