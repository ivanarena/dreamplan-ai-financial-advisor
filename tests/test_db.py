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
async def test_reply_log():
    await db.connect_db()

    # Insert a chat log entry
    await db.insert_reply(
        session_id="test-session-1",
        query="Hello, world!",
        response="Hi there!",
        response_time=50,
    )

    # Fetch the inserted row manually
    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM replies WHERE session_id = $1 AND query = $2",
            "test-session-1",
            "Hello, world!",
        )
        assert row is not None
        assert row["session_id"] == "test-session-1"
        assert row["response"] == "Hi there!"

        # Clean up by deleting the inserted row
        await conn.execute("DELETE FROM replies WHERE id = $1", row["id"])

    await db.disconnect_db()


@pytest.mark.asyncio
async def test_feedback_log():
    await db.connect_db()

    feedback_data = {
        "correctness": 5,
        "relevance": 4,
        "clarity": 5,
        "satisfaction": 4,
        "comments": "Very helpful!",
    }

    await db.insert_feedback("test-session-2", feedback_data)

    async with db.pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM feedbacks WHERE session_id = $1",
            "test-session-2",
        )
        assert row is not None
        assert row["correctness"] == 5
        assert row["comments"] == "Very helpful!"

        # Clean up by deleting the inserted row
        await conn.execute("DELETE FROM feedbacks WHERE id = $1", row["id"])

    await db.disconnect_db()
