from flask import jsonify
from traceback import format_exc
from app.utils.logger import get_logger
from marshmallow.exceptions import ValidationError


log = get_logger(__name__)


def process_error(error):
    trace = format_exc()
    status = 500

    if isinstance(error, ValidationError):
        status = 400

    log_fields = {'status': status, 'stack_trace': trace}
    args = error.args
    msg = args[0]

    if len(args) > 1:
        status = args[0]
        data = args[1]
        msg = data['msg']
        if type(status) is int and type(data) is dict:
            log_fields.update({'status': status})
            log.error(msg, log_fields)
            return jsonify(data), status

    log.error(msg, log_fields)
    return jsonify({'msg': msg}), status
