from pymongo import MongoClient

client = MongoClient("mongodb://root:root@mongo:27017/")
print("mongoDB connected")
translation_db = client["translation"]
translationTxt_collection = translation_db["translationTxt_collection"]
