import unittest
from unittest.mock import MagicMock, patch

from src.ParsedMigrationItem import ParsedMigrationItem
from src.ciki import migrate_them_all
from src.repository.MigrationRepository import MigrationRepository
from tests.FakeUserMigrationFile import FakeUserMigrationFile


class TestWhenMigratingItems(unittest.TestCase):
    @classmethod
    @patch("src.ciki.get_db_instance")
    def setUpClass(cls, get_db_instance_mock):
        get_db_instance_mock.return_value = None
        cls.prepare_mocks()

        migrate_them_all(cls.mock_repo, [cls.parsed1, cls.parsed2, cls.parsed3])

    def test_repo_should_be_called(self):
        args, kwargs = self.mock_repo.create.call_args
        called_mig = args[0]
        self.assertTrue(called_mig.migration_items[0], "02-b.py")
        self.assertTrue(called_mig.migration_items[1], "03-c.py")

    def test_parsed1_should_not_be_migrated(self):
        self.parsed1.migration.success.assert_not_called()

    def test_parsed2_should_be_migrated(self):
        self.parsed2.migration.success.assert_called()

    def test_parsed3_should_be_migrated(self):
        self.parsed3.migration.success.assert_called()

    @classmethod
    def prepare_mocks(cls):
        cls.mock_repo = MigrationRepository(cfg=MagicMock(), client=MagicMock())
        cls.mock_repo.create = MagicMock()
        cls.mock_repo.get_already_done_items = MagicMock(return_value=["01-a.py"])

        cls.parsed1 = ParsedMigrationItem(FakeUserMigrationFile(), "01-a.py", 1)
        cls.parsed1.migration.success = MagicMock()
        cls.parsed2 = ParsedMigrationItem(FakeUserMigrationFile(), "02-b.py", 2)
        cls.parsed2.migration.success = MagicMock()
        cls.parsed3 = ParsedMigrationItem(FakeUserMigrationFile(), "03-c.py", 3)
        cls.parsed3.migration.success = MagicMock()
