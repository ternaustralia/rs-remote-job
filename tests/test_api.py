def test_no_auth(client):
    response = client.post(
        "/api/v1.0/cmd/test_command",
    )
    assert response.status_code == 403

def test_no_auth_get(client):
    response = client.get(
        "/api/v1.0/cmd/test_command",
    )
    assert response.status_code == 403


def test_cmd_test_command(client, basic_auth, mock_post_request, ssh_server, test_command):
    # generate a key pair
    response = client.get(
        f"/api/v1.0/cmd/{test_command}?ssh_port={ssh_server.port}",
        headers={"Authorization": basic_auth["user"].auth},
    )

    assert response.status_code == 200


def test_cmd_post_test_command(client, basic_auth, mock_post_request, ssh_server):
    # generate a key pair
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "ssh_port": ssh_server.port,
        },
        headers={"Authorization": basic_auth["user"].auth},
    )

    assert response.status_code == 200


def test_cmd_key_error(client, basic_auth, mock_post_request, ssh_server):
    # generate a key pair
    try:
        response = client.get(
            "/api/v1.0/cmd/test_error",
            json={
                "ssh_port": ssh_server.port,
            },
            headers={"Authorization": basic_auth["user"].auth},
        )
    except KeyError as err:
        assert err.args == ('host',)
    else:
        assert response.status_code == 400
        assert response.json['message'] == 'test_error is not supported!'


def test_cmd_wrong_http_methos(client, basic_auth, mock_post_request, ssh_server, test_command):
    # generate a key pair
    try:
        response = client.post(
            f"/api/v1.0/cmd/{test_command}",
            json={
                "ssh_port": ssh_server.port,
            },
            headers={"Authorization": basic_auth["user"].auth},
        )
    except Exception as err:
        assert err.args == ("The http-method does not match with the schema, please check your request",)
    else:
        assert response.status_code == 400
        assert response.json['message'] == "method 'POST' for test_command is not supported!"


def test_cmd_arguments_post(client, basic_auth, mock_post_request, ssh_server, test_command):
    # generate a key pair
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "ssh_port": ssh_server.port,
            "resolution": "1440x900",
            "ppn": 2,
            "mem": 4,
            "jeff": "ertyuioghj",
        },
        headers={"Authorization": basic_auth["user"].auth},
    )

    assert response.status_code == 200

def test_cmd_arguments_get(client, basic_auth, mock_post_request, ssh_server, test_command):
    # generate a key pair

    response = client.get(
        f"/api/v1.0/cmd/{test_command}?ssh_port={ssh_server.port}&resolution=1440x900&ppn=2&mem=4&jeff=adfadsfasdf",
        headers={"Authorization": basic_auth["user"].auth},
    )

    assert response.status_code == 200
