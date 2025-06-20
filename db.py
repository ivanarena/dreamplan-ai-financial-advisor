import os
import asyncpg
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
import asyncio
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    func,
)

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"

pool: asyncpg.Pool | None = None

metadata = MetaData()

chat_logs = Table(
    "chat_logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("session_id", String(40), index=True),
    Column("query", Text),
    Column("response", Text),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
    Column("feedback", Integer, nullable=True),
    Column("response_time", Integer, nullable=True),
)


async def connect_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            ssl="require",
            statement_cache_size=0,  # 💡 disables prepared statement caching
        )
        print("✅ Database pool created (statement cache disabled)")


async def disconnect_db():
    global pool
    if pool:
        try:
            await asyncio.wait_for(pool.close(), timeout=10)
            print("🛑 Database pool closed")
        except asyncio.TimeoutError:
            print("⚠️ Timed out while closing the database pool")
        finally:
            pool = None


async def insert_chat_log(
    session_id: str, query: str, response: str, response_time: int
) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO chat_logs(session_id, query, response, response_time)
            VALUES ($1, $2, $3, $4)
            RETURNING id
            """,
            session_id,
            query,
            response,
            response_time,
        )
        return row["id"]


async def update_feedback(reply_id: int, session_id: str, feedback: int):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE chat_logs
            SET feedback = $1
            WHERE id = $2 AND session_id = $3
            """,
            feedback,
            reply_id,
            session_id,
        )


def create_tables(database_url: str) -> Engine:
    engine = create_engine(database_url, connect_args={"sslmode": "require"})
    metadata.create_all(engine)
    return engine
