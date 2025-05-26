import json

import asyncpg
from asyncpg import InvalidCatalogNameError, connect
from fastapi import HTTPException, status
from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator

from app.config.logging import logger
from app.config.settings import settings as config


Base = declarative_base()


async def _init_connection(conn):
    """Json codec for proper json fields encode/decode"""
    await conn.set_type_codec('jsonb',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog'
                              )
    await conn.set_type_codec('json',
                              encoder=json.dumps,
                              decoder=json.loads,
                              schema='pg_catalog'
                              )


async def get_connection_pool():
    try:
        _connection_pool = await asyncpg.create_pool(
            min_size=1,
            max_size=40,
            command_timeout=60,
            max_queries=10,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB,
            init=_init_connection,
            server_settings={'application_name': 'webapi (asyncpg)'}
            # ssl="require",
        )
        logger.info("Database pool connection opened")
        return _connection_pool

    except Exception as e:

        logger.error("Database pool connection opener error: ", e)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database pool connection opener error"
        )


def dumps(d):
    return json.dumps(d, default=str)

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(
    config.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True
)

# Создаем фабрику сессий
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_async_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()
