import re
import json, yaml
from jsonschema import validate
from typing import Dict, List
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


def _convert(obj, otype):
    # convert the object to the type specified
    if obj is None:
        return None
    if otype == "integer":
        return int(obj)
    elif otype == "number":
        return float(obj)
    elif otype == "boolean":
        if obj in ['true', 'True', 1, True]:
            return True
        if obj in ['false', 'False', 0, False]:
            return False
        raise Exception(f"Invalid boolean value {obj} ")
    return str(obj)


def get_command(cmd: str, qparams: Dict[str, any], config: Dict[str, any]) -> Dict[str, any]:
    """ Return the command with all its parameters and associated values set.
        Parameters:
        cmd: the command to be executed
        qparams: parameters to the command
        config: configuration settings from the yaml config file 

        Return
        -------------
        command: Dict[str,any]
    """
    command = dict()
    for cmditem in config['endpoints']:
        if cmditem['name'] == cmd:
            params = get_parameters(cmd, qparams, cmditem)
            command = json.loads(Template(json.dumps(cmditem)).render(params))
            break
    return command


def get_parameters(cmd: str, params: Dict[str, any], cmditem: Dict[str, any]) -> Dict[str, any]:
    """ Validate the command's parameters against the command configuration,
        and return all the parameters required for the command.
    """

    # Get all the command parameters, and fill it with default values if not specified
    parameters = dict()
    cmd_pnames = [ p['name'] for p in cmditem['parameters'] ]
    for p in cmditem['parameters']:
        pname = p['name']
        schema = p['schema']

        # validate against the parameter's schema
        try:
            parameters[pname] = _convert(params.get(pname, schema.get('default')), schema['type'])
            validate(parameters[pname], schema)
        except Exception as e:
            raise Exception(f"Invalid parameter '{pname} ({parameters[pname]}): {str(e)}")

        # Command parameter must have value
        if pname in cmd_pnames and parameters[pname] is None:
            raise Exception(f"Missing parameter '{pname}' for command {cmd}")

    return parameters