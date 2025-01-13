import hmac
import os
from functools import wraps
from typing import Dict, Any
from werkzeug.exceptions import (
    Forbidden,
)
from flask import (
    Response,
    make_response,
    jsonify,
    request,
)


def jsonify_response(
    result: Dict[str, Any],
    status_code: int,
    success: bool = True,
) -> Response:
    result['success'] = success
    return make_response(
        jsonify(result),
        status_code,
    )

def auth_key_required(f):
    """
    Decorator: Check auth key
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        real_signature = request.headers.get('X-Gitea-Signature', '')
        calc_signature = hmac.new(
            key=os.environ['AUTH_KEY'].encode(),
            msg=request.data,
            digestmod='SHA256',
        ).hexdigest()
        if real_signature != calc_signature:
            raise Forbidden(
                'Wrong or empty auth key'
            )
        return f(*args, **kwargs)
    return decorated_function


def get_name_from_payload(
    payload: Dict[str, Any]
) -> str:
    if 'repository' in payload:
        if 'name' in payload['repository']:
            return payload['repository']['name']
    return ''


def get_branch_from_payload(
    payload: Dict[str, Any]
) -> str:
    if 'ref' in payload:
        return payload['ref'].split('/')[-1]
    return ''
