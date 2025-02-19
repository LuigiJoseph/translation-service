from pymongo import MongoClient
import os
from pathlib import Path
import yaml

from log.loggers import logger

# logger = get_logger(__name__)

configfile_path = Path("/configs/config.yaml")
# configfile_path = Path(__file__).resolve().parents[1] / "configs"/"config.yaml"

try:
    with open(configfile_path, "r") as file:
        logger.info("File opened successfully!")
        config = yaml.safe_load(file)
except Exception as e:
    logger.info(f"Error opening file: {e}")

mongo_HOST = config["database"]["host"]
mongo_PORT = int(config["database"]["port"])
mongo_NAME = config["database"]["name"]
mongo_collection = config["database"]["collection"]
mongo_USER = config["database"]["username"]
mongo_PASS = config["database"]["password"]


mongo_url=f"mongodb://{mongo_USER}:{mongo_PASS}@{mongo_HOST}:{mongo_PORT}/"
client = MongoClient(mongo_url)

logger.info(f"mongoDB connected url: {mongo_url}")
# logger.info(f"Number of handlers attached: {len(logger.handlers)}")


translation_db = client["translation"]
translationTxt_collection = translation_db["translationTxt_collection"]
