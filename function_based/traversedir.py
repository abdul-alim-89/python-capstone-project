from pathlib import Path
from function_based.customerror import InvalidRowError, MissingManifestError

def traverse_directory(path: Path):
    """Find CSV and JSON files recursively."""

    if path.is_file():

        if path.suffix.lower() in {".csv", ".json"}:
            yield path

        return

    if not path.is_dir():
        raise MissingManifestError(f"path not found: {path}")

    for item in path.iterdir():

        if item.is_dir():

            yield from traverse_directory(item)

        elif item.suffix.lower() in {".csv", ".json"}:

            yield item