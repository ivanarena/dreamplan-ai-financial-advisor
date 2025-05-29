def test_session(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "session_id" in response.cookies
    assert "<html" in response.text.lower()
    assert (
        "chat" in response.text.lower() or "message" in response.text.lower()
    )  # assuming your template has it


def test_existing_session(client):
    cookies = {"session_id": "test-session-id"}
    response = client.get("/", cookies=cookies)

    assert response.status_code == 200
    assert (
        response.cookies.get("session_id") is None
    )  # means it reused the existing one
    assert "<html" in response.text.lower()
