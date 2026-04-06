from asyncio import current_task
from core.config import settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    async_scoped_session,
)
import core.models


class DatabaseHelper:
    def __init__(self, db_url, db_echo=False):
        self.engine = create_async_engine(
            url=db_url,
            echo=db_echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def session_dependencies(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(
    db_url=settings.db_url,
    db_echo=settings.db_echo,
)
