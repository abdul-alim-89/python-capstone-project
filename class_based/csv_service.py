"""CSV service module to handle CSV file reading."""
import csv
from pathlib import Path
from class_based.customerror import InvalidRowError


class CsvService:
    """Service class to handle CSV file reading."""

    def read_csv(self, file_path: Path):
        """Read CSV file lazily."""
        
        with open(file_path, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames is None:
                raise InvalidRowError("CSV header is missing")
            for row in reader:
                    yield row
