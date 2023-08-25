from asyncio.tasks import current_task
from functools import lru_cache

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.app_configs import settings

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=True)
BaseModel = declarative_base()


@lru_cache
def create_session():
    Session = async_scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
        ),
        scopefunc=current_task,
    )
    return Session


async def get_session():
    Session = create_session()
    try:
        yield Session
    finally:
        await Session.remove()
