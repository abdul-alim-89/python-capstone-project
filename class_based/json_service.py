import json
from pathlib import Path


class JsonService:

    def read_json(self, file: Path):

        with file.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)