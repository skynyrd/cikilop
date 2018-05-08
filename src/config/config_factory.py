import json
import os

from src.colorful_print import print_red

env = os.environ.get('env', 'local')
print(f"Running for environment: {env}")


def get_config():
    try:
        config_file_stream = open(f'src/config/config.{env}.json')
        config_dict = json.load(config_file_stream)

        if not config_dict.get("mongo_uri", None):
            print_red(f"Configuration has missing field: mongo_uri")
            exit()

        if not config_dict.get("migrations_coll_name", None):
            print_red(f"Configuration has missing field: migrations_coll_name")
            exit()

        if not config_dict.get("migrations_db_name", None):
            print_red(f"Configuration has missing field: migrations_db_name")
            exit()

        return config_dict
    except FileNotFoundError:
        print_red(f"Cannot find file config.{env}.json")
        exit()
