import csv
from pathlib import Path
from function_based.customerror import InvalidRowError, MissingManifestError

def read_csv(file_path: Path):
    """Read CSV file lazily."""

    with open(file_path, "r", encoding="utf-8", newline="") as csv_file:

        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise InvalidRowError(
                "CSV header is missing"
            )

        # missing_fields = (
        #     REQUIRED_FIELDS - set(reader.fieldnames)
        # )

        # if missing_fields:
        #     raise InvalidRowError(
        #         f"missing CSV fields: {missing_fields}"
        #     )

        for row in reader:
            yield row
