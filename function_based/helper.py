def compliance_rate_by_item(item: list):
    true_count = sum(item)
        
    rate = round((true_count / len(item)) * 100, 2)
        
    return rate

    
def compliance_rate(compliant_count, total_count):

    if total_count == 0:
        return 0.0

    rate = round((compliant_count / total_count) * 100, 2)

    return rate
