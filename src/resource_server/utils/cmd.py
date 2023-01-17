import re
import json
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
    if otype == "int":
        return int(obj)
    elif otype in ("float", "double"):
        return float(obj)
    elif otype == "bool":
        if obj in ['true', 'True', 1, True]:
            return True
        if obj in ['false', 'False', 0, False]:
            return False
        raise Exception(f"Invalid boolean value {obj} ")
    return str(obj)


def get_command(cmd: str, qparams: Dict[str, any], config_file:str) -> Dict[str, any]:
    """ Return the command with all its parameters and associated values set.
        Parameters:
        cmd: the command to be executed
        qparams: parameters to the command
        config_file: path to command configuration file

        Return
        -------------
        command: Dict[str,any]
    """
    with open(config_file, 'r') as f1:
        cmd_config = json.load(f1)

    command = dict()
    for cmditem in cmd_config['endpoints']:
        if cmditem['name'] == cmd:
            params = get_parameters(cmd, qparams, cmditem, cmd_config['parameters'])
            command = json.loads(Template(json.dumps(cmditem)).render(params))
            break
    return command


def get_parameters(cmd: str, params: Dict[str, any], cmditem: Dict[str, any], gparams: List) -> Dict[str, any]:
    """ Validate the command's parameters against the command configuration,
        and return all the parameters required for the command.
    """

    # Get all the command parameters, and fill it with default values if not specified
    parameters = dict()
    cmd_pnames = [ p['name'] for p in cmditem['exec']['parameters'] ]
    for p in cmditem['exec']['parameters'] + gparams:
        pname = p['name']
        parameters[pname] = _convert(params.get(pname, p.get('default')), p['type'])

        # Command parameter must have value
        if pname in cmd_pnames and parameters[pname] is None:
            raise Exception(f"Missing parameter '{pname}' for command {cmd}")

    return parameters