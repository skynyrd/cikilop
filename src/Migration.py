from datetime import datetime
from typing import List

from bson import ObjectId


class Migration(object):
    def __init__(self, migration_item_names: List[str]):
        self.id = ObjectId()
        self.migration_items = migration_item_names
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_reverted = False

    def make_reverted(self):
        self.is_reverted = True
        self.updated_at = datetime.utcnow()

    def to_document(self):
        return {
            "_id": self.id,
            "migration_items": self.migration_items,
            "is_reverted": self.is_reverted,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def load(cls, doc):
        mig = cls(doc["migration_items"])
        mig.id = doc["_id"]
        mig.created_at = doc["created_at"]
        mig.updated_at = doc["updated_at"]
        mig.is_reverted = doc["is_reverted"]
        return mig

