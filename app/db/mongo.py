from pymongo import MongoClient
from app.config import settings

_client = None


def get_db():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client[settings.MONGO_DB]