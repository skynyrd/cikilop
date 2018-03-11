import unittest

import time
from pymongo import MongoClient

from src.Migration import Migration
from src.repository.MigrationRepository import MigrationRepository
from src.repository.MongoInstanceFactory import get_db_instance
from tests.integration_tests.test_config import test_config


class TestWhenGettingTheLastMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = MigrationRepository(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)

        mig1 = Migration(["2-b.py"])
        time.sleep(0.5)
        mig2 = Migration(["1-a.py"])

        cls.id1 = cls.repo.create(mig1)
        cls.id2 = cls.repo.create(mig2)

        cls.last_mig = cls.repo.get_last_migration()

    def test_just_file_1_should_be_returned(self):
        self.assertIn("1-a.py", self.last_mig.migration_items)

    @classmethod
    def tearDownClass(cls):
        db = get_db_instance(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)
        col = db[test_config["migrations_coll_name"]]
        col.delete_one({"_id": cls.id1})
        col.delete_one({"_id": cls.id2})
