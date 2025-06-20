import pytest
import db


@pytest.mark.asyncio
async def test_db():
    await db.connect_db()
    async with db.pool.acquire() as conn:
        val = await conn.fetchval("SELECT 1")
        assert val == 1
    await db.disconnect_db()


@pytest.mark.asyncio
async def test_chat_log():
    await db.connect_db()

    # Insert a chat log entry
    inserted_id = await db.insert_chat_log(
        session_id="test-session-1",
        query="Hello, world!",
        response="Hi there!",
        response_time=50,
    )
    assert inserted_id is not None

    # Fetch the inserted row manually
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM chat_logs WHERE id = $1", inserted_id)
        assert row is not None
        assert row["session_id"] == "test-session-1"
        assert row["response"] == "Hi there!"

    # Clean up by deleting the inserted row
    async with db.pool.acquire() as conn:
        await conn.execute("DELETE FROM chat_logs WHERE id = $1", inserted_id)

    await db.disconnect_db()
