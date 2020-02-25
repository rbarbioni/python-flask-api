from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from app.dao import db


class TestDaoDb(TestCase):

    def setUp(self):
        self.session = AlchemyMagicMock()

    def test_all(self):
        db.all(self.session, {})
        self.assertTrue(self.session.query.called)

    def test_query(self):
        db.query(self.session, {}, ())
        self.assertTrue(self.session.query.called)

    def test_query_all(self):
        db.query_all(self.session, {}, ())
        self.assertTrue(self.session.query.called)

    def test_query_first(self):
        db.query_first(self.session, {}, ())
        self.assertTrue(self.session.query.called)

    def test_insert(self):
        db.insert(self.session, {})
        self.assertTrue(self.session.add.called)

    def test_update(self):
        db.update(self.session, {}, (), {})
        self.assertTrue(self.session.query.called)

    def test_delete(self):
        db.delete(self.session, {}, ())
        self.assertTrue(self.session.query.called)
