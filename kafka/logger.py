import logging
import json
from pathlib import Path
import os

# ✅ Define Log Directory and File
log_dir = Path("/json_logs")
log_file_path = log_dir / "logs.json"

# ✅ Ensure the log directory exists
log_dir.mkdir(parents=True, exist_ok=True)

# ✅ Create a Custom JSON Formatter
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "name": record.name,
            "asctime": self.formatTime(record, self.datefmt),
            "levelname": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_obj)

# ✅ Create Logger
def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Log all levels (DEBUG, INFO, WARNING, ERROR)

    # ✅ Create Handlers (File + Console)
    file_handler = logging.FileHandler(log_file_path)
    console_handler = logging.StreamHandler()

    # ✅ Assign JSON Formatter
    formatter = JsonFormatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # ✅ Add Handlers to Logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
