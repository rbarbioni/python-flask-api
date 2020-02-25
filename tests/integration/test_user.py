import requests
import json
from uuid import uuid1
from unittest import TestCase


URL = 'http://localhost:5000/api/v1/user'
HEADERS = {'content-type': 'application/json'}
USER = {
            'name': 'User Integration Tests 1',
            'email': str(uuid1())[:8] + '@email.com'
            }


class TestuserIntegration(TestCase):

    def __create_user(self, user=None):
        body = user
        if user is None:
            body = USER.copy()
            body.update({'email': str(uuid1())[:8] + '@email.com'})
        return requests.post(
            URL,
            data=json.dumps(body),
            headers=HEADERS
        )

    def test_find_users(self):
        resp = requests.get(URL)
        self.assertEqual(resp.status_code, 200)

    def test_find_user_by_id(self):
        resp = self.__create_user()
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp_body['id'])

        user_id = resp.json()['id']
        url = URL + '/' + str(user_id)
        resp = requests.get(url)
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_body['id'], user_id)

    def test_find_user_by_error_id_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_create_user(self):
        resp = self.__create_user()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp.json()['id'])

    def test_create_user_error_already_exists_email(self):
        resp = self.__create_user()
        user = resp.json()
        resp = self.__create_user(user)
        error = resp.json()
        email = user['email']
        msg = 'user email:{} already exists'.format(email)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(error['msg'], msg)

    def test_update_user_price(self):
        resp = self.__create_user()
        user = resp.json()
        user_id = user['id']
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(user_id)

        name = 'User Name Updated'
        user['name'] = name
        url = URL + '/' + str(user_id)
        resp = requests.put(
            url,
            data=json.dumps(user),
            headers=HEADERS
        )

        user = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(user['name'], name)
        self.assertIn('updated_at', user)

    def test_update_user_error_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.put(
            url,
            data=json.dumps(USER),
            headers=HEADERS
        )
        self.assertEqual(resp.status_code, 404)

    def test_delete_user(self):
        resp = self.__create_user()
        resp_body = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIsNotNone(resp_body['id'])

        user_id = resp.json()['id']
        url = URL + '/' + str(user_id)
        resp = requests.delete(url)
        self.assertEqual(resp.status_code, 204)

    def test_delete_user_error_not_found(self):
        url = URL + '/' + str('999999')
        resp = requests.delete(url)
        self.assertEqual(resp.status_code, 404)
