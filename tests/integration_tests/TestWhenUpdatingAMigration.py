import unittest

from pymongo import MongoClient

from src.Migration import Migration
from src.repository.MigrationRepository import MigrationRepository
from src.repository.MongoInstanceFactory import get_db_instance
from tests.integration_tests.test_config import test_config


class TestWhenUpdatingAMigration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = MigrationRepository(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)

        mig1 = Migration(["2-b.py"])
        cls.id1 = cls.repo.create(mig1)

        mig1.make_reverted()
        cls.last_mig = cls.repo.update_migration(mig1.to_document())

    def test_just_file_1_should_be_returned(self):
        self.assertTrue(self.last_mig.is_reverted)

    @classmethod
    def tearDownClass(cls):
        db = get_db_instance(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)
        col = db[test_config["migrations_db_name"]][test_config["migrations_coll_name"]]
        col.delete_one({"_id": cls.id1})
