import os
from unittest import TestCase
from dynaconf import LazySettings
from app.utils import config


class TestConfig(TestCase):

    def setUp(self):
        config.settings = LazySettings(KEY_DYNACONF='VALUE')

    def test_get_config_not_found(self):
        conf = config.get_config('NOT_FOUND_KEY')
        self.assertIsNone(conf)

    def test_get_config_not_found_default_value(self):
        conf = config.get_config('NOT_FOUND_KEY', 'DEFAULT')
        self.assertEqual(conf, 'DEFAULT')

    def test_get_config_in_env_var(self):
        conf_declared = 'VALUE_ENV_VAR'
        key = 'KEY_ENV_VAR'
        os.environ[key] = conf_declared
        conf = config.get_config(key)
        self.assertEqual(conf, conf_declared)

    def test_get_config_in_dynaconf(self):
        conf = config.get_config('KEY_DYNACONF')
        self.assertEqual(conf, 'VALUE')

    def test_get_config_in_env_var_x_dynaconf_priority(self):
        key = 'CONFIG_KEY'
        conf_value_dynaconf = 'VALUE_DYNACONF'
        config.settings = LazySettings(KEY_DYNACONF=conf_value_dynaconf)

        conf_value_env_var = 'VALUE_ENV_VAR'
        os.environ[key] = conf_value_env_var

        conf = config.get_config(key)
        self.assertEqual(conf, conf_value_env_var)
