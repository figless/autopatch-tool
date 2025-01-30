import json
from flask import (
    Response,
    Flask,
    request,
)
from werkzeug.exceptions import (
    InternalServerError,
)

from tools.logger import logger
from debranding import apply_modifications
from tools.webserv_tools import (
    auth_key_required,
    jsonify_response,
    get_name_from_payload,
    get_branch_from_payload,
)
import tools.slack

app = Flask('almalinux-debranding-tool')

HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400

@app.route(
    '/debrand_packages',
    methods=('POST',),
)
@auth_key_required
def debrand_packages():
    try:
        logger.debug(json.dumps(request.json, indent=4))
        if 'commits' not in request.json:
            return jsonify_response(
                result={
                    'message': 'Nothing to sync, because commits are absent',
                },
                status_code=HTTP_200_OK,
                success=True,
            )

        repo_name = get_name_from_payload(request.json)
        branch = get_branch_from_payload(request.json)

        if not repo_name or not branch:
            return jsonify_response(
                result={
                    'message': f'Nothing to sync, because repository name or branch are absent in payload',
                    'details': f'repo name - {repo_name}, branch - {branch}'
                },
                status_code=HTTP_400_BAD_REQUEST,
                success=False,
            )

        message = apply_modifications(repo_name, branch)
        logger.info(message)
        tools.slack.success_message(repo_name, branch)

        return jsonify_response(
            result={
                'message': message,
            },
            status_code=HTTP_200_OK,
        )
    except Exception as err:
        logger.error(err)
        tools.slack.failed_message(repo_name, branch, str(err))


@app.errorhandler(InternalServerError)
def handle_internal_server_error(
    error: InternalServerError
) -> Response:
    logger.exception(error)
    return jsonify_response(
        result={
            'message': 'Internal server error',
            'details': str(error),
        },
        status_code=error.code,
    )

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080,
    )
