from prometheus_client import generate_latest
from flask import Response, Blueprint
from .constants import GET, COUNTER


RESOURCE = 'metrics'
PATH = f'/api/v1/{RESOURCE}'
api = Blueprint(RESOURCE, __name__, url_prefix=PATH)


@api.route('/', methods=[GET])
def get():
    COUNTER.labels(GET, PATH).inc()
    return Response(generate_latest(),
                    mimetype=str('text/plain; charset=utf-8'))
