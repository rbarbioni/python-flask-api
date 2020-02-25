from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app.dao import product


class TestDaoProduct(TestCase):

    product_mock = {
        'id': 1,
        'code': '1',
        'name': 'Product 1',
        'price': 99.99
    }

    def setUp(self):
        self.session = AlchemyMagicMock()

    @patch('app.dao.db.all', MagicMock(return_value=[]))
    def test_find_all(self):
        products = product.find_all(self.session)
        self.assertEqual(len(products), 0)

    @patch('app.dao.db.query_first', MagicMock(return_value=product_mock))
    def test_find_by_id(self):
        id = 1
        product_find = product.find_by_id(self.session, id)
        self.assertEqual(product_find, self.product_mock)

    @patch('app.dao.db.query_first', MagicMock(return_value=product_mock))
    def test_find_by_code(self):
        code = '1'
        product_find = product.find_by_code(self.session, code)
        self.assertEqual(product_find, self.product_mock)

    @patch('app.dao.db.query_first', MagicMock(side_effect=[None, product_mock]))
    @patch('app.dao.db.insert', MagicMock(return_value=product_mock))
    def test_create(self):
        product_created = product.create(self.session, self.product_mock)
        self.assertEqual(product_created, self.product_mock)

    @patch('app.dao.db.query_first', MagicMock(side_effect=product_mock))
    def test_create_already_exists_error(self):
        try:
            product.create(self.session, self.product_mock)
        except Exception as ex:
            self.assertEqual(ex.args[0], 400)
            self.assertEqual(ex.args[1]['msg'], 'product code:1 already exists')

    @patch('app.dao.db.update', MagicMock(return_value=product_mock))
    def test_update(self):
        product_create_update = self.product_mock.copy()
        product_create_update['price'] = 88.88
        with patch('app.dao.db.query_first',
                   MagicMock(side_effect=[self.product_mock, product_create_update])):

            product_create_update = product.update(self.session, 1, product_create_update)
            self.assertEqual(product_create_update['price'], 88.88)

    @patch('app.dao.db.query_first', MagicMock(return_value=None))
    def test_update_not_found(self):
        try:
            product.update(self.session, 1, self.product_mock)
        except Exception as ex:
            self.assertEqual(ex.args[0], 404)
            self.assertEqual(ex.args[1]['msg'], 'product id:1 not found')

    @patch('app.dao.db.query_first', MagicMock(return_value=product_mock))
    @patch('app.dao.db.delete', MagicMock(return_value=True))
    def test_delete(self):
        product_deleted = product.delete(self.session, 1)
        self.assertTrue(product_deleted)

    @patch('app.dao.db.query_first', MagicMock(return_value=None))
    def test_delete_not_found(self):
        try:
            product.delete(self.session, 1)
        except Exception as ex:
            self.assertEqual(ex.args[0], 404)
            self.assertEqual(ex.args[1]['msg'], 'product id:1 not found')
