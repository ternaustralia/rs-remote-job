from flask import jsonify, request
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from .blueprint import bp
from .classes.slurm import Slurm
slurm = Slurm('here is the pkey')



@bp.route("/slurm/exists", methods=["GET"])
@require_user
@openapi.validate()
def slurm_users_exists():
    """ Check if user exists in the masternode
        1. Check current acces_token
        2. Connect with paramiko to the master node, if it fails, request new certificate
        3. Check if user exists, if it fails create a new one
    """

    access_token = request.openapi.parameters.query.get("access_token")

    response =  slurm.user_exists()
    return response

@bp.route("/slurm/projects", methods=["GET"])
@require_user
@openapi.validate()
def slurm_projects():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.get_projects() 
    response = jsonify({})
    return response

@bp.route("/slurm/usage", methods=["GET"])
@require_user
@openapi.validate()
def slurm_usage():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.get_usage()
    response = jsonify({})
    return response

@bp.route("/slurm/stopprocess", methods=["GET"])
@require_user
@openapi.validate()
def slurm_stop_process():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.stop_process()
    response = jsonify({})
    return response

@bp.route("/slurm/startserver", methods=["GET"])
@require_user
@openapi.validate()
def slurm_start_server():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.start_server()
    response = jsonify({})
    return response

@bp.route("/slurm/listall", methods=["GET"])
@require_user
@openapi.validate()
def slurm_list_all():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.list_all()
    response = jsonify({})
    return response

@bp.route("/slurm/exechost", methods=["GET"])
@require_user
@openapi.validate()
def slurm_exec_host():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.exec_host()
    response = jsonify({})
    return response

@bp.route("/slurm/running", methods=["GET"])
@require_user
@openapi.validate()
def slurm_running():
    """ Not description yet """

    access_token = request.openapi.parameters.query.get("access_token")

    response = slurm.running() 
    response = jsonify({})
    return response