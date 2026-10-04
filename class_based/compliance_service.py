"""compliance service module to handle compliance checking for CSV and JSON files."""

from pathlib import Path
import json
from class_based.csv_service import CsvService
from class_based.json_service import JsonService
from class_based.customerror import MissingManifestError, EmptyInputError, InvalidRowError
from class_based.validation import Validation

class ComplinaceService:
    """Service class to handle compliance checking."""

    def __init__(self, path: Path):
        self.input_path = path
        self.csv = CsvService()
        self.json = JsonService()
        self.validation = Validation()
        self.reports = {}

    def generate_report(self):
        """Generate compliance report for CSV and JSON files."""

        # print(f"Processing path: {self.input_path}")
        # print(f"Is file: {self.input_path.is_file()}")
        if self.input_path.is_file():
            result = self.process_file(self.input_path)
            self.reports[str(self.input_path)] = result

        else:
            if not self.input_path.is_dir():
                raise MissingManifestError(f"path not found: {self.input_path}")
            
            for file in self.traverse_dir():

                result = self.process_file(file)

                self.reports[str(file)] = result

        if not self.reports:
            raise EmptyInputError("No CSV or JSON files found")   
          
        return json.dumps(self.reports, indent=4)

    def traverse_dir(self, path=None):
        """Traverse directory to find CSV and JSON files."""

        path = path or self.input_path

        print(f"Traversing path: {path}")

        if path.suffix.lower() in {".csv", ".json"}:

            yield path

        if not path.is_dir():
            raise MissingManifestError(f"path not found: {path}")

        for item in path.iterdir():

            print(item)

            if item.is_dir():

                yield from self.traverse_dir(item)

            elif item.suffix.lower() in {".csv", ".json"}:
                yield item

    def read_manifest(self, file: Path):
        """Read CSV or JSON manifest."""

        if file.suffix.lower() in {".csv"}:
            return self.csv.read_csv(file)

        elif file.suffix.lower() in {".json"}:
            return self.json.read_json(file)

    def process_file(self, file: Path):
        """Process a single CSV or JSON file and return compliance report."""

        #print(f"Processing file: {file}")
        issues_by_file = {}
        module_results = {}
        compliant_count = 0
        non_compliant_count = 0
        total_files = 0
        summary_by_module = {}
        rows = self.read_manifest(file)

        #print("rows", rows)


        for _, row in enumerate(rows, start=2):
            try:
                compliant, issues, module_row_compliance = self.validation.validate_row(row)

            except InvalidRowError as err:
                compliant = False
                issues = [str(err)]
                module_row_compliance = []
                # print("/////////////////////////////////////")

                # print(compliant, issues)

                # print("////////////////////////////////////////")

            filename = row["filename"]
            
            if filename:
                total_files += 1

            if compliant:
                compliant_count += 1
            else:
                non_compliant_count += 1
                
            if issues:
                issues_by_file[filename] = issues

            module_code = row.get("module_code")
            if not module_code:
                continue

            if module_code not in module_results:
                module_results[module_code] = []
                
            module_results[module_code].extend(module_row_compliance)

                #print(module_results)
            
        # print(issues_by_file)
        # print(module_results)

        for key, item in module_results.items():
            summary_by_module[key] = ComplinaceService.compliance_rate_by_item(item)
        return {
                            "total_files": total_files,
                            "compliant_count": compliant_count,
                            "non_compliant_count": non_compliant_count,
                            "compliance_rate": ComplinaceService.compliance_rate(total_files, compliant_count),
                            "issues_by_file": issues_by_file,
                            "summary_by_module": summary_by_module,
                        }

    @staticmethod
    def compliance_rate_by_item(item: list):
        """Calculate compliance rate for a list of boolean values."""
        true_count = sum(item)
        
        rate = round((true_count / len(item)) * 100, 2)
        
        return rate

    @staticmethod
    def compliance_rate(total_file, count):
        """Calculate compliance rate given total files and compliant count."""

        if count == 0:
            return 0.0

        rate = round(((count / total_file) * 100), 2)

        return rate



        
   
        









    

        

