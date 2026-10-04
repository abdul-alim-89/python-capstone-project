import logging
import time
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def log_and_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        logging.info("Started: %s", func.__name__)

        try:
            result = func(*args, **kwargs)
            return result

        finally:
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time

            logging.info(
                "Finished: %s | Time: %.4f seconds", func.__name__, elapsed_time
            )

    return wrapper