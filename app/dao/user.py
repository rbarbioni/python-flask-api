from app.dao import db
from datetime import datetime
from .schema import User


def find_all(session):
    return db.all(session, User)


def find_by_id(session, id):
    return db.query_first(session, User, (User.id == id))


def find_by_email(session, email):
    return db.query_first(session, User, (User.email == email))


def create(session, model):
    email = model['email']
    user = find_by_email(session, email)
    if not user:
        user = User(**model)
        user.created_at = datetime.today()
        db.insert(session, user)
        return find_by_email(session, email)
    raise Exception(400, {'msg': f'user email:{email} already exists'})


def update(session, id, model):
    if find_by_id(session, id):
        model['updated_at'] = datetime.today()
        db.update(session, User, (User.id == id), model)
        return find_by_id(session, id)
    raise Exception(404, {'msg': f'user id:{id} not found'})


def delete(session, id):
    if find_by_id(session, id):
        db.delete(session, User, (User.id == id))
        return True
    raise Exception(404, {'msg': f'user id:{id} not found'})
