import unittest
from unittest.mock import MagicMock, patch

from src.Migration import Migration
from src.ParsedMigrationItem import ParsedMigrationItem
from src.ciki import revert_peacefully
from src.repository.MigrationRepository import MigrationRepository
from tests.FakeUserMigrationFile import FakeUserMigrationFile


class TestWhenRevertingMigrationItems(unittest.TestCase):
    @classmethod
    @patch("src.ciki.get_db_instance")
    def setUpClass(cls, get_db_instance_mock):
        get_db_instance_mock.return_value = None
        cls.prepare_mocks()

        revert_peacefully(cls.mock_repo, [cls.parsed1, cls.parsed2, cls.parsed3])

    def test_repo_should_be_called(self):
        self.mock_repo.update_migration.assert_called_with(self.last_mig.to_document())

    def test_parsed1_should_not_reverted(self):
        self.parsed1.migration.fail.assert_not_called()

    def test_parsed2_should_be_reverted(self):
        self.parsed2.migration.fail.assert_called()

    def test_parsed3_should_be_reverted(self):
        self.parsed3.migration.fail.assert_called()

    @classmethod
    def prepare_mocks(cls):
        cls.mock_repo = MigrationRepository(cfg=MagicMock(), client=MagicMock())
        cls.mock_repo.update_migration = MagicMock()

        cls.last_mig = Migration(["02-b.py", "03-c.py"])
        cls.last_mig.make_reverted = MagicMock()
        cls.mock_repo.get_last_migration = MagicMock(return_value=cls.last_mig)

        cls.parsed1 = ParsedMigrationItem(FakeUserMigrationFile(), "01-a.py", 1)
        cls.parsed1.migration.fail = MagicMock()
        cls.parsed2 = ParsedMigrationItem(FakeUserMigrationFile(), "02-b.py", 2)
        cls.parsed2.migration.fail = MagicMock()
        cls.parsed3 = ParsedMigrationItem(FakeUserMigrationFile(), "03-c.py", 3)
        cls.parsed3.migration.fail = MagicMock()
