## Usage
The "resource server" is the service that talks to the HPC. It can mint SSH certificates
to impersonate any (non-operator) user.


The resource server provides several endpoints:

- `/api/execute/{endpoint}`
- `/api/configuration`

The only one ever used by the portals is `/api/execute/{endpoint}`. `endpoint` is defined in configuration

## Configuration

Tasks are defined via a separate JSON configuration file. See the short example below.
```json
{
    "parameters": [
        {"name": "login", "type": "string", "default": ""},
        {"name": "var2","type": "int", "default": 1}    
    ],
    "endpoints": [
        {
            "name": "example1",
            "async": false,
            "httpMethod": "POST", 
            "exec": {
                "parameters":[
                    {"name": "param1", "type": "int", "default": 1},
                    {"name": "param2", "type": "string", "default": ""}
                ],
                "command": "/path/to/binary {param1} {param2} {var2}"
            },
            "output": {
                "type": "regex/string",
                "value": "(?P<name>[a-zA-Z0-9_]+),(?P<type>[a-zA-Z0-9_]+),(?P<jsonconfig>.*),(?P<amqpuri>.*),(?P<amqpcert>.*),(?P<amqpnoverifypeer>.*),(?P<amqpnoverifyhost>.*),(?P<uri>.*),(?P<cert>.*),(?P<noverifypeer>.*),(?P<noverifyhost>.*)",
            },
            "requireMatch": true,
            "failFatal": true,
            "formatFatal": false,
            "host": "{login}"
        }
    ]
}
```
### Defining Endpoints
Endpoints are defined in the `endpoints` section of the json config. 

Each endpoint needs the following values:
* **name** this will turn into the name of the endpoint
* **async** whether this is asynchronous API
* **httpMethod** the http method of this endpint. This will define how the parameters are passed to this endpoint
* **exec** command to execute. Parameters need to be substituted. 
* **output** the contents of the response. If output type is `string`, exec is ignored
* **requireMatch** if true, `command` in `exec` needs to have exact parameters defined for the endpoint
* **failFatal** if true, return server error code (500 range) when command fails
* **formatFatal** if true, return server error code (500 range code) if output does not match regex
* **host** the host to execute this command 
## Request and Response

Responses are of the format:
```json
{
  "userMessages": [
    "error1",
    "error2"
  ],
  "commandResult": [
    {
      "match0": "value",
      "match1": "value"
    },
    {
      "match0": "value2",
      "match1": "value2"
    }
  ]
}
```

`userMessages` is a list of error strings that should be displayed to the user.
`commandResult` is a list of objects containing the matched fields in the regex.
