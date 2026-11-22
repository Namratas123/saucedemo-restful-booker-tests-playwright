def test_ping_reports_the_service_is_up(api):
    response = api.get("/ping")

    # Restful-Booker answers its health check with 201 Created.
    assert response.status == 201


def test_valid_credentials_return_a_token(api):
    response = api.post("/auth", data={"username": "admin", "password": "password123"})

    assert response.status == 200
    token = response.json()["token"]
    assert isinstance(token, str)
    assert len(token) > 5


def test_wrong_password_does_not_return_a_token(api):
    response = api.post("/auth", data={"username": "admin", "password": "definitely-wrong"})

    # The API reports bad credentials in the body instead of using a 401.
    body = response.json()
    assert "token" not in body
    assert body["reason"] == "Bad credentials"
