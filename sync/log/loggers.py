import logging
import sys
from pythonjsonlogger import jsonlogger

# Create logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define log format using pythonjsonlogger
log_format = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console (stdout) handler for terminal logging
stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)

# Log message
logger.info("Logger initialized")
