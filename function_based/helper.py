def compliance_rate_by_item(item: list):
    """Calculate compliance rate for a list of boolean values."""
    true_count = sum(item)
        
    rate = round((true_count / len(item)) * 100, 2)
        
    return rate

    
def compliance_rate(compliant_count, total_count):
    """Calculate compliance rate given total files and compliant count."""

    if total_count == 0:
        return 0.0

    rate = round((compliant_count / total_count) * 100, 2)

    return rate
