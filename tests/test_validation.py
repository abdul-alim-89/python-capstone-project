import pytest

from class_based.validation import Validation
from class_based.customerror import InvalidRowError


@pytest.fixture
def validation():
    return Validation()


@pytest.fixture
def valid_row():
    return {
        "filename": "module1.pdf",
        "module_code": "CB-123",
        "page_count": 10,
        "file_size_kb": 50.5,
        "has_toc": True,
        "has_images": False,
        "author": "Abdul",
        "status": "review",
    }


# -------------------------
# Happy Path
# -------------------------

def test_valid_row(validation, valid_row):
    compliant, issues, module_result = validation.ValidationRow(valid_row)

    # print(compliant, issues, module_result)

    assert compliant is True
    assert issues == []
    assert all(module_result)


# -------------------------
# Filename
# -------------------------

def test_empty_filename(validation, valid_row):
    valid_row["filename"] = ""

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "filename_empty" in issues


def test_invalid_filename(validation, valid_row):
    valid_row["filename"] = "module1.txt"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "filename_invalid" in issues


# -------------------------
# Module Code
# -------------------------

def test_empty_module_code(validation, valid_row):
    valid_row["module_code"] = ""

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "module_code_empty" in issues


def test_invalid_module_code(validation, valid_row):
    valid_row["module_code"] = "invalid-code"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "module_code_invalid" in issues


# -------------------------
# Page Count
# -------------------------

def test_positive_page_count(validation):
    assert validation.is_valid_pagecount(1) is None


def test_zero_page_count(validation, valid_row):
    valid_row["page_count"] = 0

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "page_count_empty" in issues


def test_negative_page_count(validation, valid_row):
    valid_row["page_count"] = -1

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "page_count_invalid" in issues


def test_invalid_page_count_type(validation, valid_row):
    valid_row["page_count"] = "abc"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "page_count_invalid" in issues


# -------------------------
# File Size
# -------------------------

def test_positive_file_size(validation):
    assert validation.is_valid_file_size(10.5) is True


def test_negative_file_size(validation, valid_row):
    valid_row["file_size_kb"] = -10

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "file_size_kb_invalid" in issues


def test_invalid_file_size_type(validation, valid_row):
    valid_row["file_size_kb"] = "abc"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "file_size_kb_invalid" in issues


# -------------------------
# Boolean
# -------------------------

def test_valid_boolean(validation):
    assert validation.is_valid_bool(True) is True
    assert validation.is_valid_bool(False) is True
    assert validation.is_valid_bool("true") is True
    assert validation.is_valid_bool("false") is True


def test_invalid_boolean(validation, valid_row):
    valid_row["has_toc"] = "yes"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "has_toc_invalid" in issues


# -------------------------
# Status
# -------------------------

def test_valid_status(validation):
    assert validation.is_valid_status("draft") is True
    assert validation.is_valid_status("review") is True
    assert validation.is_valid_status("final") is True


def test_invalid_status(validation, valid_row):
    valid_row["status"] = "published"

    compliant, issues, _ = validation.ValidationRow(valid_row)

    assert compliant is False
    assert "status_invalid" in issues


# -------------------------
# Invalid Row Type
# -------------------------

def test_invalid_row_type(validation):
    with pytest.raises(InvalidRowError, match="row must be a dictionary"):
        validation.ValidationRow("invalid row")