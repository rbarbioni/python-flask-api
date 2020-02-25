from app.api import metrics
from unittest import TestCase


class TestMetrics(TestCase):

    def test_health(self):
        resp = metrics.get()
        self.assertTrue(resp, {'status_code': 200})
