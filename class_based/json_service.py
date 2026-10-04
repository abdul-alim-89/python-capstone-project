"""Service class for reading JSON files."""

import json
from pathlib import Path


class JsonService:
    """Service class to handle JSON file reading."""

    def read_json(self, file: Path):
        """Read JSON file."""

        with file.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)