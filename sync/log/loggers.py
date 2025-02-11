import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from pythonjsonlogger import jsonlogger

log_file_path = Path("/json_logs/logs.json")

if not log_file_path.exists():
    log_file_path.touch()
# log_file_path = Path(__file__).resolve().parents[1] / "json_logs" / "logs.json"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)

log_format = jsonlogger.JsonFormatter(
"%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s", 
rename_fields={"levelname": "severity", "asctime": "timestamp"},
    datefmt="%Y-%m-%d %H:%M:%S" 
)


if not logger.hasHandlers():
    file_handler =RotatingFileHandler(log_file_path,  backupCount=5, maxBytes=5000000)
    file_handler.setFormatter(log_format)
    stdoutHandler.setFormatter(log_format)
    logger.addHandler(file_handler)

# def get_logger(name):
#     """Returns a logger with JSON formatting."""
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
    
#     # file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)

#     # file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
#     if not logger.hasHandlers():
#         # file_handler = logging.FileHandler(log_file_path , mode="a" , encoding="utf-8")
#         file_handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
#         file_handler.setFormatter(log_format)
#         logger.addHandler(file_handler)

#     return logger



# logger = get_logger(__name__)
logger.info("Logger initialized")