def all(session, Model):
    return session.query(Model).all()


def query(session, Model, filter):
    return session.query(Model).filter(filter)


def query_first(session, Model, filter):
    return session.query(Model).filter(filter).first()


def query_all(session, Model, filter):
    return session.query(Model).filter(filter).all()


def insert(session, model):
    return session.add(model)


def update(session, Model, filter, model):
    return session.query(Model).filter(filter).update(model)


def delete(session, Model, filter):
    return session.query(Model).filter(filter).delete()
