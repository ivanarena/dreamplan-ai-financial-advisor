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

replies = Table(
    "replies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("session_id", String(40), index=True),
    Column("query", Text),
    Column("response", Text),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
    Column("response_time", Integer, nullable=True),
)

feedbacks = Table(
    "feedbacks",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("session_id", String(40), index=True),
    Column("correctness", Integer, nullable=True),
    Column("relevance", Integer, nullable=True),
    Column("clarity", Integer, nullable=True),
    Column("satisfaction", Integer, nullable=True),
    Column("comments", Text, nullable=True),
    Column("timestamp", TIMESTAMP, server_default=func.now()),
)


async def connect_db():
    global pool
    if pool is None:
        retries = 5
        delay = 2
        for attempt in range(1, retries + 1):
            try:
                pool = await asyncpg.create_pool(
                    DATABASE_URL,
                    ssl="require",
                    statement_cache_size=0,
                )
                print("✅ Database pool created (statement cache disabled)")
                return
            except Exception as e:
                print(f"❌ DB connection failed: {e} (attempt {attempt}/{retries})")
                if attempt == retries:
                    raise
                await asyncio.sleep(delay)


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


async def insert_reply(session_id: str, query: str, response: str, response_time: int):
    async with pool.acquire() as conn:
        await conn.fetchrow(
            """
            INSERT INTO replies(session_id, query, response, response_time)
            VALUES ($1, $2, $3, $4)
            """,
            session_id,
            query,
            response,
            response_time,
        )


async def insert_feedback(session_id: str, feedback: dict):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO feedbacks (
                session_id,
                correctness,
                relevance,
                clarity,
                satisfaction,
                comments
            )
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            session_id,
            feedback.get("correctness"),
            feedback.get("relevance"),
            feedback.get("clarity"),
            feedback.get("satisfaction"),
            feedback.get("comments"),
        )


def create_tables(database_url: str) -> Engine:
    engine = create_engine(database_url, connect_args={"sslmode": "require"})
    metadata.create_all(engine)
    return engine
