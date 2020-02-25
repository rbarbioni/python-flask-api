from alchemy_mock.mocking import AlchemyMagicMock
from unittest import TestCase
from unittest.mock import MagicMock, patch
from app.dao import user


class TestDaoUser(TestCase):

    user_mock = {
        'id': 1,
        'name': 'User 1',
        'email': 'user1@email.com'
    }

    def setUp(self):
        self.session = AlchemyMagicMock()

    @patch('app.dao.db.all', MagicMock(return_value=[]))
    def test_find_all(self):
        users = user.find_all(self.session)
        self.assertEqual(len(users), 0)

    @patch('app.dao.db.query_first', MagicMock(return_value=user_mock))
    def test_find_by_id(self):
        id = 1
        user_find = user.find_by_id(self.session, id)
        self.assertEqual(user_find, self.user_mock)

    @patch('app.dao.db.query_first', MagicMock(return_value=user_mock))
    def test_find_by_email(self):
        email = 'user1@email.com'
        user_find = user.find_by_email(self.session, email)
        self.assertEqual(user_find, self.user_mock)

    @patch('app.dao.db.query_first', MagicMock(side_effect=[None, user_mock]))
    @patch('app.dao.db.insert', MagicMock(return_value=user_mock))
    def test_create(self):
        user_created = user.create(self.session, self.user_mock)
        self.assertEqual(user_created, self.user_mock)

    @patch('app.dao.db.query_first', MagicMock(side_effect=user_mock))
    def test_create_already_exists_error(self):
        try:
            user.create(self.session, self.user_mock)
        except Exception as ex:
            self.assertEqual(ex.args[0], 400)
            self.assertEqual(ex.args[1]['msg'], 'user email:user1@email.com already exists')

    @patch('app.dao.db.update', MagicMock(return_value=user_mock))
    def test_update(self):
        user_create_update = self.user_mock.copy()
        user_create_update['price'] = 88.88
        with patch('app.dao.db.query_first',
                   MagicMock(side_effect=[self.user_mock, user_create_update])):

            user_create_update = user.update(self.session, 1, user_create_update)
            self.assertEqual(user_create_update['price'], 88.88)

    @patch('app.dao.db.query_first', MagicMock(return_value=None))
    def test_update_not_found(self):
        try:
            user.update(self.session, 1, self.user_mock)
        except Exception as ex:
            self.assertEqual(ex.args[0], 404)
            self.assertEqual(ex.args[1]['msg'], 'user id:1 not found')

    @patch('app.dao.db.query_first', MagicMock(return_value=user_mock))
    @patch('app.dao.db.delete', MagicMock(return_value=True))
    def test_delete(self):
        user_deleted = user.delete(self.session, 1)
        self.assertTrue(user_deleted)

    @patch('app.dao.db.query_first', MagicMock(return_value=None))
    def test_delete_not_found(self):
        try:
            user.delete(self.session, 1)
        except Exception as ex:
            self.assertEqual(ex.args[0], 404)
            self.assertEqual(ex.args[1]['msg'], 'user id:1 not found')