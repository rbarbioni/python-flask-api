import requests
import json
from uuid import uuid1
from unittest import TestCase
from app.utils.config import get_config


DOMAIN = get_config('TEST_DOMAIN', 'http://localhost:5000')
URL = f'{DOMAIN}/api/v1/product'
HEADERS = {'content-type': 'application/json'}
PRODUCT = {
            'name': 'Product Integration Tests 1',
            'code': str(uuid1())[:8],
            'price': 99.99,
            }


class TestProductIntegration(TestCase):

    def __create_product(self, product=None):
        prod = product
        if product is None:
            prod = PRODUCT.copy()
            prod.update({'code': str(uuid1())[:8]})
        return requests.post(
            URL,
            data=json.dumps(prod),
            headers=HEADERS
        )

    def test_find_products(self):
        resp = requests.get(URL)
        self.assertEqual(resp.status_code, 200)

    def test_find_product_by_id(self):
        resp = self.__create_product()
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp_body['id'])

        product_id = resp.json()['id']
        url = URL + '/' + str(product_id)
        resp = requests.get(url)
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['id'], product_id)

    def test_find_product_by_error_id_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_create_product(self):
        resp = self.__create_product()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json()['id'])

    def test_create_product_error_already_exists_code(self):
        resp = self.__create_product()
        product = resp.json()
        resp = self.__create_product(product)
        error = resp.json()
        code = product['code']
        msg = 'product code:{} already exists'.format(code)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(error['msg'], msg)

    def test_update_product_price(self):
        resp = self.__create_product()
        product = resp.json()
        product_id = product['id']
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(product_id)

        price = 88.88
        product['price'] = price
        url = URL + '/' + str(product_id)
        resp = requests.put(
            url,
            data=json.dumps(product),
            headers=HEADERS
        )

        product = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(product['price'], price)
        self.assertIn('updated_at', product)

    def test_update_product_error_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.put(
            url,
            data=json.dumps(PRODUCT),
            headers=HEADERS
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_product(self):
        resp = self.__create_product()
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp_body['id'])

        product_id = resp.json()['id']
        url = URL + '/' + str(product_id)
        resp = requests.delete(url)
        self.assertEqual(resp.status_code, 204)

    def test_delete_product_error_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.delete(url)
        self.assertEqual(resp.status_code, 404)
