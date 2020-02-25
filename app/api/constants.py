from prometheus_client import Counter


GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
COUNTER = Counter('Api', 'Requests', ['method', 'path'])

HTTP_STATUS = {
    'OK': 200,
    'CREATED': 201,
    'NO_CONTENT': 204,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
}
