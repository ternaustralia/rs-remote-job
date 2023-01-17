import logging
from flask import current_app, jsonify, request, abort
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.utils.cmd import execute_command, get_command
from resource_server.utils.common import paramiko_establish_connection


log = logging.getLogger(__name__)


@bp.route("/cmd/<endpoint>", methods=["GET", "POST"])
@require_user
@openapi.validate()
def cmd(endpoint):

    path_file = current_app.config["CMD_PATH_FILE"]
    base_url = current_app.config["SSH_KEYSIGN_BASE_URL"]
    user = current_user.claims[current_app.config["SSH_PRINCIPAL_CLAIM"]]

    params = dict()
    if request.method == 'POST':
        params = request.json
    elif request.method == 'GET':
        params = request.args 

    command = get_command(endpoint, params, path_file)
    if not command:
        abort(400, description=f"{endpoint} is not supported!")
    if command.get('httpMethod') != request.method:
        abort(400, description=f"method '{request.method}' for {endpoint} is not supported!")

    log.info(f"Command issued: {command['exec']['command']}")
    headers = {
        "Authorization": request.headers.get("Authorization"),
    }

    ssh = paramiko_establish_connection(base_url, user, command["host"], command["port"], headers)
    response = execute_command(ssh, command, request.method)
    return jsonify(response)
