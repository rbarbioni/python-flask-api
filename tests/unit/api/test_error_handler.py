from flask import Flask
from unittest import TestCase
from app.api import error_handler
from marshmallow.exceptions import ValidationError


class TestErrorHandler(TestCase):

    app = Flask(__name__)

    def test_process_handler_generic_exception(self):
        with self.app.app_context():
            ex = Exception('General Error')
            resp = error_handler.process_error(ex)
            body = resp[0].get_json()
            status = resp[1]
            self.assertEqual(body, {'msg': 'General Error'})
            self.assertEqual(status, 500)

    def test_process_http_status_exception(self):
        with self.app.app_context():
            ex = Exception(404, {'msg': 'Not Found'})
            resp = error_handler.process_error(ex)
            body = resp[0].get_json()
            status = resp[1]
            self.assertEqual(body, {'msg': 'Not Found'})
            self.assertEqual(status, 404)

    def test_process_validation_exception(self):
        with self.app.app_context():
            ex = ValidationError('Validation Error')
            resp = error_handler.process_error(ex)
            body = resp[0].get_json()
            status = resp[1]
            self.assertEqual(body, {'msg': 'Validation Error'})
            self.assertEqual(status, 400)
