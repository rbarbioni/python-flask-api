from flask import Flask
from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app.api import user


class MockFlaskRequest():

    def __init__(self, json):
        self.json = json

    def get_json(self):
        return self.json


class Testuser(TestCase):

    app = Flask(__name__)
    user_mock = {
                'id': 1,
                'name': 'user 1',
                'email': 'email@email.com',
            }

    def setUp(self):
        user.create_context = AlchemyMagicMock()

    def test_error_handler(self):
        with self.app.app_context():
            resp = user.error_handler(Exception('Generic Error'))
            self.assertEqual(resp[0].get_json(), {'msg': 'Generic Error'})
            self.assertEqual(resp[1], 500)

    @patch('app.dao.user.find_all', MagicMock(return_value=[user_mock]))
    def test_find_all(self):
        with self.app.app_context():
            resp = user.find_all()
            self.assertEqual(resp[0].get_json(), [self.user_mock])
            self.assertEqual(resp[1], 200)

    @patch('app.dao.user.find_all', MagicMock(return_value=None))
    def test_find_all_empty(self):
        with self.app.app_context():
            resp = user.find_all()
            self.assertEqual(resp[0].get_json(), [])
            self.assertEqual(resp[1], 200)

    @patch('app.dao.user.find_by_id', MagicMock(return_value=user_mock))
    def test_find_by_id(self):
        with self.app.app_context():
            resp = user.find_by_id(id)
            self.assertEqual(resp[0], self.user_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.user.find_by_id', MagicMock(return_value=None))
    def test_find_by_id_not_found(self):
        with self.app.app_context():
            resp = user.find_by_id(id)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)

    @patch('app.dao.user.create', MagicMock(return_value=user_mock))
    def test_create(self):
        with self.app.app_context():
            user.request = MockFlaskRequest(self.user_mock)
            resp = user.create()
            self.assertEqual(resp[0], self.user_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.user.update', MagicMock(return_value=user_mock))
    def test_update(self):
        with self.app.app_context():
            user.request = MockFlaskRequest(self.user_mock)
            resp = user.update(1)
            self.assertEqual(resp[0], self.user_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.user.update', MagicMock(return_value=None))
    def test_update_not_found(self):
        with self.app.app_context():
            user.request = MockFlaskRequest(self.user_mock)
            resp = user.update(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)

    @patch('app.dao.user.delete', MagicMock(return_value=True))
    def test_delete(self):
        with self.app.app_context():
            resp = user.delete(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 204)

    @patch('app.dao.user.delete', MagicMock(return_value=False))
    def test_delete_not_found(self):
        with self.app.app_context():
            resp = user.delete(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)
