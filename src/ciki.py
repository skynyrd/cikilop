import importlib
import os
import re

import click
from asq.initiators import query

from src.Migration import Migration
from src.ParsedMigrationItem import ParsedMigrationItem
from src.colorful_print import print_blue, print_green, print_red
from src.repository.MigrationRepository import MigrationRepository
from src.repository.MongoInstanceFactory import get_db_instance

migrations_dir = "migrations"


def load_migration_items():
    py_search_re = re.compile('.py$', re.IGNORECASE)

    plugin_files = filter(py_search_re.search,
                          os.listdir(os.path.join(os.path.dirname(__file__), migrations_dir)))

    migrations = map(lambda fp: '.' + os.path.splitext(fp)[0], plugin_files)

    importlib.import_module(migrations_dir)
    module_list = []

    for migration in migrations:
        module_list.append(importlib.import_module(migration, package=migrations_dir))

    return module_list


@click.command()
@click.option('--revert', is_flag=True, help="Sorts all migrations by created_at and reverts the newest one.")
def action(revert):
    parsed_migration_items = get_parsed_migration_items()
    mig_repo = MigrationRepository()

    if revert:
        revert_peacefully(mig_repo, parsed_migration_items)
    else:
        migrate_them_all(mig_repo, parsed_migration_items)


def revert_peacefully(mig_repo, parsed_migration_items):
    last_mig = mig_repo.get_last_migration()
    if last_mig:
        items = last_mig.migration_items
        migs_to_be_applied = query(parsed_migration_items) \
            .where(lambda pmig: pmig.file_name in items) \
            .order_by_descending(lambda pmig: pmig.order).to_list()

        while len(migs_to_be_applied) > 0:
            pmig = migs_to_be_applied.pop(0)
            print_green(f"REVERT: Migration file {pmig.file_name} is going to be applied...")
            pmig.migration.fail(get_db_instance())

        last_mig.make_reverted()
        mig_repo.update_migration(last_mig.to_document())

    else:
        print_red("Revert failed: There is no migration that can be reverted in the mongo collection..")


def migrate_them_all(mig_repo, parsed_migration_items):
    already_done_mig_files = mig_repo.get_already_done_items([p.file_name for p in parsed_migration_items])

    migs_to_be_applied = query(parsed_migration_items) \
        .where(lambda pmig: pmig.file_name not in already_done_mig_files) \
        .order_by(lambda pmig: pmig.order).to_list()

    files_to_be_migrated = query(migs_to_be_applied).select(lambda pm: pm.file_name).to_list()
    while len(migs_to_be_applied) > 0:
        parsed_migration = migs_to_be_applied.pop(0)
        print_green(f"Migration file {parsed_migration.file_name} is going to be applied...")
        parsed_migration.migration.success(get_db_instance())

    if len(files_to_be_migrated) > 0:
        migration = Migration(files_to_be_migrated)
        mig_repo.create(migration)
    else:
        print_green("All the migration files already applied, skipping...")


def get_parsed_migration_items():
    migration_items = query(load_migration_items()).where(lambda mig: migrations_dir in mig.__name__ and
                                                                      mig.__name__.split(migrations_dir)[1][
                                                                          1] != "_").to_list()

    parsed_migration_items = []
    for migration_item in migration_items:
        file_name = migration_item.__name__.split(f"{migrations_dir}.")[1]
        parsed_migration_items.append(ParsedMigrationItem(migration_item, file_name, int(file_name.split('-')[0])))

    return parsed_migration_items


if __name__ == '__main__':
    print_blue('''
  ___(_) | _(_) | ___  _ __  
 / __| | |/ / | |/ _ \| '_ \ 
| (__| |   <| | | (_) | |_) |
 \___|_|_|\_\_|_|\___/| .__/ 
                      |_|    
    ''')
    print_blue("Easy mongo migration for all <3")
    action()

