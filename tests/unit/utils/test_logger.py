from unittest import TestCase
from app.utils import logger


class TestLogger(TestCase):

    def setUp(self):
        self.log = logger.get_logger('tests')

    def test_log(self):
        self.log.info('tests')

    def test_log_custom_fields(self):
        self.log.info('tests', {'custom_key': 'custom_value'})
