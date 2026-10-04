from function_based.helper import compliance_rate

def merged_report(reports):
    """Merge multiple compliance reports into a single report."""
    
    merged = {
    "total_files": 0,
    "compliant_count": 0,
    "non_compliant_count": 0,
    "compliance_rate": 0,
    "issues_by_file": {},
    "summary_by_module": {}
}

    for report in reports:
        merged["total_files"] += report["total_files"]
        merged["compliant_count"] += report["compliant_count"]
        merged["non_compliant_count"] += report["non_compliant_count"]

        for filename, issues in report["issues_by_file"].items():
            if filename in merged["issues_by_file"]:
                merged["issues_by_file"][filename].extend(issues)
            else:
                merged["issues_by_file"][filename] = issues.copy()

            merged["summary_by_module"].update(report["summary_by_module"])

            merged["compliance_rate"] = compliance_rate(merged["compliant_count"], merged["total_files"])
    return merged
