import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from pythonjsonlogger import jsonlogger

log_file_path = Path("/json_logs/logs.json")

if not log_file_path.exists():
    log_file_path.touch()
# log_file_path = Path(__file__).resolve().parents[1] / "json_logs" / "logs.json"

log_format = jsonlogger.JsonFormatter(
"%(name)s %(asctime)s %(levelname)s %(message)s", 
    datefmt="%Y-%m-%d %H:%M:%S" 
)

def get_logger(name):
    """Returns a logger with JSON formatting."""
    logger = logging.getLogger(name).setLevel(logging.INFO)
    
    # file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)

    file_handler = logging.FileHandler(log_file_path , mode="w" , encoding="utf-8")

    file_handler.setFormatter(log_format)

    return logger

logger = get_logger(__name__)
logger.info("Logger initialized")