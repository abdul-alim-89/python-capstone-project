from pathlib import Path
from function_based.readcsv import read_csv
from function_based.readjson import read_json
from function_based.helper import compliance_rate, compliance_rate_by_item
from function_based.validation import validate_row
from function_based.customerror import InvalidRowError, MissingManifestError
from function_based.log_time import log_and_time

def read_manifest(file_path: Path):
    """Read CSV or JSON manifest."""

    if file_path.suffix.lower() == ".csv":

        yield from read_csv(file_path)

    elif file_path.suffix.lower() == ".json":

        yield from read_json(file_path)

    else:
        raise InvalidRowError(
            f"unsupported file type: {file_path.suffix}"
        )
    
@log_and_time   
def process_file(file):
    """Process a single CSV or JSON file and return compliance report."""
    # print("prcoess", file)
    issues_by_file = {}
    module_results = {}
    compliant_count = 0
    non_compliant_count = 0
    total_files = 0

    rows = read_manifest(file)

    for _, row in enumerate(rows, start=2):
        try:
            #print(row)
            compliant, issues, module_row_compliance = validate_row(row)
            #print(compliant)
            # print(compliant)
            # print(issues)
            filename = row.get("filename")
            total_files += 1

            if compliant:
                #print("run")
                compliant_count += 1
            else:
                non_compliant_count += 1
            if issues:
                issues_by_file[filename] = issues

            #print(compliant_count)
            module_code = row.get("module_code")

            if not module_code:
                continue

            if module_code not in module_results:
                module_results[module_code] = []

            module_results[module_code].extend(module_row_compliance)

            # print(issues_by_file)
            # print(module_results)
            # print(compliant_count)
            # print(non_compliant_count)
            # print(total_files)

            if total_files == 0:
                raise MissingManifestError("manifest is empty")

            summary_by_module = {}

            for key, item in module_results.items():

                # rates = round((module_count / module_total) % 100, 2)
                summary_by_module[key] = compliance_rate_by_item(item)

            #print(summary_by_module)

    

        except InvalidRowError:
            compliant = False
            filename = row.get("filename")
            issues = ["malformed_row"]
    # print("before result", total_files)
    return {
                    "total_files": total_files,
                    "compliant_count": compliant_count,
                    "non_compliant_count": non_compliant_count,
                    "compliance_rate": compliance_rate(
                                compliant_count,
                                total_files,
                            ),
                    "issues_by_file": issues_by_file,
                    "summary_by_module": summary_by_module,
                }
        
