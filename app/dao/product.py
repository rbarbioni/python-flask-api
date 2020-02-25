from app.dao import db
from datetime import datetime
from .schema import Product


def find_all(session):
    return db.all(session, Product)


def find_by_id(session, id):
    return db.query_first(session, Product, (Product.id == id))


def find_by_code(session, code):
    return db.query_first(session, Product, (Product.code == code))


def create(session, model):
    code = model['code']
    product = find_by_code(session, code)
    if not product:
        product = Product(**model)
        product.created_at = datetime.today()
        db.insert(session, product)
        return find_by_code(session, code)
    raise Exception(400, {'msg': f'product code:{code} already exists'})


def update(session, id, model):
    if find_by_id(session, id):
        model['updated_at'] = datetime.today()
        db.update(session, Product, (Product.id == id), model)
        return find_by_id(session, id)
    raise Exception(404, {'msg': f'product id:{id} not found'})


def delete(session, id):
    if find_by_id(session, id):
        db.delete(session, Product, (Product.id == id))
        return True
    raise Exception(404, {'msg': f'product id:{id} not found'})
