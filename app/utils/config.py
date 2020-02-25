from dynaconf import settings
from os import getenv


def get_config(key=None, default=None, cast=None):
    return getenv(key) or settings(key, default, cast=cast)
