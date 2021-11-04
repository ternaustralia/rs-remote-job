import re
import json
from types import coroutine
from typing import Dict
from paramiko import SSHClient
from jinja2 import Template

from resource_server.utils.common import read_json_file


def execute_command(ssh: SSHClient, endpoint: str, method: str) -> Dict[str, any]: 
    """ Run the specific command and then check for the result """

    command = load_template_values(endpoint)

    if method != command["httpMethod"]:
        raise Exception("The http-method does not match with the schema, please check your request")

    cmd = command["exec"]["command"]

    stdin, stdout, stderr = ssh.exec_command(cmd.get('cmd'))
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

def load_template_values(target: str) -> Dict[str, any]:
    """ Instance the command to be a candidate to run.
        Parameters
        -------------
        targe: str

        Return
        -------------
        command: Dict[str,any]
    """
    jsonfile = read_json_file()
    endpoints = jsonfile['endpoints']
    parameters = load_template_parameters(jsonfile["parameters"]) 
    command = dict()

    for endpoint in endpoints:
        if endpoint["name"] != target:
            continue

        # Load local parameters
        local_param = load_template_parameters(endpoint["exec"]["parameters"])

        # Load global parameters
        template = json.dumps(endpoint)
        # merge both parameter where local_param will replace global params
        command = json.loads(Template(template).render(parameters | local_param))    

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
        elif param["type"] == "double":
            default = float(default)
        elif param["type"] == "bool":
            default = bool(default)

        parameters[param["name"]] = default 

    return parameters
