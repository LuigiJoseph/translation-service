import logging
import json
from pathlib import Path
from pythonjsonlogger import jsonlogger
# Custom JSON Formatter
# class JsonFormatter(logging.Formatter):
#     def format(self, record):
#         log_obj = {
#             "name": record.name,
#             "asctime": self.formatTime(record, self.datefmt),
#             "levelname": record.levelname,
#             "message": record.getMessage()
#         }
#         return json.dumps(log_obj)



log_file_path = Path("/json_logs/logs.json")
if not log_file_path.exists():
    log_file_path.touch()

# log_file_path = Path(__file__).resolve().parents[1] / "json_logs" / "logs.json"

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)  

file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")

# Define JSON log format
log_format = jsonlogger.JsonFormatter(
"%(name)s %(asctime)s %(levelname)s %(message)s"
)

def get_logger(name):
    """Returns a logger with JSON formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(log_format)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger

# Test log message


# logger.info("Logger initialized")
