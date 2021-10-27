def test_no_auth(client):
    response = client.post(
        "/api/v1.0/slurm/test_command",
    )
    assert response.status_code == 403


def test_cmd_test_command(client, basic_auth):
    # generate a key pair
    response = client.post(
        "/api/v1.0/cmd/test_command",
        headers={"Authorization": basic_auth["user"]["auth"]},
    )

    assert response.status_code == 200
