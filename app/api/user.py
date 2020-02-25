from flask import Blueprint, request, jsonify
from app.dao import user as db
from app.dao.context import create_context
from app.utils.logger import get_logger
from .constants import GET, POST, PUT, DELETE, COUNTER
from .error_handler import process_error
from .serializers import UserSchema


RESOURCE = 'user'
PATH = f'/api/v1/{RESOURCE}'

schema = UserSchema()
api = Blueprint(RESOURCE, __name__, url_prefix=PATH)
log = get_logger(__name__)


@api.errorhandler(Exception)
def error_handler(error):
    return process_error(error)


@api.route('/', methods=[GET])
def find_all():
    """return list of User
    ---
    tags:
      - User
    responses:
      200:
        description: A list users
        schema:
          id: UserResponse
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string

    """
    log.debug(f'GET {PATH}')
    COUNTER.labels(GET, PATH).inc()
    with create_context() as context:
        session = context['session']
        results = db.find_all(session)
        if results:
            results = jsonify([schema.dump(u) for u in results])
            return results, 200
        return jsonify([]), 200


@api.route('/', methods=[POST])
def create():
    """create new User
    ---
    tags:
      - User
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: UserRequest
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: Created new User
        schema:
          $ref: '#/definitions/UserResponse'
      400:
        description: Invalid any property
        schema:
          id: ErrorResponse
          properties:
            msg:
              type: string
    """
    log.debug(f'POST {PATH}')
    COUNTER.labels(POST, PATH).inc()
    body = request.get_json()
    schema.load(body)
    with create_context() as context:
        session = context['session']
        product = db.create(session, body)
        result = schema.dump(product)
        return result, 200


@api.route('/<int:id>', methods=[GET])
def find_by_id(id):
    """Return a User by id
    ---
    tags:
      - User
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: One User by id
        schema:
          $ref: '#/definitions/UserResponse'
      400:
        description: Invalid any User property
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: User not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    log.debug(f'GET {PATH}/{id}')
    COUNTER.labels(GET, PATH.join(f'/{id}')).inc()
    with create_context() as context:
        session = context['session']
        model = db.find_by_id(session, id)
        if model:
            return schema.dump(model), 200
        return '', 404


@api.route('/<int:id>', methods=[PUT])
def update(id):
    """Update a existing User
    ---
    tags:
      - User
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/UserRequest'
    responses:
      201:
        description: Created new User
        schema:
          $ref: '#/definitions/UserResponse'
      400:
        description: Invalid any User property
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: User not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    log.debug(f'PUT {PATH}/{id}')
    COUNTER.labels(PUT, PATH.join(f'/{id}')).inc()
    body = request.get_json()
    schema.load(body)
    with create_context() as context:
        session = context['session']
        model = db.update(session, id, body)
        if model:
            return schema.dump(model), 200
        return '', 404


@api.route('/<int:id>', methods=[DELETE])
def delete(id):
    """Remove on existing User
    ---
    tags:
      - User
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: User deleted
      404:
        description: User not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    log.debug(f'DELETE {PATH}/{id}')
    COUNTER.labels(DELETE, PATH.join(f'/{id}')).inc()
    with create_context() as context:
        session = context['session']
        model = db.delete(session, id)
        if model:
            return '', 204
        return '', 404
