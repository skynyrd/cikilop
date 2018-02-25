class ParsedMigrationItem(object):
    def __init__(self, migration, file_name, order: int):
        self.migration = migration
        self.file_name = file_name
        self.order = order
