from pymongo import MongoClient
from src.config.config import settings


def get_database():
    mongodb_uri = settings.mongo_db_uri
    client = MongoClient(mongodb_uri)
    db = client[settings.mongo_db_name]
    return db
