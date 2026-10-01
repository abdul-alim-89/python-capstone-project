import json
from pathlib import Path
def read_json(file: Path):
      
      with file.open("r", encoding="utf-8") as json_file:
          return json.load(json_file)