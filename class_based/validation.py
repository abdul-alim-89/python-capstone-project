from class_based.customerror import InvalidRowError
import re
class Validation:

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

    def ValidationRow(self, row):

        issues = []

        module_row_compliance = []

        for field, validator in self.__VALIDATORS.items():
            try:
                self.__getattribute__(validator)(row[field])
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

        # if not isinstance(row, dict):
        #     raise InvalidRowError("row must be a dictionary")
        # try:
        #     self.is_valid_filename(row["filename"])
        #     module_row_compliance.append(True)
        # except InvalidRowError:
        #     issues.append("filename_empty")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("filename_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #     self.is_valid_code(row["module_code"])
        #     module_row_compliance.append(True)
        # except InvalidRowError:
        #     issues.append("module_code_empty")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("module_code_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #     self.is_valid_pagecount(row["page_count"])
        #     module_row_compliance.append(True)
        # except InvalidRowError:
        #     issues.append("page_count_empty")
        #     module_row_compliance.append(False)
        # except TypeError:
        #     issues.append("page_count_invalid_type")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("page_count_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #      self.is_valid_file_size(row["file_size_kb"])
        #      module_row_compliance.append(True)
        # except InvalidRowError:
        #      issues.append("file_size_kb_empty")
        #      module_row_compliance.append(False)
        # except TypeError:
        #     issues.append("file_size_kb_invalid_type")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("file_size_kb_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #     self.is_valid_bool(row["has_toc"])
        #     module_row_compliance.append(True)
            
        # except InvalidRowError:
        #     issues.append("has_toc_empty")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("has_toc_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #     self.is_valid_bool(row["has_images"])
        #     module_row_compliance.append(True)
        # except InvalidRowError:
        #     issues.append("has_images_empty")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("has_images_invalid")
        #     module_row_compliance.append(False)
        
        # try:
        #     self.is_valid_status(row["status"])
        #     module_row_compliance.append(True)
        # except InvalidRowError:
        #     issues.append("status_empty")
        #     module_row_compliance.append(False)
        # except ValueError:
        #     issues.append("status_invalid")
        #     module_row_compliance.append(False)

        return len(issues) == 0, issues, module_row_compliance
        


    def is_valid_filename(self, filename):
        if not filename:
            raise InvalidRowError("filename is empty")

        if not str(filename).lower().endswith(".pdf"):
            raise ValueError("filename must be a PDF file")

        return True
        



    def is_valid_pagecount(self, pagecount):
        if not pagecount:
            raise InvalidRowError("page count is empty")
        try:
            pagecount = int(pagecount)
        except TypeError:
            raise TypeError("page_count must be an integer")
        except ValueError:
            raise ValueError("page_count must be an integer")
        if pagecount <= 0:
            raise ValueError("page_count must be positive")
        

    def is_valid_file_size(self, filesize):

        if not filesize:
            raise InvalidRowError("filesize is empty")
        try:
            filesize = float(filesize)
        except TypeError:
            raise TypeError("file_size must be an int or flot")
        except ValueError:
            raise ValueError("file_size must be an int or flot")

        if filesize <= 0:
            raise ValueError("file_size_kb must be positive")

        return True

    def is_valid_bool(self, val):
        
        if val is None or val == "":
            raise InvalidRowError(f"{val} is empty")

        if isinstance(val, bool):
            return True

        if not isinstance(val, str):
            raise TypeError(f"{val} must be a string or boolean")

        val = val.strip().lower()

        if val not in {"true", "false"}:
            raise ValueError(f"{val} must be true or false")

        return True

    def is_valid_status(self, status):

        if not status:
            raise InvalidRowError("status is empty")

        status = str(status).strip().lower()

        if status not in Validation.__STATUS:
            raise ValueError(f"Invalide status {status}")

        return True

    def is_valid_code(self, code):

        if not code:
            raise InvalidRowError("module_code is empty")
    
        if not re.fullmatch(self.__PATTERN, str(code)):
            raise ValueError("invalid module code")
    
        return True