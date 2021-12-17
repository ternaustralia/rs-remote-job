import re
import json

from typing import Dict
from jinja2 import Template
from paramiko import SSHClient


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


def load_template_values(cmd_config: Dict[str, any], target: str, query_params: Dict[str, any]) -> Dict[str, any]:
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
    parameters = load_template_parameters(cmd_config["parameters"], query_params)

    command = dict()

    for endpoint in endpoints:
        if endpoint["name"] != target:
            continue

        # Load local parameters
        local_param = load_template_parameters(endpoint["exec"]["parameters"], query_params)

        # Convert the Dict into a json template
        template = json.dumps(endpoint)
        # merge both parameter where local_param will replace global params
        command = json.loads(Template(template).render({** parameters, **local_param}))

    return command

def load_template_parameters(params: list, query_params: Dict[str, any]) -> Dict[str, any]:
    """ Create the render values to match with the template.
        Parameters
        -------------
        params: list

        Return
        -------------
        parameters: Dict[str,any]
    """
    # Check that the query_params are allowed and then replace the defalt value
    allowed_params = [item["name"] for item in params]
    for key in query_params.keys():
        if key not in allowed_params: 
            continue

        for item in params:
            if key != item["name"]:
                continue

            item["default"] = query_params[key]

    parameters = dict()
    for param in params:
        default = param["default"]

        if param["type"] == "int":
            default = int(default)
        elif param["type"] in ("float", "double"): 
            default = float(default)
        elif param["type"] == "bool":
            default = bool(default)

        parameters[param["name"]] = default

    return parameters
