from class_based.validation import Validation


def test_validate_row_accepts_json_numeric_values():
    row = {
        "filename": "module01.pdf",
        "module_code": "CB-123",
        "page_count": 10,
        "file_size_kb": 50.5,
        "has_toc": True,
        "has_images": False,
        "status": "review",
    }

    valid, issues, compliance = Validation().validate_row(row)

    assert valid is True
    assert issues == []
    assert compliance == [True, True, True, True, True, True, True]


def test_validate_row_flags_invalid_fields():
    row = {
        "filename": "",
        "module_code": "ABCD",
        "page_count": "0",
        "file_size_kb": "-1",
        "has_toc": "maybe",
        "has_images": " ",
        "status": "archived",
    }

    valid, issues, _ = Validation().validate_row(row)

    assert valid is False
    assert "filename_empty" in issues
    assert "module_code_invalid" in issues
    assert "page_count_invalid" in issues
    assert "file_size_kb_invalid" in issues
    assert "has_toc_invalid" in issues
    assert "has_images_empty" in issues
    assert "status_invalid" in issues
