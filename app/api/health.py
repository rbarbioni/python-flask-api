
from flask import Blueprint
from .constants import GET, COUNTER

RESOURCE = 'health'
PATH = f'/api/v1/{RESOURCE}'
api = Blueprint(RESOURCE, __name__, url_prefix=PATH)


@api.route('/', methods=[GET])
def get():
    COUNTER.labels(GET, PATH).inc()
    return {'status': 'ok'}
