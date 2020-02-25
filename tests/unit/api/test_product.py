from flask import Flask
from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app.api import product


class MockFlaskRequest():

    def __init__(self, json):
        self.json = json

    def get_json(self):
        return self.json


class TestProduct(TestCase):

    app = Flask(__name__)
    product_mock = {
                'id': 1,
                'price': 99.99,
                'code': '1',
                'name': 'Product 1'
            }

    def setUp(self):
        product.create_context = AlchemyMagicMock()

    def test_error_handler(self):
        with self.app.app_context():
            resp = product.error_handler(Exception('Generic Error'))
            self.assertEqual(resp[0].get_json(), {'msg': 'Generic Error'})
            self.assertEqual(resp[1], 500)

    @patch('app.dao.product.find_all', MagicMock(return_value=[product_mock]))
    def test_find_all(self):
        with self.app.app_context():
            resp = product.find_all()
            self.assertEqual(resp[0].get_json(), [self.product_mock])
            self.assertEqual(resp[1], 200)

    @patch('app.dao.product.find_all', MagicMock(return_value=None))
    def test_find_all_empty(self):
        with self.app.app_context():
            resp = product.find_all()
            self.assertEqual(resp[0].get_json(), [])
            self.assertEqual(resp[1], 200)

    @patch('app.dao.product.find_by_id', MagicMock(return_value=product_mock))
    def test_find_by_id(self):
        with self.app.app_context():
            resp = product.find_by_id(id)
            self.assertEqual(resp[0], self.product_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.product.find_by_id', MagicMock(return_value=None))
    def test_find_by_id_not_found(self):
        with self.app.app_context():
            resp = product.find_by_id(id)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)

    @patch('app.dao.product.create', MagicMock(return_value=product_mock))
    def test_create(self):
        with self.app.app_context():
            product.request = MockFlaskRequest(self.product_mock)
            resp = product.create()
            self.assertEqual(resp[0], self.product_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.product.update', MagicMock(return_value=product_mock))
    def test_update(self):
        with self.app.app_context():
            product.request = MockFlaskRequest(self.product_mock)
            resp = product.update(1)
            self.assertEqual(resp[0], self.product_mock)
            self.assertEqual(resp[1], 200)

    @patch('app.dao.product.update', MagicMock(return_value=None))
    def test_update_not_found(self):
        with self.app.app_context():
            product.request = MockFlaskRequest(self.product_mock)
            resp = product.update(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)

    @patch('app.dao.product.delete', MagicMock(return_value=True))
    def test_delete(self):
        with self.app.app_context():
            resp = product.delete(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 204)

    @patch('app.dao.product.delete', MagicMock(return_value=False))
    def test_delete_not_found(self):
        with self.app.app_context():
            resp = product.delete(1)
            self.assertEqual(resp[0], '')
            self.assertEqual(resp[1], 404)
