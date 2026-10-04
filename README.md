# Compliance Checker Project

This project validates CSV and JSON manifest files for module compliance and generates a report showing which files are compliant and which have issues.

## Project structure

- `class_based/` - object-oriented implementation
- `function_based/` - procedural implementation
- `class.py` - entry point for the class-based version
- `function.py` - entry point for the function-based version
- `tests/` - automated test cases
- `data/` - sample manifests and CSV/JSON files

## Run instructions

### 1) Class-based implementation

```bash
cd /home/deq/capstone-project
source .venv/bin/activate
python3 class.py
```

### 2) Function-based implementation

```bash
cd /home/deq/capstone-project
source .venv/bin/activate
python3 function.py
```

### 3) Run tests

```bash
cd /home/deq/capstone-project
source .venv/bin/activate
pytest -q
```

## Design comparison: class-based vs function-based

| Aspect | Class-based design | Function-based design |
| --- | --- | --- |
| Structure | Encapsulates behavior inside service and validation classes | Uses standalone functions and modules |
| State management | Keeps configuration and report state in object attributes | Passes data between functions explicitly |
| Reuse | Easier to extend with additional services or inherited logic | Simpler for small scripts and lightweight workflows |
| Readability | Good for larger systems with clear responsibilities | Good for straightforward processing flows |
| Testing | Easy to instantiate and verify with object state | Easy to test individual functions in isolation |
| Example files | `class_based/compliance_service.py`, `class_based/validation.py` | `function_based/process.py`, `function_based/report.py`, `function_based/traversedir.py` |

## Summary

The class-based version is better suited to a larger, maintainable service architecture. The function-based version is simpler and easier to follow for smaller programs or educational comparisons of procedural vs object-oriented design.

## Notes

- The output is a JSON report containing file-level compliance metrics and per-module summaries.
- Sample input files are stored under `data/` and can be replaced or extended for testing.
