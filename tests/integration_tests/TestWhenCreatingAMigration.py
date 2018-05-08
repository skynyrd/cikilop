import unittest

from pymongo import MongoClient

from src.Migration import Migration
from src.repository.MigrationRepository import MigrationRepository
from src.repository.MongoInstanceFactory import get_db_instance
from tests.integration_tests.test_config import test_config


class TestWhenCreatingAMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = MigrationRepository(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)
        cls.migration_for_test = Migration(["01-a.py"])
        cls.fetched_id = cls.repo.create(cls.migration_for_test)

    def test_migration_should_be_created_successfully(self):
        self.assertEqual(self.migration_for_test.id, self.fetched_id)

    @classmethod
    def tearDownClass(cls):
        db = get_db_instance(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)
        col = db[test_config["migrations_db_name"]][test_config["migrations_coll_name"]]
        col.delete_one({"_id": cls.fetched_id})
