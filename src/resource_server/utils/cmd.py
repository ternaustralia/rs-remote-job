import re
import json

from typing import Dict
from jinja2 import Template
from paramiko import SSHClient

from resource_server.utils.common import create_request_param_to_config


def execute_command(ssh: SSHClient, command: Dict[str, any], method: str) -> Dict[str, any]:
    """ Run the specific command and then check for the result """

    if method != command["httpMethod"]:
        raise Exception("The http-method does not match with the schema, please check your request")

    cmd = command["exec"]["command"]

    stdin, stdout, stderr = ssh.exec_command(cmd)
    lines = stdout.readlines()

    # Return any error
    if not stderr.channel.exit_status_ready():
        return {
            "code": 500,
            "message": f"[INFO] {' '.join(lines)}"
        }

    # Return lines if not regex ouput
    if not command["output"].get("value"):
        return {
            "code": 200,
            "message": tuple(lines),
        }

    # Return lines if and match regex output
    result = re.search(command["output"]["value"], " ".join(lines), re.IGNORECASE)
    return {
        "code": 200,
        "message": result.groups() if result else (),
    }


def load_template_values(cmd_config: Dict[str, any], target: str, params: Dict[str, any]) -> Dict[str, any]:
    """ Instance the command to be a candidate to run.
        Parameters
        -------------
        cmd_config: dict
        targe: str
        param: list

        Return
        -------------
        command: Dict[str,any]
    """
    endpoints = cmd_config['endpoints']
    # Load global parameters
    parameters = load_template_parameters(cmd_config["parameters"])

    # Filter and validate request query parameters
    query_params = dict()
    for key in params.keys():
        if key not in cmd_config.get("allowed_query_params", list()): 
            continue
        query_params[key] = params[key]

    # Load the correct format and structure to run it in jinja
    request_params = load_template_parameters(create_request_param_to_config(query_params)) 
    command = dict()

    for endpoint in endpoints:
        if endpoint["name"] != target:
            continue

        # Load local parameters
        local_param = load_template_parameters(endpoint["exec"]["parameters"])

        # Convert the Dict into a json template
        template = json.dumps(endpoint)
        # merge both parameter where local_param will replace global params
        command = json.loads(Template(template).render({** parameters, **local_param, **request_params}))

    return command

def load_template_parameters(params: list) -> Dict[str, any]:
    """ Create the render values to match with the template.
        Parameters
        -------------
        params: list

        Return
        -------------
        parameters: Dict[str,any]
    """
    parameters = dict()
    for param in params:
        default = param["default"]

        if param["type"] == "int":
            default = int(default)
        elif param["type"] == "float" or param["type"] == "double":
            default = float(default)
        elif param["type"] == "bool":
            default = bool(default)

        parameters[param["name"]] = default

    return parameters
