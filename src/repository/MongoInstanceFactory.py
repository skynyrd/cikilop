from pymongo import MongoClient

from src.config.config_factory import get_config


def get_db_instance(client: MongoClient = None, cfg=None):
    cfg = get_config() if not cfg else cfg
    client = MongoClient(cfg["mongo_uri"]) if not client else client
    db = client[cfg["db_name"]]
    return db
