import yaml
import logging
from flask import current_app, jsonify, request, abort
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.utils.cmd import execute_command, get_command
from resource_server.utils.common import paramiko_establish_connection


log = logging.getLogger(__name__)


def get_principal(data):
    # Get the principals. For service role, this is the username passed in as
    # parameter. Otherwise this is extracted from the user attribute.
    if current_user.has_role('service') and data.get("username") is not None:
        principals = data.get("username")
    else:
        principals = current_user.claims[current_app.config["SSH_PRINCIPAL_CLAIM"]]
    if not principals:
        source = "username" if current_user.has_role("service") else f"user attribute '{current_app.config['SSH_PRINCIPAL_CLAIM']}'"
        abort(400, description=f"{source} cannot be empty")
    return principals


@bp.route("/cmd/<endpoint>", methods=["GET", "POST"])
@require_user
@openapi.validate()
def cmd(endpoint):
    def _get_config_value(pname, config):
        for item in config:
            if item['name'] == pname:
                return item['default']

    path_file = current_app.config["CMD_PATH_FILE"]
    base_url = current_app.config["SSH_KEYSIGN_BASE_URL"]

    params = dict()
    if request.method == 'POST':
        params = request.json
    elif request.method == 'GET':
        params = request.args

    # Get the username from parameters passed in or token claim
    user = get_principal(params)

    with open(path_file, 'r') as f1:
        cmd_config = yaml.safe_load(f1)

    command = get_command(endpoint, params, cmd_config)
    if not command:
        abort(400, description=f"{endpoint} is not supported!")
    if command.get('httpMethod') != request.method:
        abort(400, description=f"method '{request.method}' for {endpoint} is not supported!")

    log.info(f"Command issued: {command['exec']['command']}")

    host = _get_config_value("ssh_host", cmd_config["config"])
    port = _get_config_value("ssh_port", cmd_config["config"])
    ssh = paramiko_establish_connection(base_url, user, host, port)
    response = execute_command(ssh, command, request.method)
    return jsonify(response)