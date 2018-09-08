from flask import jsonify

from mocksi.api import api


def _resp(error, message):
    response = jsonify(
        {
            'code': str(error),
            'message': str(message)
        }
    )
    return response


def bad_request(msg):
    response = _resp('bad_request', msg)
    response.status_code = 400
    return response


def not_found(msg):
    response = _resp('not_found', msg)
    response.status_code = 404
    return response


def internal_error(msg):
    response = _resp('internal_error', msg)
    response.status_code = 500
    return response


def service_unavailable(msg):
    response = _resp('service_unavailable', msg)
    response.status_code = 503
    return response


@api.errorhandler(Exception)
def error(e):
    return internal_error(e)
