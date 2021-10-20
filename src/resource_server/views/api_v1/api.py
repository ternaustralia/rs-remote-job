from flask import jsonify, request
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from resource_server.views.api_v1.blueprint import bp
from resource_server.views.api_v1.classes.cmd import CMD


@bp.route("/slurm/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def slurm(endpoint):
    cmd = CMD()
    response = cmd.execute(endpoint)
    return jsonify({response})

@bp.route("/vnc/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def vnc(endpoint):
    cmd = CMD()
    response = cmd.execute(endpoint)
    return jsonify({response})

@bp.route("/group/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def group(endpoint):
    cmd = CMD()
    response = cmd.execute(endpoint)
    return jsonify({response})