import os
import ujson

env = os.environ.get('env', 'local')
print(f"Running for environment: {env}")


class CannotOpenConfigFileError(Exception):
    def __init__(self, file_name):
        super(CannotOpenConfigFileError, self).__init__(f"Cannot find file {file_name}")


def get_config():
    try:
        config_file_stream = open(f'src/config/config.{env}.json')
        return ujson.load(config_file_stream)
    except FileNotFoundError:
        raise CannotOpenConfigFileError(f"config.{env}.json")
