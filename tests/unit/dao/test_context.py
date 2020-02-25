from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from app.dao import context


class TestDaoContext(TestCase):

    def setUp(self):
        context.Session = AlchemyMagicMock()

    def test_create_context(self):
        ctx = context.create_context(context=None)
        self.assertIsNotNone(ctx)
