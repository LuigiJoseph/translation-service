import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pythonjsonlogger import jsonlogger

# Define log file path
log_dir = Path("/json_logs")
log_file_path = log_dir / "logs.json"

# Ensure log directory exists
log_dir.mkdir(parents=True, exist_ok=True)

# Ensure log file exists
if not log_file_path.exists():
    log_file_path.touch()

# JSON log formatting
log_format = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name):
    """Returns a logger with JSON formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Use RotatingFileHandler to avoid log file growing indefinitely
    file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setFormatter(log_format)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger

# Example usage
logger = get_logger(__name__)
logger.info("Logger initialized")
