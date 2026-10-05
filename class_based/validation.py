"""Validation class for checking the compliance of module rows."""

import re
from class_based.customerror import InvalidRowError

class Validation:
    """Class to validate module rows for compliance."""

    __PATTERN = r"[A-Z]{2,4}-\d{3}"
    __STATUS =  {"draft", "review", "final"}

    __VALIDATORS = {
        "filename" : "is_valid_filename",
        "module_code" : "is_valid_code",
        "page_count" : "is_valid_pagecount",
        "file_size_kb" : "is_valid_file_size",
        "has_toc" : "is_valid_bool",
        "has_images" : "is_valid_bool",
        "status" : "is_valid_status"
    }

    @staticmethod
    def _normalize_text(value):
        """Normalize values from CSV or JSON rows to a string for validation."""
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        return str(value).strip()

    def validate_row(self, row):
        """Validate a single row of module data."""

        issues = []

        module_row_compliance = []

        for field, validator in self.__VALIDATORS.items():
            try:
                self.__getattribute__(validator)(row.get(field))
              
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
        


    def is_valid_filename(self, filename):
        """Validate the filename field."""
        filename = self._normalize_text(filename)
        if not filename:
            raise InvalidRowError("filename is empty")

        if not filename.lower().endswith(".pdf"):
            raise ValueError("filename must be a PDF file")

        return True

    def is_valid_pagecount(self, pagecount):
        """Validate the page count field."""
        pagecount = self._normalize_text(pagecount)
        if not pagecount:
            raise InvalidRowError("page count is empty")
        try:
            pagecount = int(pagecount)
        except (TypeError, ValueError) as exc:
            raise ValueError("page_count must be an integer") from exc
        if pagecount <= 0:
            raise ValueError("page_count must be positive")

        return True

    def is_valid_file_size(self, filesize):
        """Validate the file size field."""
        filesize = self._normalize_text(filesize)

        if not filesize:
            raise InvalidRowError("filesize is empty")
        try:
            filesize = float(filesize)
        except (TypeError, ValueError) as exc:
            raise ValueError("file_size must be an int or float") from exc

        if filesize <= 0:
            raise ValueError("file_size_kb must be positive")

        return True

    def is_valid_bool(self, val):
        """Validate the boolean field."""
        if val is None:
            raise InvalidRowError(f"{val} is empty")

        if isinstance(val, bool):
            return True

        val = self._normalize_text(val)
        if val == "":
            raise InvalidRowError(f"{val} is empty")

        if not isinstance(val, str):
            raise TypeError(f"{val} must be a string or boolean")

        val = val.lower()

        if val not in {"true", "false"}:
            raise ValueError(f"{val} must be true or false")

        return True

    def is_valid_status(self, status):
        """Validate the status field."""
        status = self._normalize_text(status)

        if not status:
            raise InvalidRowError("status is empty")

        status = status.lower()

        if status not in Validation.__STATUS:
            raise ValueError(f"Invalide status {status}")

        return True

    def is_valid_code(self, code):
        """Validate the module code field."""
        code = self._normalize_text(code)

        if not code:
            raise InvalidRowError("module_code is empty")

        if not re.fullmatch(self.__PATTERN, code):
            raise ValueError("invalid module code")

        return True