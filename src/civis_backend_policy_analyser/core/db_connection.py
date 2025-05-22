import  contextlib
import os
from typing import AsyncIterator, Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncConnection,
    AsyncSession,
)

from civis_backend_policy_analyser.utils.constants import DB_BASE_URL, DB_PORT, DB_NAME


class DatabaseSessionManager:

    def __init__(self):
        db_url = DB_BASE_URL.format(
            db_user="ffg",  #  os.getenv("DB_USER"),
            db_secret="ffg_jpmc_civis",  #  os.getenv("DB_SECRET"),
            db_port=DB_PORT,
            database_name=DB_NAME
        )
        engine_keywords = {}
        self._engine = create_async_engine(db_url, **engine_keywords)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()

async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
