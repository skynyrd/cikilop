from typing import Optional

from pymongo import MongoClient, ReturnDocument

from src.Migration import Migration
from src.config.config_factory import get_config


class MigrationRepository:
    def __init__(self, client: MongoClient = None, cfg=None):
        cfg = get_config() if not cfg else cfg
        self._client = MongoClient(cfg["mongo_uri"]) if not client else client
        self._db = self._client[cfg["db_name"]]
        self._collection = self._db[cfg["migrations_coll_name"]]

    def create(self, migration: Migration):
        return self._collection.insert_one(migration.to_document()).inserted_id

    def get_already_done_items(self, file_names):
        result = []

        for raw_mig in self._collection.find({"migration_items": {"$in": file_names}, "is_reverted": False}):
            migration = Migration.load(raw_mig)
            result.append(migration)

        already_done_mig_files = set()

        for mig in result:
            for item in mig.migration_items:
                already_done_mig_files.add(item)

        return already_done_mig_files

    def get_last_migration(self) -> Optional[Migration]:
        raw_last_mig = [m for m in self._collection.find({"is_reverted": False}).sort([("created_at", -1)]).limit(1)]
        if len(raw_last_mig) != 0:
            return Migration.load(raw_last_mig[0])
        else:
            return None

    def update_migration(self, mig_doc):
        updated = self._collection.find_one_and_replace({"_id": mig_doc["_id"]}, mig_doc,
                                                        return_document=ReturnDocument.AFTER)

        if updated:
            return Migration.load(updated)
        else:
            return None
