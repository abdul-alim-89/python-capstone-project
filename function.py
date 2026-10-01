from pathlib import Path
import json
from function_based.log import logger
from function_based.customerror import InvalidRowError, MissingManifestError, EmptyInputError
from function_based.traversedir import traverse_directory
from function_based.process import process_file
from function_based.report import merged_report

def main():



    try:
        input_path = Path("data")

        if not input_path.exists():
            raise MissingManifestError(f"path not found : {input_path}")

        files = list(traverse_directory(input_path))
        #print(files)
        if not files:
            raise FileNotFoundError("files not found")

        reports = {}

        for file in files:
            try:
                result = process_file(file)
                #print(result)
        
            except (MissingManifestError, InvalidRowError) as err:
                logger.error( "Could not process %s: %s", file, err,)
                continue
            else:
                reports[str(file)] = result

        if not reports:
            raise EmptyInputError("No valid manifest could be processed")
        # print("---------------------")
        # print(reports)
        # print("---------------------")
        # merged_result = merged_report(reports)
        print(json.dumps(reports, indent=4))

        


    except MissingManifestError as err:
        logger.exception(err)
        print(err)

    except EmptyInputError as err:
        logger.exception(err)
        print(err)

    except PermissionError as err:
        logger.exception(err)
        print(err)

    except Exception as err:
        logger.exception(err)
        print(err)

    else:
        logger.info("Compliance checker completed successfully")

    finally:
        logger.info("Compliance checker finished")

if __name__ == "__main__":
    main()
