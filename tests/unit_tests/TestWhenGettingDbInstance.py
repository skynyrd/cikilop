import unittest
from unittest.mock import patch

from src.repository.MongoInstanceFactory import get_db_instance


class TestWhenGettingDbInstance(unittest.TestCase):
    def test_it_should_return_db_with_given_cfg_and_client(self):
        db = get_db_instance(client={"test_db": "expected"}, cfg={"db_name": "test_db"})
        self.assertEqual(db, "expected")

    @patch("src.repository.MongoInstanceFactory.get_config")
    def test_it_should_return_db_with_default_cfg(self, get_config_mock):
        get_config_mock.return_value = {"db_name": "test_db"}
        db = get_db_instance(client={"test_db": "expected"})
        self.assertEqual(db, "expected")
