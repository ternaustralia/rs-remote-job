from flask import jsonify, request
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.utils.cmd import execute_command
from resource_server.utils.commond import paramiko_establish_connection


@bp.route("/cmd/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def cmd(endpoint):
    ssh = paramiko_establish_connection()
    response = execute_command(ssh, endpoint)
    return jsonify({response})
