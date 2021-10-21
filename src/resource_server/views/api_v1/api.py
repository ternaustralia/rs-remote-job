from flask import jsonify, request
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.utils.cmd import execute_command
from resource_server.utils.commond import paramiko_establish_connection


@bp.route("/slurm/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def slurm(endpoint):
    ssh = paramiko_establish_connection()
    response = execute_command(ssh, endpoint)
    return jsonify({response})

@bp.route("/vnc/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def vnc(endpoint):
    ssh = paramiko_establish_connection()
    response = execute_command(ssh, endpoint)
    return jsonify({response})

@bp.route("/group/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def group(endpoint):
    ssh = paramiko_establish_connection()
    response = execute_command(ssh, endpoint)
    return jsonify({response})