from pathlib import Path
from class_based.customerror import InvalidRowError
import csv

class CsvService:

    def read_csv(self, file_path: Path):
        with open(file_path, "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            if reader.fieldnames is None:
                raise InvalidRowError("CSV header is missing")
            for row in reader:
                    yield row
