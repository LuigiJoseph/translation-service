from pymongo import MongoClient
import hashlib

from python_services.sync.log.loggers import logger
from python_services.config import load_config

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


translation_db = client[mongo_NAME]
translation_cache = translation_db[mongo_collection]


def generate_cache_key(text, source_locale, target_locale, model_name):
    key_string = f"{text}-{source_locale}-{target_locale}-{model_name}"
    return hashlib.sha256(key_string.encode()).hexdigest()

def cache_translations(cache_key, text, source_locale, target_locale, model_name, translated_text):
    """Store translation in MongoDB."""
    translation_cache.insert_one({
            "_id": cache_key,
            "source_text": text,
            "source_language": source_locale,
            "target_language": target_locale,
            "model_used": model_name,
            "translated_text": translated_text
    })

def get_cached_translation(cache_key):
    """Retrieve cached translation from MongoDB using the generated cache key."""
    cached_result = translation_cache.find_one({"_id": cache_key})
    return cached_result
