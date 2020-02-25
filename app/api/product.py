from flask import Blueprint, request, jsonify
from app.dao import product as db
from app.dao.context import create_context
from .serializers import ProductSchema
from .constants import GET, POST, PUT, DELETE, COUNTER
from .error_handler import process_error


RESOURCE = 'product'
PATH = f'/api/v1/{RESOURCE}'

schema = ProductSchema()
api = Blueprint(RESOURCE, __name__, url_prefix=PATH)


@api.errorhandler(Exception)
def error_handler(error):
    return process_error(error)


@api.route('/', methods=[GET])
def find_all():
    """return list of Product
    ---
    tags:
      - Product
    responses:
      200:
        description: A list Products
        schema:
          id: ProductResponse
          properties:
            id:
              type: integer
            code:
              type: string
            name:
              type: string
            price:
              type: number
    """
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
    """create new Product
    ---
    tags:
      - Product
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: ProductRequest
          required:
            - name
            - code
            - price
          properties:
            name:
              type: string
            code:
              type: string
            price:
              type: number
    responses:
      201:
        description: Created new Product
        schema:
          $ref: '#/definitions/ProductResponse'
      400:
        description: Invalid any property
        schema:
          id: ErrorResponse
          properties:
            msg:
              type: string
    """
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
    """Return a Product by id
    ---
    tags:
      - Product
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: One Product by id
        schema:
          $ref: '#/definitions/ProductResponse'
      400:
        description: Invalid any Product property
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Product not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    COUNTER.labels(GET, PATH.join(f'/{id}')).inc()
    with create_context() as context:
        session = context['session']
        model = db.find_by_id(session, id)
        if model:
            return schema.dump(model), 200
        return '', 404


@api.route('/<int:id>', methods=[PUT])
def update(id):
    """Update a existing Product
    ---
    tags:
      - Product
    parameters:
      - name: id
        in: path
        required: true
        type: integer
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/ProductRequest'
    responses:
      201:
        description: Created new Product
        schema:
          $ref: '#/definitions/ProductResponse'
      400:
        description: Invalid any Product property
        schema:
          $ref: '#/definitions/ErrorResponse'
      404:
        description: Product not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
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
    """Remove on existing Product
    ---
    tags:
      - Product
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Product deleted
      404:
        description: Product not found
        schema:
          $ref: '#/definitions/ErrorResponse'
    """
    COUNTER.labels(DELETE, PATH.join(f'/{id}')).inc()
    with create_context() as context:
        session = context['session']
        model = db.delete(session, id)
        if model:
            return '', 204
        return '', 404
