import unittest

from pymongo import MongoClient

from src.Migration import Migration
from src.repository.MigrationRepository import MigrationRepository
from src.repository.MongoInstanceFactory import get_db_instance
from tests.integration_tests.test_config import test_config


class TestWhenGettingAlreadyDoneItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = MigrationRepository(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)

        mig1 = Migration(["1-a.py"])
        mig2 = Migration(["2-b.py"])
        mig3 = Migration(["3-c.py"])
        mig3.make_reverted()

        cls.id1 = cls.repo.create(mig1)
        cls.id2 = cls.repo.create(mig2)
        cls.id3 = cls.repo.create(mig3)

        cls.already_done_files = cls.repo.get_already_done_items(["1-a.py", "3-c.py"])

    def test_just_file_1_should_be_returned(self):
        self.assertEqual(self.already_done_files, set(["1-a.py"]))

    @classmethod
    def tearDownClass(cls):
        db = get_db_instance(client=MongoClient(test_config["mongo_uri"]), cfg=test_config)
        col = db[test_config["migrations_coll_name"]]
        col.delete_one({"_id": cls.id1})
        col.delete_one({"_id": cls.id2})
        col.delete_one({"_id": cls.id3})
