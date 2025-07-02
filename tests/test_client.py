import pytest


@pytest.mark.asyncio
async def test_session(client):
    response = await client.get("/")  # await here

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "session_id" in response.cookies
    assert "<html" in response.text.lower()
    assert "chat" in response.text.lower() or "message" in response.text.lower()


@pytest.mark.asyncio
async def test_existing_session(client):
    cookies = {"session_id": "test-session-id"}
    response = await client.get("/", cookies=cookies)  # await here

    assert response.status_code == 200
    assert (
        response.cookies.get("session_id") is None
    )  # means it reused the existing one
    assert "<html" in response.text.lower()


@pytest.mark.asyncio
async def test_chat_unset_session(client):
    response = await client.post("/chat", json={"message": "Hello"})  # await here
    assert response.status_code == 400
    assert response.json() == {"error": "Session ID not set."}


@pytest.mark.asyncio
async def test_chat_session(monkeypatch, client):
    async def mock_chat(messages):
        return "Test reply"

    monkeypatch.setattr("main.chat", mock_chat)

    cookies = {"session_id": "test-session-id"}
    response = await client.post(
        "/chat", json={"message": "Hello"}, cookies=cookies
    )  # await here
    assert response.status_code == 200
    assert "reply" in response.json()
    assert response.json()["reply"] == "Test reply"
