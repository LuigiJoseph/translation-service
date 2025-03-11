from pymongo import MongoClient
from pathlib import Path
import yaml
import hashlib

from python_services.sync.log.loggers import logger
from config import load_config

config = load_config()


mongo_HOST = config["database"]["host"]
mongo_PORT = int(config["database"]["port"])
mongo_NAME = config["database"]["name"]
mongo_collection = config["database"]["collection"]
mongo_USER = config["database"]["username"]
mongo_PASS = config["database"]["password"]


mongo_url=f"mongodb://{mongo_USER}:{mongo_PASS}@{mongo_HOST}:{mongo_PORT}/"

#for testing locally
# mongo_url=f"mongodb://localhost:27017/"

client = MongoClient(mongo_url)

logger.info(f"mongoDB connected url: {mongo_url}")
# logger.info(f"Number of handlers attached: {len(logger.handlers)}")


translation_db = client[mongo_NAME]
translation_cache = translation_db[mongo_collection]


def generate_cache_key(text, source_locale, target_locale, model_name):
    key_string = f"{text}-{source_locale}-{target_locale}-{model_name}"
    return hashlib.sha256(key_string.encode()).hexdigest()