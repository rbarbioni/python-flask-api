from app.api import health
from unittest import TestCase


class TestHealth(TestCase):

    def test_health_get(self):
        resp = health.get()
        self.assertTrue(resp, {'status': 'ok'})
