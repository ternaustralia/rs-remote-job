from flask import jsonify, request
from flask.globals import current_app
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.utils.cmd import execute_command, load_template_values
from resource_server.utils.common import paramiko_establish_connection, validate_schema


@bp.route("/cmd/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def cmd(endpoint):
    path_file = current_app.config["CMD_PATH_FILE"]
    user = current_user.claims[current_app.config["SSH_PRINCIPAL_CLAIM"]]

    # If the schema validator does raise any error then load the right endpoint values
    command = load_template_values(validate_schema(path_file), endpoint)

    ssh = paramiko_establish_connection(user, command["host"], command["port"])
    response = execute_command(ssh, command, "GET")
    return jsonify(response)

@bp.route("/cmd/<endpoint>", methods=["POST"])
@require_user
@openapi.validate()
def cmd_post(endpoint):
    path_file = current_app.config["CMD_PATH_FILE"]
    user = current_user.claims[current_app.config["SSH_PRINCIPAL_CLAIM"]]

    # If the schema validator does raise any error then load the right endpoint values
    command = load_template_values(validate_schema(path_file), endpoint)

    ssh = paramiko_establish_connection(user, command["host"], command["port"])
    response = execute_command(ssh, endpoint, "POST")
    return jsonify(response)
