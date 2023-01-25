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
    # Execute a test command using GET method
    response = client.get(
        f"/api/v1.0/cmd/{test_command}?ssh_port={ssh_server.port}",
        headers={"Authorization": basic_auth["user"].auth},
    )

    # Check that it is successful and output is as expected
    assert response.status_code == 200
    assert response.json['message'] == ['vim']


def test_cmd_test_command_with_service_role(client, basic_auth, mock_post_request, ssh_server, test_command):
    # Execute a test command using GET method
    response = client.get(
        f"/api/v1.0/cmd/{test_command}?ssh_port={ssh_server.port}&username=service",
        headers={"Authorization": basic_auth["service"].auth},
    )

    # Check that it is successful and output is as expected
    assert response.status_code == 200
    assert response.json['message'] == ['vim']


def test_cmd_post_test_command(client, basic_auth, mock_post_request, ssh_server):
    # Execute a test command using POST method
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "file": "vim-yong-blah",
        },
        headers={"Authorization": basic_auth["user"].auth},
    )
    # Check that it is successful and output is as expected
    assert response.status_code == 200
    assert response.json['message'] == ['vim', 'yong']


def test_cmd_post_test_command_with_service_role(client, basic_auth, mock_post_request, ssh_server):
    # Execute a test command using POST method
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "file": "vim-yong-blah",
            "username": "service"
        },
        headers={"Authorization": basic_auth["service"].auth},
    )
    # Check that it is successful and output is as expected
    assert response.status_code == 200
    assert response.json['message'] == ['vim', 'yong']


def test_cmd_post_output_not_match(client, basic_auth, mock_post_request, ssh_server):
    # Execute a test command using POST method with no match to output regular expression
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "file": "vim-nomatch-blah",
        },
        headers={"Authorization": basic_auth["user"].auth},
    )
    # Check that it is successful and output is empty
    assert response.status_code == 200
    assert response.json['message'] == []


def test_cmd_key_error(client, basic_auth, mock_post_request, ssh_server):
    # Execute an unsupport command
    response = client.get(
        "/api/v1.0/cmd/test_error",
        json={
            "file": "vim-yong-blah"
        },
        headers={"Authorization": basic_auth["user"].auth},
    )

    # Check for status code and error message
    assert response.status_code == 400
    assert response.json['message'] == 'test_error is not supported!'


def test_cmd_wrong_http_methos(client, basic_auth, mock_post_request, ssh_server, test_command):
    # Execute test command with wrong method
    response = client.post(
        f"/api/v1.0/cmd/{test_command}",
        json={
            "file": "vim-yong-blah"
        },
        headers={"Authorization": basic_auth["user"].auth},
    )

    # Check for status code and error message
    assert response.status_code == 400
    assert response.json['message'] == "method 'POST' for test_command is not supported!"


def test_cmd_arguments_post(client, basic_auth, mock_post_request, ssh_server, test_command):
    # Execute test command with parameters
    response = client.post(
        "/api/v1.0/cmd/test_post_command",
        json={
            "file": "blah-vim-yong-blah",
            "resolution": "1440x900",
            "ppn": 2,
            "mem": 4,
            "jeff": "ertyuioghj",
        },
        headers={"Authorization": basic_auth["user"].auth},
    )

    assert response.status_code == 200
    assert response.json['message'] == ['vim', 'yong']

def test_cmd_arguments_get(client, basic_auth, mock_post_request, ssh_server, test_command):
    # Execute test command with parameters
    response = client.get(
        f"/api/v1.0/cmd/{test_command}?file=look-for-vim-string&resolution=1440x900&ppn=2&mem=4&jeff=adfadsfasdf",
        headers={"Authorization": basic_auth["user"].auth},
    )

    # Check that it is successful and output is as expected
    assert response.status_code == 200
    assert response.json['message'] == ['vim']