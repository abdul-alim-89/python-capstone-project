from pathlib import Path
from class_based.compliance_service import ComplinaceService

try: 
    path = Path("data")
    
    service = ComplinaceService(path)
    
    report = service.generate_report()
    
    print(report)

except FileNotFoundError as err:
    print(err)

except PermissionError as err:
    print(err)

except Exception as err:
    print(err)

else:
    print("report generated successfully")