import re
from function_based.customerror import InvalidRowError, MissingManifestError

PATTERN = "[A-Z]{2,4}-\d{3}"
VALID_STATUS = {"draft", "review", "final"}

def validate_filename(filename):
    """Validate PDF filename."""

    if not filename:
        raise InvalidRowError("filename is empty")

    if not str(filename).lower().endswith(".pdf"):
        raise ValueError("filename must be a PDF file")

    return True

def validate_module_code(module_code):
    """Validate module code."""

    if not module_code:
        raise InvalidRowError("module_code is empty")

    if not re.fullmatch(PATTERN, str(module_code)):
        raise ValueError("invalid module code")

    return True


def validate_page_count(page_count):
    """Validate positive integer page count."""

    if page_count is None or page_count == "":
        raise InvalidRowError("page_count is empty")

    try:
        page_count = int(page_count)
    except TypeError as exc:
        raise TypeError("page_count must be an integer") from exc
    except ValueError as exc:
        raise ValueError("page_count must be an integer") from exc

    if page_count <= 0:
        raise ValueError(
            "page_count must be greater than 0"
        )

    return True


def validate_file_size(file_size):
    """Validate positive file size."""

    if file_size is None or file_size == "":
        raise InvalidRowError("file_size_kb is empty")

    try:
        file_size = float(file_size)
    except TypeError as exc:
            raise TypeError("file_size must be an int or flot") from exc
    except ValueError as exc:
            raise ValueError("file_size must be an int or flot") from exc

    if file_size <= 0:
        raise ValueError(
            "file_size_kb must be positive"
        )

    return True


def validate_bool(value):
    """Validate boolean field."""

    if value is None or value == "":
        raise InvalidRowError(
            f"{value} is empty"
        )

    value = str(value).strip().lower()

    if isinstance(value, bool):
        raise ValueError(f"{value} must be true or false")

    if value not in {"true", "false"}:
        raise ValueError(
            f"{value} must be true or false"
        )

    return True

def validate_status(status):
    """Validate document status."""

    if not status:
        raise InvalidRowError("status is empty")

    status = str(status).strip().lower()

    if status not in VALID_STATUS:
        raise ValueError(
            f"invalid status: {status}"
        )

    return True

def validate_row(row):
    """
    Validate one CSV/JSON row.

    Every validation function is called separately.
    """

    if not isinstance(row, dict):
        raise InvalidRowError("row must be a dictionary")
 
    issues = []
    module_row_compliance = []

    VALIDATORS = {
        "filename": validate_filename,
        "module_code": validate_module_code,
        "page_count": validate_page_count,
        "file_size_kb": validate_file_size,
        "has_toc": validate_bool,
        "has_images": validate_bool,
        "status": validate_status
    }

    for field, validator in VALIDATORS.items():
        try:
            validator(row[field])
            module_row_compliance.append(True)
        except InvalidRowError:
            issues.append(f"{field}_empty")
            module_row_compliance.append(False)
        except ValueError:
            issues.append(f"{field}_invalid")
            module_row_compliance.append(False)
        except TypeError:
            issues.append(f"{field}_invalid_type")
            module_row_compliance.append(False)


    return len(issues) == 0, issues, module_row_compliance