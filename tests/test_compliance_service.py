import json

import pytest

from class_based.compliance_service import ComplinaceService
from class_based.customerror import (
    EmptyInputError,
    MissingManifestError,
)


@pytest.fixture
def valid_csv(tmp_path):

    file = tmp_path / "manifest.csv"

    file.write_text(
        """filename,module_code,page_count,file_size_kb,has_toc,has_images,author,status
module1.pdf,CB-123,10,50.5,TRUE,FALSE,Abdul,review
module2.pdf,XYZ-456,20,100,TRUE,FALSE,Abdul,draft
""",
        encoding="utf-8",
    )

    return file


@pytest.fixture
def valid_json(tmp_path):

    file = tmp_path / "manifest.json"

    file.write_text(
        """[
            {
                "filename": "module1.pdf",
                "module_code": "CB-123",
                "page_count": 10,
                "file_size_kb": 50.5,
                "has_toc": true,
                "has_images": false,
                "author": "Abdul",
                "status": "review"
            }
        ]""",
        encoding="utf-8",
    )

    return file


# -------------------------
# Happy Path
# -------------------------

def test_generate_report_csv(valid_csv):

    service = ComplinaceService(valid_csv)

    result = service.generate_report()

    report = json.loads(result)

    assert str(valid_csv) in report

    file_report = report[str(valid_csv)]

    assert file_report["total_files"] == 2
    assert file_report["compliant_count"] == 2
    assert file_report["non_compliant_count"] == 0
    assert file_report["compliance_rate"] == 100.0


def test_generate_report_json(valid_json):

    service = ComplinaceService(valid_json)

    result = service.generate_report()

    report = json.loads(result)

    assert str(valid_json) in report

    file_report = report[str(valid_json)]

    assert file_report["total_files"] == 1
    assert file_report["compliant_count"] == 1
    assert file_report["non_compliant_count"] == 0
    assert file_report["compliance_rate"] == 100.0


# -------------------------
# Single Row
# -------------------------

def test_single_row(valid_json):

    service = ComplinaceService(valid_json)

    result = service.generate_report()

    report = json.loads(result)

    file_report = report[str(valid_json)]

    assert file_report["total_files"] == 1


# -------------------------
# Empty File
# -------------------------

def test_empty_directory(tmp_path):

    service = ComplinaceService(tmp_path)

    with pytest.raises(EmptyInputError):
        service.generate_report()


# -------------------------
# Missing File
# -------------------------

def test_missing_file(tmp_path):

    missing_file = tmp_path / "missing.csv"

    service = ComplinaceService(missing_file)

    with pytest.raises(MissingManifestError):
        service.generate_report()


# -------------------------
# Compliance Rate
# -------------------------

def test_compliance_rate():

    result = ComplinaceService.compliance_rate(10, 8)

    assert result == 80.0


def test_zero_compliant_rate():

    result = ComplinaceService.compliance_rate(10, 0)

    assert result == 0.0


def test_module_compliance_rate():

    result = ComplinaceService.compliance_rate_by_item(
        [True, True, False, True]
    )

    assert result == 75.0