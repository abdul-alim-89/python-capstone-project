import json

import pytest

from class_based.compliance_service import ComplinaceService
from class_based.customerror import EmptyInputError, MissingManifestError


@pytest.fixture
def valid_csv(tmp_path):
    file = tmp_path / "manifest.csv"
    file.write_text(
        """filename,module_code,page_count,file_size_kb,has_toc,has_images,status
module1.pdf,CB-123,10,50.5,TRUE,FALSE,review
module2.pdf,XYZ-456,20,100,TRUE,FALSE,draft
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
                "status": "review"
            }
        ]""",
        encoding="utf-8",
    )
    return file


def test_generate_report_csv(valid_csv):
    service = ComplinaceService(valid_csv)

    result = json.loads(service.generate_report())
    file_report = result[str(valid_csv)]

    assert file_report["total_files"] == 2
    assert file_report["compliant_count"] == 2
    assert file_report["non_compliant_count"] == 0
    assert file_report["compliance_rate"] == 100.0


def test_generate_report_json(valid_json):
    service = ComplinaceService(valid_json)

    result = json.loads(service.generate_report())
    file_report = result[str(valid_json)]

    assert file_report["total_files"] == 1
    assert file_report["compliant_count"] == 1
    assert file_report["non_compliant_count"] == 0
    assert file_report["compliance_rate"] == 100.0


def test_generate_report_for_directory_with_multiple_files(tmp_path, valid_csv, valid_json):
    service = ComplinaceService(tmp_path)

    result = json.loads(service.generate_report())

    assert len(result) == 2
    assert str(valid_csv) in result
    assert str(valid_json) in result


def test_empty_directory_raises_empty_input_error(tmp_path):
    service = ComplinaceService(tmp_path)

    with pytest.raises(EmptyInputError):
        service.generate_report()


def test_missing_file_raises_missing_manifest_error(tmp_path):
    missing_file = tmp_path / "missing.csv"
    service = ComplinaceService(missing_file)

    with pytest.raises(MissingManifestError):
        service.generate_report()


def test_process_file_tracks_module_summary(valid_csv):
    service = ComplinaceService(valid_csv)

    report = json.loads(service.generate_report())
    file_report = report[str(valid_csv)]

    assert "summary_by_module" in file_report
    assert file_report["summary_by_module"]["CB-123"] == 100.0
    assert file_report["summary_by_module"]["XYZ-456"] == 100.0
