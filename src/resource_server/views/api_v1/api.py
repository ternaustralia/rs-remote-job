from flask import jsonify, request
from flask_tern import openapi
from flask_tern.auth import current_user, require_user

from .blueprint import bp
from .classes.slurm import Slurm
slurm = Slurm('here is the pkey')


@bp.route("/slurm/<endpoint>", methods=["GET"])
@require_user
@openapi.validate()
def slurm(endpoint):
    """ Check if user exists in the masternode
        1. Check current acces_token
        2. Connect with paramiko to the master node, if it fails, request new certificate
        3. Check if user exists, if it fails create a new one
    """

    response =  slurm.execute(endpoint)
    return response
